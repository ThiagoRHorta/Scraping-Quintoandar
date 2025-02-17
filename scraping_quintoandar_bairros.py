import re
import csv
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def configurar_driver():
    options = Options()
    options.add_argument("--headless")  # Modo headless para rodar mais rápido
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Reduz a verbosidade do Selenium
    return webdriver.Chrome(options=options)

def processar_cidade(linha):
    driver = configurar_driver()
    uf, cidade, link_cidade = linha['UF'], linha['Cidade'], linha['Link_Cidade']
    resultados = []
    
    print(f"\nProcessando cidade: {cidade} ({uf})")
    driver.get(link_cidade)
    
    try:
        letters_container = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.NeighborhoodList__LettersWrapper-sc-1agyhqr-0"))
        )
    except Exception as e:
        print(f"Erro ao carregar letras de {cidade}: {e}")
        driver.quit()
        return []
    
    letter_buttons = letters_container.find_elements(By.TAG_NAME, "button")
    
    for idx in range(len(letter_buttons)):
        try:
            letters_container = driver.find_element(By.CSS_SELECTOR, "div.NeighborhoodList__LettersWrapper-sc-1agyhqr-0")
            letter_buttons = letters_container.find_elements(By.TAG_NAME, "button")
            btn = letter_buttons[idx]
            letra = btn.text.strip()
            
            print(f"Clicando na letra: {letra}")
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
            driver.execute_script("arguments[0].click();", btn)
            
            neighborhoods_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.NeighborhoodList__NeighborhoodsWrapper-sc-1agyhqr-1"))
            )
            
            links_bairros = neighborhoods_container.find_elements(By.TAG_NAME, "a")
            
            for link in links_bairros:
                href = link.get_attribute("href")
                bairro = link.text.strip()
                novo_link_bairro = re.sub(r"(-brasil).*", r"\1", href.replace("regioes-atendidas", "alugar/imovel"))
                resultados.append([uf, cidade, bairro, link_cidade, novo_link_bairro])
                print(f"  - Bairro: {bairro} | Novo Link: {novo_link_bairro}")
        except Exception as e:
            print(f"Erro ao processar bairros de {cidade}: {e}")
            continue
    
    driver.quit()
    return resultados

# Processamento Paralelo
def main():
    with open('quintoandar_uf_cidade.csv', newline='', encoding='utf-8') as csv_in, \
         open('quintoandar_bairros.csv', 'w', newline='', encoding='utf-8') as csv_out:
        
        leitor = csv.DictReader(csv_in)
        writer = csv.writer(csv_out, quoting=csv.QUOTE_ALL)
        writer.writerow(['UF', 'Cidade', 'Bairro', 'Link_Cidade', 'Link_Bairro'])
        
        with ThreadPoolExecutor(max_workers=5) as executor:  # 5 threads paralelas
            resultados_futuros = executor.map(processar_cidade, leitor)
            
            for resultado in resultados_futuros:
                writer.writerows(resultado)
    
    # os.remove('quintoandar_uf_cidade.csv')

if __name__ == "__main__":
    main()
