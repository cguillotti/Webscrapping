# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 12:42:18 2022

@author: Compumar
"""

from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
ruta = ChromeDriverManager(path = './chromedriver').install()
s = Service(ruta)
driver = webdriver.Chrome(service = s)

