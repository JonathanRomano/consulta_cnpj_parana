from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By


driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

driver.get('https://www.empresafacil.pr.gov.br/')

cookie_list = [
    {'name': '_gat', 'value': '1', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650318979, 'sameSite': 'None'},
    {'name': 'voxtecnologia-consent-cookie', 'value': 'MQ==', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681854920, 'sameSite': 'None'},
    {'name': 'voxtecnologia-initial-message', 'value': 'IjA2LzA0LzIwMjIi', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1651614921, 'sameSite': 'None'},
    {'name': 'sigfacil', 'value': 'f6401f840ad4b780ef81e63361c461aa', 'path': '/', 'domain': 'www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': True, 'sameSite': 'None'},
    {'name': 'hgyclh-w7930', 'value': '9fa8eb2cfa2839b6ff99e6340d1c9de4', 'path': '/', 'domain': '.www.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1681854933, 'sameSite': 'None'},
    {'name': '_ga', 'value': 'GA1.4.1176697986.1650318920', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1713390933, 'sameSite': 'None'},
    {'name': '_gid', 'value': 'GA1.4.469418369.1650318920', 'path': '/', 'domain': '.empresafacil.pr.gov.br', 'secure': False, 'httpOnly': False, 'expiry': 1650405333, 'sameSite': 'None'}
]

for cookie in cookie_list:
    driver.add_cookie(cookie)

driver.get('https://www.empresafacil.pr.gov.br/s/consultaprevia/')

driver.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_nireMatriz"]').clear()
driver.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_cnpj"]').clear()
driver.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_razaoSocial"]').clear()

cnpj = '78.413.325/0017-50'
for num in cnpj:
    if num.isdigit():
        driver.find_element(by=By.XPATH, value='//*[@id="solicitacao_empresas_0_cnpj"]').send_keys(num)

driver.find_element(by=By.XPATH, value='/html/body/div[1]/main/div[2]/div/div[1]/form/div[6]/div/div/div/span/input').click()

driver.find_element(by=By.XPATH, value='//*[@id="botao-avancar"]').click()

input('<< enter para encerrar >>')

driver.close()