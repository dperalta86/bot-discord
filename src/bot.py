import discord
from discord.ext import commands, tasks
from flask import Flask
from threading import Thread
import json
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from mensajes import mensaje_tp, mensaje_examen  # Importar las funciones
from utils import cargar_eventos, formatear_fecha

# --- Configuración inicial ---
load_dotenv()  # Carga variables de entorno desde .env
TOKEN = os.getenv("DISCORD_TOKEN")
JSON_URL = os.getenv("JSON_URL") # URL del JSON remoto
LOCAL_PATH="data/eventos.json"

# Configura Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "¡Bot de Discord en línea! Usa !ayuda en tu servidor."

@app.route('/ping')
def ping():
    return "pong", 200

def run_flask():
    app.run(host='0.0.0.0', port=8080)

# Inicia Flask en segundo plano
Thread(target=run_flask).start()

# Configura el bot de Discord
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,  # Desactiva el comando de ayuda por defecto
)

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user.name}")

@bot.event
async def on_guild_join(guild):
    """Envía un mensaje al unirse a un nuevo servidor."""
    # Busca el primer canal de texto donde el bot pueda escribir
    canal = next((c for c in guild.text_channels if c.permissions_for(guild.me).send_messages), None)
    
    if canal:
        mensaje = (
            "🎉 **¡Hola comunidad!** 🎉\n"
            f"Soy {bot.user.name}, el bot no oficial de recordatorios de la facultad.\n\n"
            "📌 **Mis funciones principales**:\n"
            "Me programaron para enviar recordatorios de deadlines o fechas importantes.\n"
            "Segurmante esté escribiendo en estos días, hay muchos TP's por entregar tosavia!\n"
            "🛠️ **Atajo para los curiosos**:\n"
            "Usa `!eventos` para ver todos los eventos registrados.\n"
            "*«Programado para evitar tu procrastinación»* 💻"
        )
        await canal.send(mensaje)

# --- Comandos del Bot ---
@bot.check
async def no_dms(ctx):
    if not ctx.guild:
        await ctx.send("🚫 **Aquí no hay nada...**\n¡Los comandos solo funcionan en servidores! *(Como el Wi-Fi de la facu, a veces conecta, a veces no)* 📡")
        return False
    return True

@bot.command(name="agregar_evento")
async def agregar_evento(ctx, nombre: str, fecha: str, avisos: str):
    # Si es un DM, envía mensaje humorístico y bloquea
    if not ctx.guild:
        await ctx.send(
            "🤖 **¡Ups! ¿Hablando solo con un bot?**\n"
            "Los bots también tenemos vida social... ¡en servidores! 🎉\n\n"
            "**¿Cómo agregar eventos?**\n"
            "1. Ve al servidor de tu materia.\n"
            "2. Usa `!agregar_evento \"Nombre\" AAAA-MM-DD días` (ej: `!agregar_evento \"Parcial\" 2024-12-20 3,1`).\n"
            "3. ¡Solo admins pueden hacerlo! *(Como diría Skynet: 'No tienes permisos.')* 🚫\n\n"
            "*PD: Si esto fuera un chatbot de película, ya habría iniciado el apocalipsis.* ☠️"
        )
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
        # Acá se ebería actualizar el JSON remoto (ej: vía GitHub API o manualmente)
        with open("data/eventos.json", "w") as f:
            json.dump(eventos, f, indent=4)
        await ctx.send(f"✅ **Evento agregado**: '{nombre}' el {fecha}. ¡Gracias por evitar el caos temporal! ⏳")
    except Exception as e:
        await ctx.send(f"⚠️ **Error crítico**: `{e}`. ¡Corran, es un bug! 🐞")

@bot.command()
async def eventos(ctx):
    """Muestra eventos del servidor actual."""
    try:
        eventos = cargar_eventos(json_url=JSON_URL, local_path=LOCAL_PATH, servidor_id=str(ctx.guild.id))
        
        if not eventos:
            await ctx.send("📭 No hay eventos programados. ¡Agrega uno con `!agregar_evento`!")
            return
        
        mensaje = "📅 **Eventos activos:**\n"
        for e in eventos:
            try:
                if 'fecha' not in e or 'avisos' not in e:
                    continue
                mensaje += f"- **{e['nombre']}**: {e['fecha']} (avisos: {', '.join(map(str, e['avisos']))} días antes)\n"
            except KeyError:
                continue
        
        await ctx.send(mensaje)
    except Exception as e:
        await ctx.send(f"❌ Error al cargar eventos: {str(e)}")

@bot.command(name="ayuda")
async def ayuda(ctx):
    """Muestra la ayuda del bot."""
    ayuda_msg = """
🤖 **Comandos de PdepBot**:
- `!agregar_evento "Nombre" YYYY-MM-DD dias` → Agrega un evento (ej: `!agregar_evento "Parcial" 2024-07-20 3,1`).
- `!eventos` → Lista todos los eventos.
- `!ayuda` → Muestra este mensaje.

*"Más confiable que un `try-catch` vacío."* 🛠️
    """
    await ctx.send(ayuda_msg)

@bot.command()
async def debug(ctx):
    """Muestra información de configuración."""
    info = f"""
    🔍 **Debug Info**:
    - JSON_URL: {JSON_URL}
    - Servidor ID: {ctx.guild.id}
    - Canal ID : {ctx.channel.id}
    - Archivo local: {LOCAL_PATH}
    - Token: {'✅' if TOKEN else '❌'}
    """
    await ctx.send(info)

# --- Tarea automática de recordatorios ---
@tasks.loop(hours=24)
async def enviar_recordatorios():
    """Envía recordatorios de eventos programados."""
    try:
        eventos = cargar_eventos(json_url=JSON_URL, local_path="data/eventos.json")
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
                    canal = bot.get_channel(int(evento["canal_id"]))
                    if canal:
                        if "parcial" in evento["nombre"].lower() or "examen" in evento["nombre"].lower():
                            mensaje = mensaje_examen(evento["fecha"])
                        else:
                            mensaje = mensaje_tp(evento["fecha"])
                        await canal.send(mensaje)
            except Exception as e:
                print(f"Error al procesar evento {evento}: {e}")
    except Exception as e:
        print(f"Error crítico en enviar_recordatorios: {e}")

# --- Eventos del Bot ---
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user.name}")
    enviar_recordatorios.start()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado. Usa `!ayuda` para ver la lista.")
    else:
        await ctx.send(f"⚠️ **Error**: {error}")

# --- Ejecución ---
if __name__ == "__main__":
    bot.run(TOKEN)