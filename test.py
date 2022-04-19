from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager



driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

input('enter apra continuar')

driver.get('https://sso.acesso.gov.br/')

driver.find_element_by_xpath('/html/body/div[1]/main/form/div/div[5]/a').click()

print(driver.get_cookies())

input('<< enter para encerrar >>')

print(driver.get_cookies())

driver.close()