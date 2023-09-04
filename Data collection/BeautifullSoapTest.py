import requests
from bs4 import BeautifulSoup
#Scrapear valor del Dolar Blue Hoy, y mostrar la diferencia entre compra y venta
# URL de la página de DolarHoy
url = 'https://www.dolarhoy.com/'

# Realizar una solicitud HTTP a la página web
response = requests.get(url)

# Verificar que la solicitud sea exitosa (código de estado 200)
if response.status_code == 200:
    # Parsear el contenido de la página web con BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar el precio del dólar blue compra
    dolar_Compra_element = soup.find('div', class_='compra')
    precio_dolar_compra = dolar_Compra_element.find('div', class_='val').text.strip()

    #Encontrar el precio del dólar blue venta
    dolar_Venta_element = soup.find('div', class_='venta')
    precio_dolar_venta= dolar_Venta_element.find('div', class_='val').text.strip()

    #Calcular la diferencia entre el dólar blue compra y el dólar blue venta
    diferencia = (int(precio_dolar_venta[1:]) - int(precio_dolar_compra[1:]))

    # Imprimir los resultados
    print(f'Precio del dólar blue compra: {precio_dolar_compra}')
    print(f'Precio del dólar blue venta: {precio_dolar_venta}')
    print(f'Diferencia: {diferencia}')
else:
    print('No se pudo acceder a la página web.')