from selenium import webdriver 
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

# Solicita ao usuário a busca que deseja realizar
search = input('Digite sua Busca: ')

# Função para ler as credenciais de um arquivo
def read_credentials(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()

        credentials = {}
        # Percorre cada linha do arquivo e armazena chave e valor no dicionário de credenciais
        for line in lines:
            key, value = line.strip().split(":")
            credentials[key] = value
        return credentials

# Caminho para o arquivo de credenciais
file_path_credentials = "Caminho do arquivo credentials.txt"
# Lê as credenciais do arquivo
credentials = read_credentials(file_path_credentials)

# Inicia o navegador Chrome
browser = webdriver.Chrome() 
# Acessa a página inicial do LinkedIn
browser.get('https://www.linkedin.com')
time.sleep(2)  # Aguarda o carregamento da página

# Acessa o botão de login e clica nele
btn_entrar_email = browser.find_element(By.CSS_SELECTOR, '#main-content > section.section.min-h-68.flex-nowrap.pt-6.babybear\:flex-col.babybear\:min-h-0.babybear\:px-mobile-container-padding.babybear\:pt-3 > div > div > a')
btn_entrar_email.click()

# Localiza os campos de e-mail e senha e o botão de login
email = browser.find_element(By.XPATH, '//*[@id="username"]')
senha = browser.find_element(By.XPATH, '//*[@id="password"]')
btn_enter = browser.find_element(By.CSS_SELECTOR, '#organic-div > form > div.login__form_action_container > button')

time.sleep(2)  # Aguarda um pouco para garantir que os elementos estejam visíveis

# Insere as credenciais e envia o formulário de login
email.send_keys(credentials['user'])
senha.send_keys(credentials['senha'])
time.sleep(2)
btn_enter.click()
time.sleep(5)  # Aguarda o login ser concluído e a página carregar

# Localiza o campo de busca e insere o texto da busca fornecido pelo usuário
input_jobs_search = browser.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
time.sleep(5)
input_jobs_search.send_keys(search)
time.sleep(5)
input_jobs_search.send_keys(Keys.ENTER)
time.sleep(5)  # Aguarda os resultados da busca serem carregados

# Localiza o botão de filtro e clica nele para refinar a busca
vagas_button = browser.find_element(By.CSS_SELECTOR, '#search-reusables__filters-bar > ul > li:nth-child(1) > button')
time.sleep(5)
vagas_button.click()
time.sleep(3)  # Aguarda o filtro ser aplicado

# Função para rolar para baixo na página
def scrool_list(pixels):
    # Rola o elemento especificado para baixo pelo número de pixels fornecido
    browser.execute_script(f"arguments[0].scrollTop+={pixels};", browser.find_element(By.CSS_SELECTOR, '#main > div > div.scaffold-layout__list-detail-inner.scaffold-layout__list-detail-inner--grow > div.scaffold-layout__list > div'))
    time.sleep(2)  # Aguarda o conteúdo ser carregado

# Lista para armazenar os links encontrados
links = []

# Rola a página para baixo e coleta os links das vagas
for _ in range(25):  # Ajuste o número de iterações conforme necessário
    scrool_list(200)
    # Encontra todos os links das vagas
    links = browser.find_elements(By.XPATH, "//main//div/div//ul//li//a[@data-control-id]")
    print(len(links))
    # Se o número de links encontrado for suficiente, sai do loop
    if len(links) >= 25:
        print(f"Chegamos ao numero esperado de {len(links)}")
        break

# Cria uma nova planilha Excel
planilha = Workbook()
sheet = planilha.active

# Define os cabeçalhos das colunas
sheet['A1'] = 'Nome da Vaga'
sheet['B1'] = 'Link da Vaga'

# Inicializa a linha onde os dados serão escritos
next_line = sheet.max_row + 1

# Adiciona os dados das vagas à planilha
for link in links:
    text = link.text
    url_link = link.get_attribute('href')

    sheet[f"A{next_line}"] = text
    sheet[f"B{next_line}"] = url_link

    next_line += 1

# Salva a planilha com o nome baseado na busca realizada
planilha.save('Vagas_Links_' + search + ".xlsx")
print("Planilha criada com Sucesso!!!")
print("Encerrando a Busca...")

# Aguarda um pouco antes de fechar o navegador
time.sleep(2)
browser.quit()
