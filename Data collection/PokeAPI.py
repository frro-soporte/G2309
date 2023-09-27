import requests

# URL base de la PokeAPI
base_url = "https://pokeapi.co/api/v2/"

# Nombre del Pokémon que queremos consultar
pokemon_nombre = "pikachu"
pokemon_numero = ''

# Construimos la URL completa para obtener información sobre el Pokémon
url = f"{base_url}pokemon/{pokemon_nombre}"

# Realizamos una solicitud GET a la URL
response = requests.get(url)

# Verificamos si la solicitud fue exitosa (código de estado 200)
if response.status_code == 200:
    # Convertimos la respuesta JSON en un diccionario de Python
    data = response.json()

    # Extraemos información relevante
    nombre = data['name']
    altura = data['height']
    peso = data['weight']
    tipos = str([tipo['type']['name'] for tipo in data['types']])



    # Imprimimos la información
    print(f"Nombre del Pokémon: {nombre}")
    print(f"Altura: {altura} decímetros")
    print(f"Peso: {peso} hectogramos")
    print("Tipo: ", tipos.replace("[", " ").replace("]",""))
else:
    print(f"No se pudo obtener información del Pokémon {pokemon_nombre}. Código de estado: {response.status_code}")
