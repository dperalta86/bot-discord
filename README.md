# 📢 Discord Reminder Bot (PdeP Edition)

Bot de recordatorios automatizados para materias universitarias, comenzando con Paradigmas de Programación (PdeP).

---

## 📌 Descripción

Bot de Discord diseñado para automatizar avisos de fechas importantes como parciales, entregas de TPs y reuniones. Cuenta con:

- ✅ Recordatorios programados con mensajes dinámicos y aleatorios.
- ✅ Soporte multi-servidor (varias cátedras/comisiones).
- ✅ Configuración remota vía JSON (accesible para no técnicos).
- ✅ Mención a @everyone o roles personalizados.

🧩 **Extensible a otras materias** con mínima configuración.

---

## ⚙️ Tecnologías

- **Lenguaje:** Python 3.10+
- **Librerías principales:**
  - `discord.py` – API de Discord.
  - `python-dotenv` – Gestión de variables de entorno.
  - `requests` – Carga remota de archivos JSON.
- **Hosting compatible:** Replit, Render, VPS o cualquier servicio con soporte Python.

---

## 🚀 Configuración Inicial

### 1. Requisitos

- Token de bot de Discord ([Guía oficial](https://discordpy.readthedocs.io/en/stable/discord.html))
- Python 3.10+ y pip
- (Opcional) Repositorio GitHub para el archivo `eventos.json`

### 2. Instalación

Clonar el repositorio:

```bash
git clone https://github.com/dperalta86/bot-discord.git
cd bot-discord
```

Entorno virtual (recomendado)

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Variables de Entorno

Crear .env en la raíz del proyecto y completa los siguientes datos:

```
DISCORD_TOKEN=tu_token_aquí
JSON_URL=https://raw.githubusercontent.com/tu_usuario/pdepbot-data/main/eventos.json
```

## 🛠️ ¿Cómo sigue esto?

### 📅 Flujo de Trabajo

- Editar eventos:

    Modificar el archivo eventos.json en GitHub o localmente.

- Sincronizar:

    El bot actualiza los eventos automáticamente cada 24h.

- Notificaciones:

    Envía mensajes en los canales configurados con @everyone o roles.



### 🔮 Roadmap

- 🧪 Fase 1: Uso interno en PdeP (2024).

- ⚙️ Fase 2: Extender a otras cátedras (configuración modular).

- 🌐 Fase 3: Panel web para gestión visual de eventos.



## 📜 Licencia

MIT License. Libre para uso y modificación.

### Notas Adicionales

Personalización: Los mensajes se ajustan al tono informal/geek (ver mensajes.py).
Escalabilidad: Diseñado para integrarse con APIs externas (Google Calendar, Notion).

### 🔧 ¿Problemas?

- Verifica que las dependencias estén instaladas
- Verifica los permisos del bot en Discord.
- Asegúrate de que el JSON remoto sea accesible.

----

## 🤝 Cómo Contribuir
¿Querés aportar?
- Hacé un fork del proyecto.
- Creá una nueva rama con tu mejora: git checkout -b feature/nombre-feature.
- Commiteá y hacé push.
- Enviá un pull request. Todas las propuestas serán revisadas.

El repositorio tiene ramas protegidas para garantizar estabilidad en producción.

### 📬 Contacto

¡Siéntete libre de contactarme para colaborar, reportar bugs o simplemente charlar sobre tecnología!
#### 🌐 Redes y Enlaces
| Plataforma | Link |
|------------|------|
| GitHub | ![Github contact](https://img.shields.io/badge/-@dperalta86-181717?style=flat&logo=github&logoColor=white) |
| Discord | ![Discord contact](https://img.shields.io/badge/-@dperalta86-5865F2?style=flat&logo=discord&logoColor=white) |
| X (Twitter) | ![Tweeter contact](https://img.shields.io/badge/-@dperalta_ok-1DA1F2?style=flat&logo=x&logoColor=white) |
| LinkeIn | ![Linked In contact](https://img.shields.io/badge/-dperalta86-0077B5?style=flat&logo=linkedin&logoColor=white) |

¿Por qué contactarme?

🤖 Ideas para mejorar proyectos.

🐞 Reportar errores o solicitar features.

☕ Tomar un café virtual (¡siempre disponible!).

**¿Preguntas o contribuciones sobre este proyecto? Abrí un issue o contactame a @dperalta86 en Discord.**
✨ _"Porque recordar fechas debería ser tan fácil como copiar código de Stack Overflow."_