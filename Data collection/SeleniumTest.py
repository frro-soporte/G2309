from selenium import webdriver
from chromedriver_py import binary_path # this will get you the path variable
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd

website = 'https://www.adamchoi.co.uk/teamgoals/detailed'

svc = webdriver.ChromeService(executable_path=binary_path)

driver = webdriver.Chrome(service=svc)

driver.get(website)


boton_all_matches = driver.find_element(By.XPATH, '//*[@id="page-wrapper"]/div/home-away-selector/div/div/div/div/label[2]')
boton_all_matches.click()
lista_paises = Select(driver.find_element(By.ID, 'country'))
lista_paises.select_by_visible_text('Argentina')
partidos = driver.find_elements(By.TAG_NAME, 'tr')

lista_partidos = []
for i in range(len(partidos)):
    lista_partidos.append(partidos[i].text)
driver.quit()

#Pandas
df = pd.DataFrame({'partidos':lista_partidos})
print(df)
df.to_csv('LigaArg.csv', index = False )
