from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource
import ast

from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

from src.server.instance import server

app, api = server.app, server.api

@api.route('/empresaFacil')
class empresaFacil(Resource):
    def post(self):
        byte_str = request.data
        dict_str = byte_str.decode("UTF-8")
        
        body = ast.literal_eval(dict_str)

        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

        x = body['x']

        driver.get('https://www.jonathanromano.online/')

        input('teste >>')

        y = driver.find_element_by_xpath('/html/body/div/div/main/div[1]/h1').text
        
        driver.close()

        if x == y:
            teste = True
            
        else:
            teste = False

        return make_response({'result':teste}, 200)