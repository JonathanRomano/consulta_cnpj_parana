from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource
from webdriver_manager.firefox import GeckoDriverManager
import ast

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import os

os.system('export PATH=$PATH:/app/vendor/geckodriver/geckodriver')

from src.server.instance import server

cookie_list = [
    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650318979, 'sameSite': 'None'},
    {'name': 'voxtecnologia-consent-cookie', 'value': 'MQ==', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681854920, 'sameSite': 'None'},
    {'name': 'voxtecnologia-initial-message', 'value': 'IjA2LzA0LzIwMjIi', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1651614921, 'sameSite': 'None'},
    {'name': 'sigfacil', 'value': 'f6401f840ad4b780ef81e63361c461aa', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'},
    {'name': 'hgyclh-w7930', 'value': '9fa8eb2cfa2839b6ff99e6340d1c9de4', 'path': '/', 'domain': '.www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681854933, 'sameSite': 'None'},
    {'name': '_ga', 'value': 'GA1.4.1176697986.1650318920', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1713390933, 'sameSite': 'None'},
    {'name': '_gid', 'value': 'GA1.4.469418369.1650318920', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650405333, 'sameSite': 'None'}
]

app, api = server.app, server.api

@api.route('/empresaFacil')
class empresaFacil(Resource):
    def post(self):
        byte_str = request.data
        dict_str = byte_str.decode("UTF-8")
        
        body = ast.literal_eval(dict_str)

        #driver = webdriver.Firefox(executable_path='./geckodriver')
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        x = body['x']

        driver.get('https://www.jonathanromano.online/')

        y = driver.find_element_by_xpath('/html/body/div/div/main/div[1]/h1').text
        
        driver.close()

        if x == y:
            teste = True
            
        else:
            teste = False

        return make_response({'result':teste}, 200)