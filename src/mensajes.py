# -*- coding: utf-8 -*-
from random import choice

# --- Mensajes para TPs ---
MENSAJES_TP = [
    "📝 **¡Recordatorio de TP!**\n¡No dejen para mañana lo que pueden commitear hoy! (Fecha: {fecha}).",
    "🔧 **TP pendiente:**\n¿Ya empezaron? Porque el deadline ({fecha}) se acerca más rápido que un `segfault`.",
    "🚀 **¡Atención, equipo!**\nEl TP vence el {fecha}. ¡A programar se ha dicho!",
]

# --- Mensajes para Exámenes ---
MENSAJES_EXAMEN = [
    "📚 **¡Recordatorio de examen!**\nLa fecha {fecha} está más cerca que tu último `git push` desesperado.",
    "🧠 **Examen alert:**\n¿Repasaron todos los temas? El día {fecha} llegará antes de que lo notes.",
    "⚡ **¡A estudiar!**\nEl parcial es el {fecha}. ¡No caigan en un `while True` de procrastinación!",
]

# --- Funciones para seleccionar mensajes aleatorios ---
def mensaje_tp(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para TPs."""
    return choice(MENSAJES_TP).format(fecha=fecha)

def mensaje_examen(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para exámenes."""
    return choice(MENSAJES_EXAMEN).format(fecha=fecha)