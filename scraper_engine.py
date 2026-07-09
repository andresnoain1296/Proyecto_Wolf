import datetime
import pytz

# Configurar Zona Horaria de Lima-Perú
LIMA_TZ = pytz.timezone('America/Lima')

def obtener_hora_lima():
    return datetime.datetime.now(LIMA_TZ)

def simular_datos_casas():
    """
    Estructura de datos ideal que tus scrapers/APIs deben llenar.
    Nota: Para producción, aquí conectarás tus scripts de Playwright o APIs.
    """
    ahora_lima = obtener_hora_lima()
    
    # Formatear fechas de ejemplo
    hoy_formato = ahora_lima.strftime("%Y-%m-%d")
    manana_formato = (ahora_lima + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    partidos = [
        {
            "id": "1",
            "categoria": "en_vivo",  # en_vivo, hoy, manana
            "local": "Sporting Cristal",
            "visitante": "Universitario",
            "marcador": "1 - 0",
            "tiempo": "65'",
            "hora_inicio": "En vivo",
            "cuotas": {
                "Bet365": {"1": 1.85, "X": 3.40, "2": 4.20},
                "Betano": {"1": 1.90, "X": 3.30, "2": 4.10},
                "Betsson": {"1": 1.83, "X": 3.50, "2": 4.30},
                "1xBet": {"1": 1.95, "X": 3.45, "2": 4.25},
                "Inkabet": {"1": 1.80, "X": 3.30, "2": 4.00},
                "Doradobet": {"1": 1.85, "X": 3.40, "2": 4.15}
            }
        },
        {
            "id": "2",
            "categoria": "hoy",
            "local": "Real Madrid",
            "visitante": "Barcelona",
            "marcador": "- / -",
            "tiempo": "-",
            "hora_inicio": "16:00",  # Hora ya convertida a Lima
            "cuotas": {
                "Bet365": {"1": 2.10, "X": 3.60, "2": 3.20},
                "Betano": {"1": 2.15, "X": 3.55, "2": 3.15},
                "Betsson": {"1": 2.08, "X": 3.65, "2": 3.25},
                "1xBet": {"1": 2.20, "X": 3.70, "2": 3.30},
                "Inkabet": {"1": 2.05, "X": 3.50, "2": 3.10},
                "Doradobet": {"1": 2.12, "X": 3.55, "2": 3.18}
            }
        },
        {
            "id": "3",
            "categoria": "manana",
            "local": "Manchester City",
            "visitante": "Liverpool",
            "marcador": "- / -",
            "tiempo": "-",
            "hora_inicio": "14:30",
            "cuotas": {
                "Bet365": {"1": 1.95, "X": 3.80, "2": 3.60},
                "Betano": {"1": 2.00, "X": 3.75, "2": 3.50},
                "Betsson": {"1": 1.93, "X": 3.85, "2": 3.65},
                "1xBet": {"1": 2.05, "X": 3.90, "2": 3.70},
                "Inkabet": {"1": 1.90, "X": 3.70, "2": 3.45},
                "Doradobet": {"1": 1.97, "X": 3.75, "2": 3.55}
            }
        }
    ]
    return partidos