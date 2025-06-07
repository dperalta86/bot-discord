import unittest
from unittest.mock import patch, mock_open
from src.utils import cargar_eventos

class TestCargarEventos(unittest.TestCase):
    @patch('requests.get')
    def test_carga_remota(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{"nombre": "Parcial"}]
        
        eventos = cargar_eventos(json_url="http://fake-url.com")
        self.assertEqual(eventos, [{"nombre": "Parcial"}])
    
    @patch('builtins.open', mock_open(read_data='[{"nombre": "Local"}]'))
    def test_carga_local(self):
        eventos = cargar_eventos(json_url=None, local_path="fake_path.json")
        self.assertEqual(eventos, [{"nombre": "Local"}])

if __name__ == "__main__":
    unittest.main()