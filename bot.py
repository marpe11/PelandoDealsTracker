import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suprimir logs do TensorFlow

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

def main():
    # Configurações do navegador
    chrome_options = Options()
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--window-size=1920x1080')

    # Inicializar WebDriver
    service = Service(service_log_path=os.devnull)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Acessar o site
        driver.get("https://www.pelando.com.br/recentes")
        time.sleep(5)

        # Rolagem para carregar mais itens
        for _ in range(5):
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
            time.sleep(2)

        # Processar o conteúdo da página
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        items = soup.find_all('li', class_='sc-4af6a208-2')

        # Coletar dados
        novos_dados = []
        if items:
            for item in items:
                try:
                    nome = item.find('a', class_='sc-jMCldn').text.strip()
                    preco_texto = item.find('div', class_='sc-dxfTlo').text.strip()
                    
                    # Processar link
                    link = item.find('a', class_='sc-jMCldn')['href']
                    if not link.startswith('http'):
                        link = f"https://www.pelando.com.br{link}"
                    
                    # Processar preço
                    preco_limpo = re.sub(r'[^0-9,]', '', preco_texto).replace(',', '.')
                    preco = float(preco_limpo) if preco_limpo else 0.0
                    
                    novos_dados.append([nome, preco, link])
                except (AttributeError, KeyError):
                    continue
        else:
            print("Nenhum item encontrado na página.")
            return

    finally:
        driver.quit()

    # Gerenciar dados no Excel
    gerenciar_excel(novos_dados)

def gerenciar_excel(novos_dados):
    file_path = "ofertas_pelando.xlsx"
    colunas = ["Produto", "Valor", "Link"]

    # Criar DataFrame com novos dados
    new_df = pd.DataFrame(novos_dados, columns=colunas)

    if os.path.exists(file_path):
        existing_df = pd.read_excel(file_path)
        
        # Verificar IDs existentes
        if "ID" in existing_df.columns:
            ultimo_id = existing_df["ID"].max()
        else:
            existing_df["ID"] = []
            ultimo_id = 0
        
        # Filtrar novos produtos
        novos_produtos = new_df[~new_df["Produto"].isin(existing_df["Produto"])]
        
        if not novos_produtos.empty:
            # Inverter a ordem dos novos produtos
            novos_produtos = novos_produtos[::-1]
            
            # Adicionar IDs sequenciais
            novos_produtos.insert(0, "ID", range(ultimo_id + 1, ultimo_id + 1 + len(novos_produtos)))
            final_df = pd.concat([existing_df, novos_produtos], ignore_index=True)
            
            # Calcular número de novos registros
            num_novos_registros = len(final_df) - len(existing_df)
            print(f"🔎 Dados atualizados com sucesso! Novos registros adicionados: {num_novos_registros}")
        else:
            final_df = existing_df
            print("Nenhum novo produto encontrado para adicionar.")
    else:
        # Criar novo arquivo com IDs
        new_df.insert(0, "ID", range(1, len(new_df) + 1))
        final_df = new_df
        print(f"🔎 Arquivo criado com sucesso! Total de registros: {len(final_df)}")

    # Salvar arquivo
    final_df.to_excel(file_path, index=False)

if __name__ == "__main__":
    main()