# CRUD desacoplado de logica principal
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

RUTA_EVENTOS = Path("data/eventos.json")


def _leer_eventos() -> List[Dict]:
    if not RUTA_EVENTOS.exists():
        return []
    with open(RUTA_EVENTOS, "r") as f:
        return json.load(f)


def _guardar_eventos(eventos: List[Dict]):
    RUTA_EVENTOS.parent.mkdir(exist_ok=True)
    with open(RUTA_EVENTOS, "w") as f:
        json.dump(eventos, f, indent=4)


def agregar_evento(nombre: str, fecha: str, servidor_id: Optional[str] = None):
    eventos = _leer_eventos()
    nuevo_evento = {
        "nombre": nombre,
        "fecha": fecha,
        "servidor_id": servidor_id
    }
    eventos.append(nuevo_evento)
    _guardar_eventos(eventos)


def eliminar_evento(nombre: str, servidor_id: Optional[str] = None) -> bool:
    eventos = _leer_eventos()
    eventos_filtrados = [
        e for e in eventos
        if e["nombre"].lower() != nombre.lower() or (servidor_id and e.get("servidor_id") != servidor_id)
    ]
    if len(eventos) == len(eventos_filtrados):
        return False  # No se eliminó nada
    _guardar_eventos(eventos_filtrados)
    return True


def editar_evento(nombre: str, nueva_fecha: Optional[str] = None, nuevo_nombre: Optional[str] = None,
                  servidor_id: Optional[str] = None) -> bool:
    eventos = _leer_eventos()
    modificado = False
    for evento in eventos:
        if evento["nombre"].lower() == nombre.lower() and (servidor_id is None or evento.get("servidor_id") == servidor_id):
            if nueva_fecha:
                evento["fecha"] = nueva_fecha
            if nuevo_nombre:
                evento["nombre"] = nuevo_nombre
            modificado = True
    if modificado:
        _guardar_eventos(eventos)
    return modificado


def obtener_proximos_eventos(n: int = 5, servidor_id: Optional[str] = None) -> List[Dict]:
    eventos = _leer_eventos()
    hoy = datetime.now().date()
    proximos = [
        e for e in eventos
        if datetime.strptime(e["fecha"], "%Y-%m-%d").date() >= hoy and (servidor_id is None or e.get("servidor_id") == servidor_id)
    ]
    proximos.sort(key=lambda e: e["fecha"])
    return proximos[:n]
