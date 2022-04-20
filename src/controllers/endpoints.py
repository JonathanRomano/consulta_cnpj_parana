from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource
import ast

from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver import FirefoxOptions
from src.components.browser import scraping_browser, sanitizar_dados

from src.server.instance import server

cookie_list = [{'name': 'sigfacil', 'value': 'b0a8df3981b5530586771c67d9ac4487', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'voxtecnologia-consent-cookie', 'value': 'MQ==', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681929887, 'sameSite': 'None'}, {'name': 'hgyclh-w7930', 'value': 'c748be75066377af71a4f878a95246f0', 'path': '/', 'domain': '.www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681929888, 'sameSite': 'None'}, {'name': 'voxtecnologia-initial-message', 'value': 'IjA2LzA0LzIwMjIi', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1651689892, 'sameSite': 'None'}, {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650393953, 'sameSite': 'None'}, {'name': '_ga', 'value': 'GA1.4.600446254.1650393894', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1713465897, 'sameSite': 'None'}, {'name': '_gid', 'value': 'GA1.4.1772386436.1650393894', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650480297, 'sameSite': 'None'}]

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

        binary = FirefoxBinary('/app/vendor/firefox/firefox')
        geckodriver_path = '/app/vendor/geckodriver/geckodriver'

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
