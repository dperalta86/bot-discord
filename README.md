## 📢 Discord Reminder Bot (PdeP Edition)

Bot de recordatorios automatizados para materias universitarias, comenzando con Paradigmas de Programación (PdeP).

---

### 📌 Descripción

Bot de Discord diseñado para automatizar avisos de fechas importantes (parciales, entregas de TP, reuniones) mediante:

    ✅ Recordatorios programados con mensajes dinámicos y aleatorios.

    ✅ Soporte multi-servidor (varias cátedras/comisiones).

    ✅ Configuración remota vía JSON (accesible para no técnicos).

    ✅ Mención a @everyone o roles personalizados.

Roadmap: Extensible a otras materias con mínima configuración.
### ⚙️ Tecnologías

    Lenguaje: Python 3.10+

    Librerías:

        discord.py (API de Discord).

        python-dotenv (gestión de tokens).

        requests (carga remota de JSON).

    Hosting: Compatible con Replit, Render, VPS.

### 🚀 Configuración Inicial
#### 1. Requisitos

    Token de bot de Discord (Guía).

    Python 3.10+ y pip.

    Repositorio GitHub para el JSON de eventos (opcional).

#### 2. Instalación

    Clonar repositorio
    git clone https://github.com/dperalta86/bot-discord.git
    cd bot-discord

Entorno virtual (recomendado)

    python3 -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

Instalar dependencias

    pip install -r requirements.txt

#### 3. Variables de Entorno

Crear .env en la raíz:

    DISCORD_TOKEN=tu_token_aquí
    JSON_URL=https://raw.githubusercontent.com/tu_usuario/pdepbot-data/main/eventos.json


### 🛠️ ¿Cómo sigue esto?

📅 Flujo de Trabajo

    Editar eventos:

        Modificar el archivo eventos.json en GitHub o localmente.

    Sincronizar:

        El bot actualiza los eventos automáticamente cada 24h (o con !actualizar).

    Notificaciones:

        Envía mensajes en los canales configurados con @everyone o roles.

🔮 Roadmap

    Fase 1: Uso interno en PdeP (2024).

    Fase 2: Extender a otras cátedras (configuración modular).

    Fase 3: Panel web para gestión visual de eventos.

📜 Licencia

MIT License. Libre para uso y modificación.
📬 Contacto

¿Preguntas o contribuciones? Abrí un issue o contactame a @dperalta86 en Discord.

✨ "Porque recordar fechas debería ser tan fácil como copiar código de Stack Overflow."
Notas Adicionales

    Personalización: Los mensajes se ajustan al tono informal/geek (ver mensajes.py).

    Escalabilidad: Diseñado para integrarse con APIs externas (Google Calendar, Notion).

🔧 ¿Problemas?

    Verifica los permisos del bot en Discord.

    Asegúrate de que el JSON remoto sea accesible.
