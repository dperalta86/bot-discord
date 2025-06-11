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
    
    # 1. Intento cargar desde la URL remota (GitHub)
    if json_url:
        try:
            response = requests.get(json_url, timeout=10)
            response.raise_for_status()  # Lanza error si HTTP != 200
            eventos = response.json()
            
            # Guardar backup local
            Path(local_path).parent.mkdir(exist_ok=True)  # Crea directorio si no existe
            with open(local_path, "w") as f:
                json.dump(eventos, f, indent=4)
                
            print("✅ Eventos cargados desde el JSON remoto.")
            
            return eventos

        except Exception as e:
            print(f"⚠️ Error al cargar JSON remoto: {e}. Usando backup local...")
    
    # 2. Fallback a archivo local
    try:
        with open(local_path) as f:
            eventos = json.load(f)
        print("✅ Eventos cargados desde backup local.")
        return eventos
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se pudo cargar el JSON: Archivo local '{local_path}' no encontrado y URL remota falló."
        )

def formatear_fecha(fecha_str):
    """Convierte 'YYYY-MM-DD' a un objeto datetime.date."""
    return datetime.strptime(fecha_str, "%Y-%m-%d").date()