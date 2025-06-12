from datetime import datetime
import json
import requests
from pathlib import Path
from typing import List, Dict

def cargar_eventos(json_url: str = None, local_path: str = "data/eventos.json") -> List[Dict]:
    """
    Carga eventos desde una URL remota (GitHub) o desde un archivo local como fallback.
    
    Args:
        json_url: URL del JSON remoto (opcional).
        local_path: Ruta al archivo local de backup.
        
    Returns:
        List[Dict]: Lista de eventos cargados.
        
    Raises:
        FileNotFoundError: Si no existe el archivo local y falla la descarga remota.
    """
    eventos = []
    
    # Intento carga remota
    if json_url:
        try:
            response = requests.get(
                json_url,
                timeout=10,
                headers={"Cache-Control": "no-cache"}  # Evita caché obsoleto
            )
            response.raise_for_status()
            eventos = response.json()
            # Guardar backup local
            Path(local_path).parent.mkdir(exist_ok=True)
            with open(local_path, "w") as f:
                json.dump(eventos, f, indent=4)
            print(f"✅ Cargados {len(eventos)} eventos desde GitHub")
            return eventos
        except Exception as e:
            print(f"⚠️ Error al cargar JSON remoto: {type(e).__name__} - {str(e)}")
    
    # Fallback local
    try:
        with open(local_path) as f:
            eventos = json.load(f)
        print(f"✅ Cargados {len(eventos)} eventos desde backup local")
        return eventos
    except Exception as e:
        print(f"❌ Error crítico: No se pudo cargar ningún JSON. {type(e).__name__} - {str(e)}")
        return []  # Retorna lista vacía para evitar crashes

def formatear_fecha(fecha_str):
    """Convierte 'YYYY-MM-DD' a un objeto datetime.date."""
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()