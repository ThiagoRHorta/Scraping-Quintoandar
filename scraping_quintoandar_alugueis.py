import requests
import csv
import time

# URL da API
url = "https://apigw.prod.quintoandar.com.br/cached/house-listing-search/v1/search/list"

# Arquivo de entrada (com cidades e slugs)
input_csv = "quintoandar_bairros.csv"

# Arquivo de saída (com imóveis)
output_csv = "quintoandar_alugueis.csv"

# Função para extrair corretamente o slug do link
def extract_slug(link):
    # Encontra a parte do slug antes de "-brasil"
    slug = link.split("/")[-1].split("-brasil")[0] + "-brasil"
    return slug.strip()  # Remove espaços extras


# Abrir o CSV de entrada e processar cada cidade
with open(input_csv, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    # Criar CSV de saída com os campos desejados
    with open(output_csv, mode="w", newline='', encoding='utf-8') as outputfile:
        fieldnames = ["UF", "city", "slug", "id", "type", "area", "bathrooms", "bedrooms",
              "parkingSpaces", "totalCost", "rent", "iptuPlusCondominium", "salePrice",
              "address", "regionName", "forRent", "forSale", "isFurnished", "Link"]
        writer = csv.DictWriter(outputfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()  # Escrever cabeçalho no CSV

        for row in reader:
            uf = row["UF"].strip()
            city = row["Cidade"].strip()
            slug = extract_slug(row["Link_Bairro"])
            print(f"🔎 Buscando imóveis para: {city} ({uf}) - {slug}...")

            offset = 0
            total_results = 0

            while True:
                # Corpo da requisição POST com paginação dinâmica
                post_body = {
                    "context": {
                        "mapShowing": True,
                        "listShowing": True,
                        "userId": "Air3W0rFILNzStFfBOri-wxBQVQk6wJ5NyZNS9vrt3vmPvKcMCYOLQ",
                        "deviceId": "Air3W0rFILNzStFfBOri-wxBQVQk6wJ5NyZNS9vrt3vmPvKcMCYOLQ",
                        "isSSR": False
                    },
                    "filters": {
                        "businessContext": "RENT",  # Pode ser "SALE" para venda
                        "location": {
                            "countryCode": "BR"
                        }
                    },
                    "sorting": {
                        "criteria": "RELEVANCE",
                        "order": "DESC"
                    },
                    "pagination": {
                        "pageSize": 5000,
                        "offset": offset
                    },
                    "slug": slug,
                    "fields": [
                        "id", "type", "area", "bathrooms", "bedrooms", "parkingSpaces",
                        "totalCost", "rent", "iptuPlusCondominium", "salePrice",
                        "address", "city", "regionName", "forRent", "forSale", "isFurnished"
                    ]
                }

                headers = {
                    "Content-Type": "application/json"
                }

                try:
                    # Fazer a requisição POST
                    response = requests.post(url, json=post_body, headers=headers)
                    
                    if response.status_code == 200:
                        data = response.json()

                        if "hits" in data and "hits" in data["hits"]:
                            hits = data["hits"]["hits"]
                            
                            if not hits:
                                break  # Para quando não houver mais resultados

                            for item in hits:
                                imóvel = item["_source"]
                                writer.writerow({
                                    "UF": uf,
                                    "city": imóvel.get("city", "").strip(),
                                    "slug": slug,
                                    "id": imóvel.get("id"),
                                    "type": imóvel.get("type", "").strip(),
                                    "area": imóvel.get("area"),
                                    "bathrooms": imóvel.get("bathrooms"),
                                    "bedrooms": imóvel.get("bedrooms"),
                                    "parkingSpaces": imóvel.get("parkingSpaces"),
                                    "totalCost": imóvel.get("totalCost"),
                                    "rent": imóvel.get("rent"),
                                    "iptuPlusCondominium": imóvel.get("iptuPlusCondominium"),
                                    "salePrice": imóvel.get("salePrice"),
                                    "address": imóvel.get("address", "").strip(),
                                    "regionName": imóvel.get("regionName", "").strip(),
                                    "forRent": imóvel.get("forRent"),
                                    "forSale": imóvel.get("forSale"),
                                    "isFurnished": imóvel.get("isFurnished"),
                                    "Link": f"https://www.quintoandar.com.br/imovel/{imóvel.get('id')}"
                                })


                            total_results += len(hits)
                            offset += 5000  # Avança para a próxima página
                        else:
                            break  # Para quando não houver mais imóveis

                    else:
                        print(f"❌ Erro {response.status_code} para {slug}: {response.text}")
                        break  # Sai do loop em caso de erro

                    time.sleep(1)  # Evitar sobrecarga na API

                except Exception as e:
                    print(f"Erro ao buscar {slug}: {e}")
                    break  # Sai do loop em caso de erro crítico

            print(f"✔ {total_results} imóveis coletados para {city} ({uf})\n")

print(f"✅ Extração concluída! Resultados salvos em '{output_csv}'.")
