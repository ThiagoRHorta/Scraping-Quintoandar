from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re

def configurar_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")  # Reduz a verbosidade do Selenium
    return webdriver.Chrome(options=options)

def main():
    driver = configurar_driver()
    driver.get("https://www.quintoandar.com.br/regioes-atendidas")

    file_name = "quintoandar_uf_cidade.csv"
    wait = WebDriverWait(driver, 10)
    regions = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "Accordion__AccordionContentWrapper-sc-151pp2r-1")))

    data = []

    for region in regions:
        try:
            cities = region.find_elements(By.CSS_SELECTOR, "a.Cozy__Link.Cozy__Link-SelectedLink._8AKcf-.pez1Ml.urVUpf")
            for city in cities:
                city_link = city.get_attribute("href")
                match = re.search(r"quintoandar\.com\.br/regioes-atendidas/([a-z\-]+)-([a-z]{2})-brasil", city_link)
                if match:
                    cidade = match.group(1).replace("-", " ").title()
                    uf = match.group(2).upper()
                    data.append([uf, cidade, city_link])
        except Exception as e:
            print(f"Erro processando: {e}")

    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["UF", "Cidade", "Link_Cidade"])
        writer.writerows(data)

    driver.quit()
    print(f"Dados salvos em {file_name}")

if __name__ == "__main__":
    main()
