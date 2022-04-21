from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource
import ast

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from src.components.browser import scraping_browser, sanitizar_dados

import os

geckodriver_path=os.environ.get("GECKODRIVER_PATH")
firefox_binary_path=os.environ.get("FIREFOX_BINARY_PATH")

from src.server.instance import server

cookie_list = [{'name': 'sigfacil', 'value': 'c30b3f2fe128ef689c9865d4c5f4d48b', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'}, {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650462838, 'sameSite': 'None'}, {'name': 'hgyclh-w7930', 'value': '128e5c25b487acebbc13590f010b5cef', 'path': '/', 'domain': '.www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681998779, 'sameSite': 'None'}, {'name': '_ga', 'value': 'GA1.4.1481603954.1650462779', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1713534780, 'sameSite': 'None'}, {'name': '_gid', 'value': 'GA1.4.12661647.1650462779', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650549180, 'sameSite': 'None'}, {'name': 'voxtecnologia-consent-cookie', 'value': 'MQ==', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681998784, 'sameSite': 'None'}, {'name': 'voxtecnologia-initial-message', 'value': 'IjA2LzA0LzIwMjIi', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1651758785, 'sameSite': 'None'}]

app, api = server.app, server.api

@api.route('/empresaFacil')
class empresaFacil(Resource):
    def post(self):
        byte_str = request.data
        dict_str = byte_str.decode("UTF-8")
        
        body = ast.literal_eval(dict_str)

        # definição do driver #
        
        opts = FirefoxOptions()
        opts.add_argument("--headless")

        binary = FirefoxBinary()

        driver = scraping_browser(
            firefox_binary=binary,
            executable_path=geckodriver_path,
            firefox_options=opts
        )
        
        # definição do driver #

        try:
            driver.get('https://www.empresafacil.pr.gov.br/')

            for cookie in cookie_list:
                driver.add_cookie(cookie)

            dados_brutos = driver.dados_dos_socios(body['cnpj'])

            driver.close()

            resultado = sanitizar_dados(dados_brutos['dados_brutos'],dados_brutos['lista_de_nomes'])

            return make_response(resultado, 200)

        except Exception as error:
            resultado = {'erro': str(error)}
            driver.close()

            return make_response(resultado, 500)
