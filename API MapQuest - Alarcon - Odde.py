import urllib.parse
import requests

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "lk3JbbB4A9aVzcu24xhjSD1OV5NOimX5"

rendimiento_km_por_litro = 12.0 #se dejo asi porque no existe parametro de bencina

def convertir_tiempo(formatted_time):
    horas, minutos, segundos = map(int, formatted_time.split(':'))
    return f"{horas} horas, {minutos} minutos, {segundos} segundos"

while True:
    print("=============================================")
    orig = input("Ciudad de origen (o 'q' para salir): ")
    if orig.lower() == "q":
        print("¡Programa finalizado!")
        break

    dest = input("Ciudad de destino (o 'q' para salir): ")
    if dest.lower() == "q":
        print("¡Programa finalizado!")
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        distancia_km = json_data["route"]["distance"] * 1.61
        litros_estimados = distancia_km / rendimiento_km_por_litro

        print("API Status: 0 = Llamada exitosa.\n")
        print("=============================================")
        print(f"Dirección desde {orig} hasta {dest}")
        print(f"Duración del viaje: {convertir_tiempo(json_data['route']['formattedTime'])}")
        print(f"Distancia: {distancia_km:.2f} kilometros")
        print(f"Combustible estimado: {litros_estimados:.2f} litros (estimado a {rendimiento_km_por_litro:.1f} km/litro)")
        print("=============================================")
        print("Instrucciones:")
        for paso in json_data["route"]["legs"][0]["maneuvers"]:
            print(f"- {paso['narrative']} ({paso['distance']*1.61:.2f} km)")
        print("=============================================\n")
    elif json_status == 402:
        print("Error: Entrada inválida para una o ambas ciudades.\n")
    elif json_status == 611:
        print("Error: Falta información para la ciudad de origen o destino.\n")
    else:
        print(f"Error (Status Code: {json_status}). Consulta la documentación:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes\n")
