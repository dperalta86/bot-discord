import asyncio
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os
from dotenv import load_dotenv

# --- Configuración inicial ---
load_dotenv()  # Carga variables de entorno desde .env
TOKEN = os.getenv("DISCORD_TOKEN")

# Configura Flask - Servidor para abrir puerto y evitar errores en Render
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
intents = discord.Intents.all()
intents.messages = True
intents.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,  # Desactiva el comando de ayuda por defecto
)


@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user.name}")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando no encontrado. Usa `!ayuda` para ver la lista.")
    else:
        await ctx.send(f"⚠️ **Error**: {error}")

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
            "Segurmante esté escribiendo en estos días, hay muchos TP's por entregar todavía!\n"
            "🛠️ **Atajo para los curiosos**:\n"
            "Usa `!eventos` para ver todos los eventos registrados.\n"
            "*«Programado para evitar tu procrastinación»* 💻"
        )
        await canal.send(mensaje)

async def main():
    # --- Cargar Cogs ---
    await bot.load_extension("eventos")

    # Iniciar el bot
    await bot.start(TOKEN)

# Ejecutar el bot
asyncio.run(main())