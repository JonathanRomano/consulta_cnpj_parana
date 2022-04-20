from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class Scraping_browser(webdriver.Firefox):
    def dados_dos_socios(self, cnpj):
        
        self.get('http://www.empresafacil.pr.gov.br/acoes/certidao')

        WebDriverWait(self, 40).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="botao-certidao-simplificada-open"]')))

        self.find_element(by=By.XPATH, value='//*[@id="botao-certidao-simplificada-open"]').click()

        WebDriverWait(self, 40).until(
        EC.presence_of_element_located((By.ID, "consulta-previa")))

        self.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_nireMatriz"]').clear()
        self.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_razaoSocial"]').clear()

        input_cnpj = self.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_cnpj"]')
        input_cnpj.clear()
        
        for num in cnpj:
            if num.isdigit():
                input_cnpj.send_keys(num)
        
        time.sleep(5)
        self.find_element(by=By.XPATH, value='/html/body/div[1]/main/div[2]/div/div[1]/form/div[6]/div/div/div/span/input').click()
        self.find_element(by=By.XPATH, value='//*[@id="botao-avancar"]').click()
        
        WebDriverWait(self, 40).until(
        EC.presence_of_element_located((By.ID, "avancar-coleta-dados")))

        button_list = self.find_elements(by=By.CLASS_NAME, value='title')
        
        lista_de_socios = []
        for button in button_list:
            lista_de_socios.append(button.text)
            button.click()
        
        time.sleep(2)
        
        return {
            'dados_brutos': self.find_element(by=By.CLASS_NAME, value='row').text,
            'lista_de_nomes': lista_de_socios
        }
    
scraping_browser = Scraping_browser

def sanitizar_dados(dados, lista_de_nomes):

    dados, dados_gerais = dados.split('Dados dos Sócios/Representantes ou Administradores')[1], dados.split('Dados dos Sócios/Representantes ou Administradores')[0]

    dados_gerais = dados_gerais.split('Identificação')[1]
    dados_gerais = dados_gerais.split('Endereço e Contato')[0]

    dados = dados.split('INFORMAÇÕES FORNECIDAS APENAS PARA CONFERÊNCIA. NÃO POSSUEM VALOR LEGAL')[0]
    
    dados_gerais = dados_gerais.split('\n')
    lista_de_dados_gerais = []

    while dados_gerais != []:
        if len(dados_gerais) > 1:
            item_atual = dados_gerais[0]
            prox_item = dados_gerais[1]

            if item_atual.endswith(':') and prox_item.endswith(':') or item_atual.endswith(':') and prox_item == '':
                lista_de_dados_gerais.append(
                    {
                        'type': item_atual.replace(':',''),
                        'value': 'não consta'
                    }
                )
            
            elif item_atual.endswith(':') and not prox_item.endswith(':'):
                lista_de_dados_gerais.append(
                    {
                        'type': item_atual.replace(':',''),
                        'value': prox_item
                    }
                )

            dados_gerais.pop(0)

        else:

            item_atual = dados_gerais[0]

            if item_atual.endswith(':'):
                lista_de_dados_gerais.append(
                    {
                        'type': item_atual,
                        'value': 'não consta'
                    }
                )
            
            dados_gerais.pop(0)


    lista_de_dados = []

    for nome in lista_de_nomes:
        if nome == lista_de_nomes[len(lista_de_nomes)-1]:
            dados_divididos = dados.split(nome)
            lista_de_dados.append(dados_divididos[0])
            lista_de_dados.append(dados_divididos[1])
            
        else:
            dados_divididos = dados.split(nome)
            lista_de_dados.append(dados_divididos[0])

            if len(dados_divididos) == 2:
                dados = dados_divididos[1]

            else:
                new_data_string = ''
                for parte in dados_divididos[1:len(dados_divididos)]:
                    new_data_string += parte
                
                dados = new_data_string

    if lista_de_dados[0] == '\n':
        lista_de_dados.pop(0)

    lista_de_socios = []
    for index in range(0,len(lista_de_nomes)-1):
        object_socio = {}
        object_socio['name'] = lista_de_nomes[index]

        data_list = []
        dados_do_socio = lista_de_dados[index].split('\n')
        
        while dados_do_socio != []:
            if len(dados_do_socio) > 1:
                
                item_atual = dados_do_socio[0]
                prox_item = dados_do_socio[1]

                if item_atual.endswith(':') and prox_item.endswith(':') or item_atual.endswith(':') and prox_item == '':
                    data_list.append(
                        {
                            'type': item_atual.replace(':',''),
                            'value': 'não consta'
                        }
                    )
                
                elif item_atual.endswith(':') and not prox_item.endswith(':'):
                    data_list.append(
                        {
                            'type': item_atual.replace(':',''),
                            'value': prox_item
                        }
                    )

                dados_do_socio.pop(0)

            else:

                item_atual = dados_do_socio[0]

                if item_atual.endswith(':'):
                    data_list.append(
                        {
                            'type': item_atual,
                            'value': 'não consta'
                        }
                    )
                
                dados_do_socio.pop(0)
        
        object_socio['data'] = data_list

        lista_de_socios.append(object_socio)
    
    return {
        'dados gerais': lista_de_dados_gerais,
        'socios': lista_de_socios
    }