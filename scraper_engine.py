import datetime
import pytz
import requests
from bs4 import BeautifulSoup

LIMA_TZ = pytz.timezone('America/Lima')

def obtener_hora_lima():
    return datetime.datetime.now(LIMA_TZ)

def obtener_datos_reales_casas():
    ahora_lima = obtener_hora_lima()
    partidos = []

    # 1. La URL de la página que quieres raspar (Ejemplo)
    url = "https://www.marca.com/futbol/primera-division/calendario.html" 
    
    # Los "headers" simulan que eres un navegador real (Chrome) para que no te bloqueen
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 2. Descargar el HTML de la página
        respuesta = requests.get(url, headers=headers, timeout=10)
        
        if respuesta.status_code == 200:
            # 3. Parsear el HTML con BeautifulSoup
            soup = BeautifulSoup(respuesta.text, 'html.parser')
            
            # 4. BUSCAR LOS DATOS (Este es el núcleo del scraping)
            # Aquí inspeccionas la web. Supongamos que cada fila de partido tiene la clase CSS 'partido-fila'
            filas_partidos = soup.find_all('tr', class_='contenedor-partido') # <- Esto cambia según la web
            
            for i, fila in enumerate(filas_partidos):
                # Ejemplo de cómo extraer el texto de las etiquetas internas
                equipo_local = fila.find('span', class_='local').text.strip()
                equipo_visitante = fila.find('span', class_='visitante').text.strip()
                
                # Armamos el diccionario real con lo clonado de la web
                partido_info = {
                    "id": str(i + 1),
                    "categoria": "hoy",
                    "local": equipo_local,
                    "visitante": equipo_visitante,
                    "marcador": "- / -",
                    "tiempo": "-",
                    "hora_inicio": "18:00",
                    "cuotas": {
                        "Bet365": {"1": 1.90, "X": 3.40, "2": 4.10}, # Aquí meterías más lógica de scraping para cuotas
                        "Betano": {"1": 1.95, "X": 3.30, "2": 4.00}
                    }
                }
                partidos.append(partido_info)
                
                # Para el ejemplo, solo traeremos los primeros 5 partidos
                if len(partidos) >= 5:
                    break
        else:
            print(f"Error de conexión: Código {respuesta.status_code}")
            
    except Exception as e:
        print(f"Ocurrió un error en el scraping: {e}")
    
    # Si el scraper falla o está vacío, devolvemos una lista vacía
    # O puedes poner tus datos simulados aquí abajo como "respaldo" si falla
    if not partidos:
        return [
            {
                "id": "1",
                "categoria": "en_vivo",
                "local": "Sporting Cristal (Simulado)",
                "visitante": "Universitario",
                "marcador": "1 - 0",
                "tiempo": "65'",
                "hora_inicio": "En vivo",
                "cuotas": {"Bet365": {"1": 1.85, "X": 3.40, "2": 4.20}}
            }
        ]
        
    return partidos