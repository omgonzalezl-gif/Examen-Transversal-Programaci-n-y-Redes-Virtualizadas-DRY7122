import requests
import urllib.parse

GEOCODE_URL = "https://graphhopper.com/api/1/geocode?"
ROUTE_URL = "https://graphhopper.com/api/1/route?"

API_KEY = "3aae1af3-3c50-41ab-af43-d5e2b086bd3c"


def geocoding(ciudad, pais):
    ciudad_completa = ciudad + ", " + pais

    url = GEOCODE_URL + urllib.parse.urlencode({
        "q": ciudad_completa,
        "limit": "1",
        "key": API_KEY
    })

    respuesta = requests.get(url)
    datos = respuesta.json()

    if respuesta.status_code == 200 and len(datos["hits"]) > 0:
        lat = datos["hits"][0]["point"]["lat"]
        lng = datos["hits"][0]["point"]["lng"]
        nombre = datos["hits"][0]["name"]

        return True, lat, lng, nombre
    else:
        return False, None, None, ciudad_completa


while True:
    print("\n======================================")
    print(" Calculadora de viaje Chile - Argentina")
    print("======================================")
    print("Para salir, escriba la letra s")

    origen = input("\nCiudad de Origen en Chile: ")

    if origen.lower() == "s":
        print("Programa finalizado.")
        break

    destino = input("Ciudad de Destino en Argentina: ")

    if destino.lower() == "s":
        print("Programa finalizado.")
        break

    print("\nSeleccione el medio de transporte:")
    print("1. Auto")
    print("2. Bicicleta")
    print("3. Caminando")

    opcion = input("Ingrese una opción: ")

    if opcion.lower() == "s":
        print("Programa finalizado.")
        break
    elif opcion == "1":
        vehiculo = "car"
        transporte = "Auto"
    elif opcion == "2":
        vehiculo = "bike"
        transporte = "Bicicleta"
    elif opcion == "3":
        vehiculo = "foot"
        transporte = "Caminando"
    else:
        print("Opción inválida. Intente nuevamente.")
        continue

    origen_geo = geocoding(origen, "Chile")
    destino_geo = geocoding(destino, "Argentina")

    if origen_geo[0] and destino_geo[0]:
        punto_origen = str(origen_geo[1]) + "," + str(origen_geo[2])
        punto_destino = str(destino_geo[1]) + "," + str(destino_geo[2])

        url_ruta = ROUTE_URL + urllib.parse.urlencode({
            "point": [punto_origen, punto_destino],
            "vehicle": vehiculo,
            "locale": "es",
            "key": API_KEY
        }, doseq=True)

        respuesta_ruta = requests.get(url_ruta)
        datos_ruta = respuesta_ruta.json()

        if respuesta_ruta.status_code == 200:
            distancia_km = datos_ruta["paths"][0]["distance"] / 1000
            distancia_millas = distancia_km / 1.60934

            tiempo_ms = datos_ruta["paths"][0]["time"]
            segundos = int(tiempo_ms / 1000 % 60)
            minutos = int(tiempo_ms / 1000 / 60 % 60)
            horas = int(tiempo_ms / 1000 / 60 / 60)

            print("\n======================================")
            print(" Resultado del viaje")
            print("======================================")
            print(f"Ciudad de Origen: {origen_geo[3]}, Chile")
            print(f"Ciudad de Destino: {destino_geo[3]}, Argentina")
            print(f"Medio de transporte: {transporte}")
            print(f"Distancia en kilómetros: {distancia_km:.2f} km")
            print(f"Distancia en millas: {distancia_millas:.2f} mi")
            print(f"Duración del viaje: {horas:02d}:{minutos:02d}:{segundos:02d}")

            print("\n======================================")
            print(" Narrativa del viaje")
            print("======================================")

            for instruccion in datos_ruta["paths"][0]["instructions"]:
                texto = instruccion["text"]
                distancia = instruccion["distance"] / 1000
                millas = distancia / 1.60934

                print(f"- {texto} ({distancia:.2f} km / {millas:.2f} mi)")

            print("======================================")

        else:
            print("No se pudo calcular la ruta.")
            print("Mensaje de error:", datos_ruta.get("message", "Error desconocido"))

    else:
        print("No se pudo encontrar la ciudad de origen o destino.")
