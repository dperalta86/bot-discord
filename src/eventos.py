# --- Eventos y commands del Bot --- #
import json
from discord.ext import commands, tasks
from datetime import date, datetime, timedelta
import os
from mensajes import mensaje_tp, mensaje_examen  # Importar las funciones
from utils import cargar_eventos, formatear_fecha

JSON_URL = os.getenv("JSON_URL") # URL del JSON remoto
LOCAL_PATH="data/eventos.json"

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

    @commands.command(name="ayuda")
    async def ayuda(self, ctx):
        """Muestra la ayuda del bot."""
        ayuda_msg = """
    🤖 **Comandos de PdepBot**:
    - `!agregar_evento "Nombre" YYYY-MM-DD dias` → Agrega un evento (ej: `!agregar_evento "Parcial" 2024-07-20 3,1`).
    - `!eventos` → Lista todos los eventos.
    - `!ayuda` → Muestra este mensaje.

    *"Más confiable que un `try-catch` vacío."* 🛠️
        """
        await ctx.send(ayuda_msg)

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
    @tasks.loop(minutes=5.0)
    async def enviar_recordatorios(self):
        """Envía recordatorios de eventos programados."""
        try:
            eventos = cargar_eventos(json_url=JSON_URL, local_path=LOCAL_PATH)
            hoy = datetime.now().date()
            
            for evento in eventos:
                try:
                    # Verifica si el evento tiene los campos necesarios
                    if not all(key in evento for key in ['fecha', 'avisos', 'canal_id', 'nombre']):
                        print(f"⚠️ Evento incompleto: {evento}")
                        continue
                    
                    fecha_evento = formatear_fecha(evento["fecha"])
                    dias_restantes = (fecha_evento - hoy).days
                    
                    if dias_restantes in evento["avisos"]:
                        canal = self.bot.get_channel(int(evento["canal_id"]))

                        if canal:
                            if "parcial" in evento["nombre"].lower() or "examen" in evento["nombre"].lower() or "recuperatorio" in evento["nombre"].lower():
                                mensaje = mensaje_examen(evento["fecha"])
                                print(f"mensaje listo: {mensaje}")
                            else:
                                mensaje = mensaje_tp(evento["fecha"])
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
        
