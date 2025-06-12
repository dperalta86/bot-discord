# --- Eventos y commands del Bot --- #
import json
from discord.ext import commands, tasks
from datetime import date, datetime, timedelta
import os
from mensajes import mensaje_clase, mensaje_motivacional, mensaje_tp, mensaje_examen  # Importar las funciones
from utils import cargar_eventos, formatear_fecha

JSON_URL = os.getenv("JSON_URL") # URL del JSON remoto
LOCAL_PATH="data/eventos.json"

with open("data/mensajes_definidos.json", "r", encoding="utf-8") as f:
    MENSAJES_PREDEFINIDOS = json.load(f)

class Eventos(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.enviar_recordatorios.start()

    def cog_unload(self):
        self.enviar_recordatorios.cancel()
    
    # --- commands ---
    @commands.check
    async def no_dms(ctx):
        if not ctx.guild:
            await ctx.send(
                "🤖 **¡Ups! ¿Hablando solo con un bot?**\n"
                "Los bots también tenemos vida social... ¡en servidores! 🎉\n\n"
                "¡Los comandos solo funcionan en servidores! *(Como el Wi-Fi de la facu, a veces conecta, a veces no)* 📡"
                "**¿Cómo agregar eventos?**\n"
                "1. Entrá al servidor de la materia.\n"
                "2. Usa `!agregar_evento \"Nombre\" AAAA-MM-DD días` (ej: `!agregar_evento \"Parcial\" 2024-12-20 3,1`).\n"
                "3. ¡Solo admins pueden hacerlo! *(Como diría Skynet: 'No tienes permisos.')* 🚫\n\n"
                "*PD: Si esto fuera un chatbot de película, ya habría iniciado el apocalipsis.* ☠️"
            )
            return False
        return True
    
    @commands.command()
    async def info(self, ctx):
        await ctx.send(MENSAJES_PREDEFINIDOS["info"])

    @commands.command(name="ayuda")
    async def ayuda(self, ctx):
        """Muestra la ayuda del bot."""
        await ctx.send(MENSAJES_PREDEFINIDOS["ayuda"])

    @commands.command(name="agregar_evento")
    async def agregar_evento(self, ctx, nombre: str, fecha: str, avisos: str):
        # Si es un DM, envía mensaje humorístico y bloquea
        if not ctx.guild:
            await ctx.send("🚫 **Aquí no hay nada...**\n¡Los comandos solo funcionan en servidores! *(Como el Wi-Fi de la facu, a veces conecta, a veces no)* 📡")
            return

        # Verificar permisos solo en servidor
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ **Error 403**: ¡No tienes permisos de admin! *(Hazte amigo del/la prof primero)* 📚")
            return

        # Lógica para guardar el evento (solo si pasa las validaciones)
        try:
            eventos = cargar_eventos(json_url=JSON_URL, local_path=LOCAL_PATH)
            nuevo_evento = {
                "nombre": nombre,
                "fecha": fecha,
                "avisos": [int(d) for d in avisos.split(",")],
                "servidor_id": str(ctx.guild.id),
                "canal_id": str(ctx.channel.id)
            }
            eventos.append(nuevo_evento)
            # Acá se ebería actualizar el JSON remoto (ej: vía GitHub API o manualmente). Todavia no implementado
            with open("data/eventos.json", "w") as f:
                json.dump(eventos, f, indent=4)
            await ctx.send(f"✅ **Evento agregado**: '{nombre}' el {fecha}. ¡Gracias por evitar el caos temporal! ⏳")
        except Exception as e:
            await ctx.send(f"⚠️ **Error crítico**: `{e}`. ¡Corran, es un bug! 🐞")

    @commands.command(name="eventos")
    async def eventos(self, ctx):
        """Muestra eventos del servidor actual."""
        try:
            eventos = cargar_eventos(json_url=JSON_URL, local_path=LOCAL_PATH)
            eventos_servidor = [e for e in eventos if e.get("servidor_id") == str(ctx.guild.id)]

            if not eventos_servidor:
                await ctx.send("📭 No hay eventos programados. ¡Agrega uno con `!agregar_evento`!")
                return
            
            mensaje = "📅 **Eventos activos:**\n"
            for e in eventos_servidor:
                try:
                    if 'fecha' not in e or 'avisos' not in e:
                        continue
                    mensaje += f"- **{e['nombre']}**: {e['fecha']} (avisos: {', '.join(map(str, e['avisos']))} días antes)\n"
                except KeyError:
                    continue
            
            await ctx.send(mensaje)
        except Exception as e:
            await ctx.send(f"❌ Error al cargar eventos: {str(e)}")

    # Eliminar en producción...
    @commands.command()
    async def debug(self, ctx):
        """Muestra información de configuración."""
        info = f"""
        🔍 **Debug Info**:
        - JSON_URL: {JSON_URL}
        - Servidor ID: {ctx.guild.id}
        - Canal ID : {ctx.channel.id}
        - Archivo local: {LOCAL_PATH}
        """
        await ctx.send(info)

    # --- Tarea automática de recordatorios ---
    @tasks.loop(hours=24.0)
    async def enviar_recordatorios(self):
        """Envía recordatorios de eventos programados."""
        try:
            eventos = cargar_eventos(json_url=JSON_URL, local_path=LOCAL_PATH)
            hoy = datetime.now().date()
            
            for evento in eventos:
                try:                  
                    fecha_evento = formatear_fecha(evento["fecha"])
                    dias_restantes = (fecha_evento - hoy).days
                    
                    if dias_restantes in evento["avisos"]:
                        canal = self.bot.get_channel(int(evento["canal_id"]))

                        if canal:
                            fecha = evento["fecha"]
                            tipo = evento.get("tipo", "").lower()

                            if not tipo:
                                nombre = evento["nombre"].lower()
                                if any(t in nombre for t in ["parcial", "examen", "recuperatorio", "final"]):
                                    tipo = "examen"
                                else:
                                    tipo = "tp"

                            if tipo == "examen":
                                mensaje_base = mensaje_examen(evento["fecha"])
                            elif tipo == "tp":
                                mensaje_base = mensaje_tp(evento["fecha"])
                            elif tipo == "clase":
                                mensaje_base = mensaje_clase(evento["fecha"])
                            elif tipo == "motivacional":
                                mensaje_base = mensaje_motivacional(evento["fecha"])
                            else:
                                mensaje_base = f"📌 **Recordatorio:**\nEvento programado para el {fecha}"

                            # Agregar anexo de proximidad (hoy, mañana)
                            if dias_restantes == 0:
                                anexo = " (¡hoy!)"
                            elif dias_restantes == 1:
                                anexo = " (mañana!)"
                            else:
                                anexo = ""

                            mensaje = mensaje_base.format(fecha=f"{fecha}{anexo}")

                            # Agregar mensaje adicional si está definido
                            adicional = evento.get("mensaje_adicional", "")
                            if adicional:
                                mensaje += f"\n\n🗒️ {adicional}"

                            await canal.send(mensaje)
                except Exception as e:
                    print(f"Error al procesar evento {evento}: {e}")
        except Exception as e:
            print(f"Error crítico en enviar_recordatorios: {e}")
    
    @enviar_recordatorios.before_loop
    async def before_recordatorio(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Eventos(bot))
        
