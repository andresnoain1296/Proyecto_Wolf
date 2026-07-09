import datetime
import pytz
import requests

LIMA_TZ = pytz.timezone('America/Lima')
# 🔑 REEMPLAZA ESTO CON LA CLAVE QUE TE LLEGUE A TU CORREO
API_KEY = "d06ef8db61b61e700b29b2a6d264aae0" 

def obtener_hora_lima():
    return datetime.datetime.now(LIMA_TZ)

def obtener_datos_reales_casas():
    ahora_lima = obtener_hora_lima()
    partidos = []

    # Consultamos partidos de las principales ligas (ej. fútbol global/peruano si está disponible)
    # The Odds API nos da cuotas de Bet365, Betano (en Latam), etc.
    url = f"https://api.the-odds-api.com/v4/sports/soccer/odds/?apiKey={API_KEY}&regions=eu,us&markets=h2h&bookmakers=bet365,betano"

    try:
        respuesta = requests.get(url, timeout=10)
        
        if respuesta.status_code == 200:
            datos_api = respuesta.json()
            
            for i, juego in enumerate(datos_api):
                # Convertir la hora del partido a la hora de Lima
                hora_utc = datetime.datetime.strptime(juego["commence_time"], "%Y-%m-%dT%H:%M:%SZ")
                hora_utc = pytz.utc.localize(hora_utc)
                hora_partido_lima = hora_utc.astimezone(LIMA_TZ)
                
                # Clasificar si el partido es Hoy o Mañana
                diferencia_dias = (hora_partido_lima.date() - ahora_lima.date()).days
                
                if diferencia_dias == 0:
                    categoria = "hoy"
                elif diferencia_dias == 1:
                    categoria = "manana"
                else:
                    continue # Si es para más adelante, lo ignoramos por ahora
                
                # Extraer las cuotas de las casas disponibles
                cuotas_estructuradas = {}
                for bookmaker in juego.get("bookmakers", []):
                    nombre_casa = bookmaker["title"] # Ej: "Bet365"
                    
                    # Buscar las cuotas de Local (1), Empate (X), Visita (2)
                    home_odds, draw_odds, away_odds = 1.0, 1.0, 1.0
                    market = bookmaker.get("markets", [{}])[0]
                    
                    for outcomes in market.get("outcomes", []):
                        if outcomes["name"] == juego["home_team"]:
                            home_odds = outcomes["price"]
                        elif outcomes["name"] == juego["away_team"]:
                            away_odds = outcomes["price"]
                        else:
                            draw_odds = outcomes["price"]
                            
                    cuotas_estructuradas[nombre_casa] = {
                        "1": home_odds,
                        "X": draw_odds,
                        "2": away_odds
                    }

                # Si la casa no ofreció cuotas, le ponemos unas por defecto para que no falle tu diseño
                if "Bet365" not in cuotas_estructuradas:
                    cuotas_estructuradas["Bet365"] = {"1": 1.0, "X": 1.0, "2": 1.0}
                if "Betano" not in cuotas_estructuradas:
                    cuotas_estructuradas["Betano"] = {"1": 1.0, "X": 1.0, "2": 1.0}

                partidos.append({
                    "id": str(i + 1),
                    "categoria": categoria,
                    "local": juego["home_team"],
                    "visitante": juego["away_team"],
                    "marcador": "- / -",
                    "tiempo": "-",
                    "hora_inicio": hora_partido_lima.strftime("%H:%M"),
                    "cuotas": cuotas_structured_final(cuotas_estructuradas)
                })
                
        else:
            print(f"Error API: {respuesta.status_code}")
            
    except Exception as e:
        print(f"Error conexión API: {e}")
        
    return partidos

def cuotas_structured_final(cuotas_existentes):
    # Asegura que las 6 columnas de tu interfaz siempre se muestren aunque la API solo traiga algunas
    todas_las_casas = ["Bet365", "Betano", "Betsson", "1xBet", "Inkabet", "Doradobet"]
    resultado = {}
    for casa in todas_las_casas:
        if casa in cuotas_existentes:
            resultado[casa] = cuotas_existentes[casa]
        else:
            # Si la API no tiene esa casa en ese instante, le pone 0.00 o una cuota base
            resultado[casa] = {"1": 1.00, "X": 1.00, "2": 1.00}
    return resultado