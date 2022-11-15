# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 23:31:51 2022

@author: Compumar
"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import math
import time
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json
from lista_urls import listado_urls

def iniciar_chrome():
    ruta = ChromeDriverManager(path = './chromedriver').install()
    #opciones de crhome
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-notifications")
    options.add_argument("--ignore-cetificate-errors")
    options.add_argument("--disable-notifications")
    options.add_argument("--no-sandbox")
    options.add_argument("--log-level=3")
    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--no-first-run")
    options.add_argument("--no-proxy-server")
    options.add_argument("--disable-blink-features=AutomationControlled")
    exp_opt = [
        'enable-automation',
        'ignore-certificate-errors',
        'enable-logging']
    options.add_experimental_option("excludeSwitches",exp_opt)
    prefs = {
        "profile.default_content_setting_values.notifications":2,
         "intl.accept_languages":["es-ES","es"]}
    options.add_experimental_option("prefs",prefs)
    s = Service(ruta)
    driver = webdriver.Chrome(service=s, options=options)
    return driver

productos_jumbo = []
precios_jumbo = []
marcas_jumbo = []
id_jumbo = []
categoria_jumbo = []


def descargar_datos_jumbo():

    print("Buscando precios en lacteos/leches")
    nProductos = int(driver.find_element(By.CSS_SELECTOR,"span.amount").text.split(" ",1)[0])
    
    total_loops = math.ceil((float(nProductos)/18))
    for i in range(total_loops):
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
        time.sleep(3)
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    nombres_productos = soup.find_all('h2', class_='product-item__name')
    precios_productos = soup.find_all('span', class_='product-prices__value product-prices__value--best-price')
    marca_productos = soup.find_all('div', class_='product-item__brand')
    id_productos = soup.find_all('div', class_='product-item__data--sku')
    nombre_categoria = soup.find('h1',class_ = 'category-name__text').text
    
    
    for n in range(nProductos):
        categoria_jumbo.append(nombre_categoria)
    
    for nombre in nombres_productos:
        producto = str(nombre.find('a', class_='product-item__name').text)
        productos_jumbo.append(producto)

    for nombre_marca in marca_productos:
        marcas_jumbo.append(nombre_marca.text)

    for precio in precios_productos:
        precios_jumbo.append(float((precio.text.split('$',1)[1]).replace(',','.')))
    
    for id_ in id_productos:
        elemento = (id_.find('li',class_="-").text)
        convertedDict = json.loads(elemento)
        for j in convertedDict.values():
            id_jumbo.append(j['ref_id'])
    
   
if __name__ == '__main__':
    
    driver = iniciar_chrome()
    
    for direccion in listado_urls:
        url = 'https://www.jumbo.com.ar/' + direccion 
        driver.get(url)
        descargar_datos_jumbo()
        time.sleep(5)
    ListaDePrecios = list(zip(id_jumbo,categoria_jumbo,marcas_jumbo,productos_jumbo,precios_jumbo))
    dflp = pd.DataFrame(ListaDePrecios, columns = ['id','categoria','marca','producto','precio'] )   
    dflp['Fecha'] = datetime.today().date()
    driver.quit()
    
        

    

