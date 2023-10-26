from selenium import webdriver
from chromedriver_py import binary_path #this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
from datetime import datetime

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

svc = webdriver.ChromeService(executable_path=binary_path)

driver = webdriver.Chrome(service=svc)

driver.get(website)


boton_all_matches = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/home-away-selector/div/div/div/div/label[2]')
boton_all_matches.click()
time.sleep(5)
lista_paises = Select(driver.find_element(By.ID, 'country'))
lista_paises.select_by_visible_text('Argentina')

time.sleep(5)
partidos = driver.find_elements(By.TAG_NAME, 'tr')

"""
partidos_por_equipo = []
nombre_equipo = 'Banfield'

for i in range(len(partidos)):
    texto_partido = partidos[i].text
    # Comprueba si el nombre del equipo está presente en la fila
    if nombre_equipo in texto_partido:
        partidos_por_equipo.append(texto_partido)

partidos_por_equipo = list(set(partidos_por_equipo))
df = pd.DataFrame({'partidos': partidos_por_equipo})
print(df)
"""

lista_partidos = []
for i in range(len(partidos)):
    lista_partidos.append(partidos[i].text)
driver.quit()

lista_partidos = list(set(lista_partidos))
#<<<<<<< HEAD
#Función para convertir una cadena de fecha en un objeto de fecha
#=======
# Función para convertir una cadena de fecha en un objeto de fecha
#>>>>>>> 9f541b3756097b9d9955e84548d9c1a4d5c2af57
def convertir_a_fecha(cadena):
    partes = cadena.split(" ")[0].split("-")
    dia = int(partes[0])
    mes = int(partes[1])
    anio = int(partes[2])
    return datetime(anio, mes, dia)

#<<<<<<< HEAD
#Ordena la lista utilizando la función convertir_a_fecha como clave
#=======
# Ordena la lista utilizando la función convertir_a_fecha como clave
#>>>>>>> 9f541b3756097b9d9955e84548d9c1a4d5c2af57
lista_partidos = sorted(lista_partidos, key=convertir_a_fecha)
#Pandas
df = pd.DataFrame({'partidos':lista_partidos})
print(df)
df.to_csv('LigaArg.csv', index=False)