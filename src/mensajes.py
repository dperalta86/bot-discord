# -*- coding: utf-8 -*-
from random import choice

# --- Mensajes para TPs ---
MENSAJES_TP = [
    "📝 **¡Recordatorio de TP!**\n¡No dejen para mañana lo que pueden commitear hoy! (Fecha: {fecha})",
    "🔧 **TP pendiente:**\n¿Ya empezaron? Porque el deadline ({fecha}) se acerca más rápido que un `segfault`.",
    "🚀 **¡Atención, equipo!**\nEl TP vence el {fecha}. ¡A programar se ha dicho!",
    "💡 **Idea brillante o bug eterno?**\nEl TP vence el {fecha}. ¡Hora de transformar café en código!",
    "👨‍💻 **Compilando esperanzas...**\nEl TP tiene deadline el {fecha}. ¡Que no se les pase como un `;` olvidado!",
    "📦 **Push, commit, entrega.**\nNo se olviden que el TP se entrega el {fecha}. ¡Let's go coders!",
]

# --- Mensajes para Exámenes ---
MENSAJES_EXAMEN = [
    "📚 **¡Recordatorio de examen!**\nLa fecha {fecha} está más cerca que tu último `git push` desesperado.",
    "🧠 **Examen alert:**\n¿Repasaron todos los temas? El día {fecha} llegará antes de que lo notes.",
    "⚡ **¡A estudiar!**\nEl parcial es el {fecha}. ¡No caigan en un `while True` de procrastinación!",
    "🔍 **¿Entendiste el tema o lo estás googleando todavía?**\nExamen el {fecha}. ¡Estudien, cracks!",
    "📖 **Modo estudio ON.**\nEl examen es el {fecha}. ¡La recursión es infinita, pero tu tiempo no!",
    "🧪 **Evaluación inminente...**\nEl {fecha} tienen examen. ¡Que no los evalúe el sistema operativo!",
]

# --- Mensajes para Clases Especiales ---
MENSAJES_CLASES = [
    "📅 **¡Clase especial!**\nEl {fecha} hay clase fuera de lo habitual. ¡Agendalo y no faltes!",
    "🎥 **Recordatorio:**\nEl {fecha} la clase será virtual. ¡Revisen el campus o el link!",
    "🕐 **Cambio de horario:**\nEl {fecha} la clase será en otro horario. ¡Estén atentos!",
]

# --- Mensajes Motivacionales ---
MENSAJES_MOTIVACION = [
    "🚀 **Motivación del día:**\nCada línea de código es un paso más. ¡Seguimos construyendo!",
    "🌟 **Ánimo equipo:**\nNo se trata de no fallar, sino de volver a compilar cada vez. ¡Vamos!",
    "🎯 **Pequeño empujón:**\nSi hoy no te sale, mañana puede que sí. ¡Seguimos adelante!",
    "🔥 **Recuerda:**\nEstudiar también es parte del éxito. ¡Estás más cerca de lo que creés!",
]

# --- Funciones para seleccionar mensajes aleatorios ---
def mensaje_tp(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para TPs."""
    return choice(MENSAJES_TP).format(fecha=fecha)

def mensaje_examen(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para exámenes."""
    return choice(MENSAJES_EXAMEN).format(fecha=fecha)

def mensaje_clase(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para exámenes."""
    return choice(MENSAJES_CLASES).format(fecha=fecha)

def mensaje_motivacional(fecha: str) -> str:
    """Devuelve un mensaje aleatorio para exámenes."""
    return choice(MENSAJES_MOTIVACION).format(fecha=fecha)