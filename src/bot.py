import discord
from discord.ext import commands, tasks
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

# Intents (necesarios para Discord.py v2.x+)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None,  # Desactiva el comando de ayuda por defecto
)

# --- Comandos del Bot ---
@bot.command(name="agregar_evento")
async def agregar_evento(ctx, nombre: str, fecha: str, avisos: str):
    """Agrega un evento al JSON (solo admins). Ejemplo: !agregar_evento "Parcial" 2024-07-20 3,1"""
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ **Error**: Solo los admins pueden agregar eventos.")
        return

    try:
        eventos = cargar_eventos()
        nuevo_evento = {
            "nombre": nombre,
            "fecha": fecha,
            "avisos": [int(d) for d in avisos.split(",")],
            "servidor_id": str(ctx.guild.id),
            "canal_id": str(ctx.channel.id),
        }
        eventos.append(nuevo_evento)
        
        # Acá se ebería actualizar el JSON remoto (ej: vía GitHub API o manualmente)
        with open("data/eventos.json", "w") as f:
            json.dump(eventos, f, indent=4)
        
        await ctx.send(f"✅ **Evento agregado**: '{nombre}' el {fecha} (avisos: {avisos} días antes).")
    except Exception as e:
        await ctx.send(f"❌ **Error**: {e}. Revisa el formato: !agregar_evento 'Nombre' YYYY-MM-DD dias (ej: 3,1)")

@bot.command(name="eventos")
async def listar_eventos(ctx):
    """Lista todos los eventos programados."""
    eventos = cargar_eventos()
    eventos_filtrados = [e for e in eventos if e["servidor_id"] == str(ctx.guild.id)]
    
    if not eventos_filtrados:
        await ctx.send("📭 No hay eventos programados. ¡Agrega uno con `!agregar_evento`!")
        return
    
    mensaje = "📅 **Eventos activos:**\n" + "\n".join(
        f"- **{e['nombre']}**: {e['fecha']} (avisos: {', '.join(map(str, e['avisos']))} días antes)"
        for e in eventos_filtrados
    )
    await ctx.send(mensaje)

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

# --- Tarea automática de recordatorios ---
@tasks.loop(hours=24)
async def enviar_recordatorios():
    eventos = cargar_eventos(JSON_URL)
    hoy = datetime.now().date()
    
    for evento in eventos:
        try:
            fecha_evento = formatear_fecha(evento["fecha"])
            dias_restantes = (fecha_evento - hoy).days
            
            if dias_restantes in evento["avisos"]:
                canal = bot.get_channel(int(evento["canal_id"]))
                
                # Seleccionar mensaje según el tipo de evento
                if "parcial" in evento["nombre"].lower() or "examen" in evento["nombre"].lower():
                    mensaje = mensaje_examen(evento["fecha"])
                else:
                    mensaje = mensaje_tp(evento["fecha"])
                
                await canal.send(mensaje)
        except Exception as e:
            print(f"Error al procesar evento {evento}: {e}")

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