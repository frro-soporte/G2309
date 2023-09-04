import requests
from lxml import html

# URL de la página web
url = 'https://www.dolarhoy.com/'

# Realizar una solicitud HTTP a la página web
response = requests.get(url)

# Verificar que la solicitud sea exitosa (código de estado 200)
if response.status_code == 200:
    # Crear un objeto HTML a partir del contenido de la página web
    pagina_web = html.fromstring(response.text)

    # Utilizar XPath para encontrar elementos en la página
    elemento = pagina_web.xpath('/html/body/div[3]/div[2]/div[1]/div[1]/div[2]/section/div/div/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]')
    # Utilizar XPath para encontrar el botón
    boton = pagina_web.xpath('//*[@id="header_dolar"]/div/div/div/div[1]/button')[0]

    # Hacer clic en el botón
    boton.click()
    if elemento:
        # Imprimir el texto del elemento encontrado
        texto_elemento = elemento[0].text_content()
        print(texto_elemento)
    else:
        print('Elemento no encontrado.')
else:
    print('No se pudo acceder a la página web.')
