# 🏠 **Web Scraping do Quinto Andar**

Este projeto consiste em uma série de scripts Python para coletar dados de imóveis disponíveis para aluguel no site [Quinto Andar](https://www.quintoandar.com.br). O processo é dividido em três etapas principais:

1. **Coleta de Cidades por UF**: Extrai a lista de cidades atendidas pelo Quinto Andar, organizadas por estado (UF).
2. **Coleta de Bairros por Cidade**: Para cada cidade, coleta os bairros disponíveis.
3. **Coleta de Imóveis por Bairro**: Para cada bairro, coleta os imóveis disponíveis para aluguel.

## 📂 **Estrutura do Projeto**

O projeto é composto por três scripts principais:

- **`scraping_quintoandar_uf_cidade.py`**: Coleta as cidades atendidas pelo Quinto Andar, organizadas por estado (UF), e salva os dados em um arquivo CSV.
- **`scraping_quintoandar_bairros.py`**: Para cada cidade, coleta os bairros disponíveis e salva os dados em um arquivo CSV.
- **`scraping_quintoandar_alugueis.py`**: Para cada bairro, coleta os imóveis disponíveis para aluguel e salva os dados em um arquivo CSV.

## 🛠️ **Como Executar o Projeto**

### Pré-requisitos

- Python 3.x instalado.
- Bibliotecas Python necessárias: `selenium`, `requests`, `csv`, `re`, `concurrent.futures`.
- ChromeDriver instalado e configurado no PATH (para o Selenium).

### Instalação das Dependências

Você pode instalar as dependências necessárias usando o `pip`:

```bash
pip install -r requirements.txt
```

### **Executando os Scripts**
#### Coleta de Cidades por UF:

Execute o script scraping_quintoandar_uf_cidade.py para coletar as cidades por UF.
Este script gerará um arquivo CSV chamado quintoandar_uf_cidade.csv com as cidades e seus respectivos links.

```bash
python scraping_quintoandar_uf_cidade.py
```

#### Coleta de Bairros por Cidade:

Com o arquivo quintoandar_uf_cidade.csv gerado, execute o script scraping_quintoandar_bairros.py para coletar os bairros de cada cidade. 
Este script gerará um arquivo CSV chamado quintoandar_bairros.csv com os bairros e seus respectivos links.

```bash
python scraping_quintoandar_bairros.py
```

#### Coleta de Imóveis por Bairro:

Com o arquivo quintoandar_bairros.csv gerado, execute o script scraping_quintoandar_alugueis.py para coletar os imóveis disponíveis para aluguel em cada bairro. Este script gerará um arquivo CSV chamado quintoandar_alugueis.csv com os detalhes dos imóveis.

```bash
python scraping_quintoandar_alugueis.py
```

## **📊 Estrutura dos Arquivos CSV**

Parte dos arquivos CSV gerados (truncados) estão disponíveis em /Exemplos_csv/

```
quintoandar_uf_cidade.csv
```

Este arquivo contém a lista de cidades atendidas pelo Quinto Andar, organizadas por estado (UF).

| UF  | Cidade        | Link_Cidade                             |
|-----|-------------|---------------------------------------|
| RJ  | Rio de Janeiro | https://www.quintoandar.com.br/regioes-atendidas/rio-de-janeiro-rj-brasil-rdy6u9x7k1 |

```
quintoandar_bairros.csv
```

Este arquivo contém a lista de bairros atendidos pelo Quinto Andar, organizados por estado (UF) e cidade.

| UF  | Cidade         | Bairro | Link_Cidade | Link_Bairro |
|-----|--------------|--------|-------------|-------------|
| RJ  | Rio De Janeiro | Tijuca | https://www.quintoandar.com.br/regioes-atendidas/rio-de-janeiro-rj-brasil-rdy6u9x7k1 | https://www.quintoandar.com.br/alugar/imovel/tijuca-rio-de-janeiro-rj-brasil |



```
quintoandar_alugueis.csv
```

Este arquivo contém a lista de imóveis disponíveis no Quinto Andar, com detalhes sobre localização, preço e características.

| UF  | city           | slug                                 | id        | type        | area | bathrooms | bedrooms | parkingSpaces | totalCost | rent | iptuPlusCondominium | salePrice | address               | regionName  | forRent | forSale | isFurnished | Link |
|-----|--------------|--------------------------------------|----------|------------|------|-----------|----------|--------------|-----------|------|-------------------|----------|----------------------|------------|--------|--------|-------------|------|
| RJ  | Rio de Janeiro | tijuca-rio-de-janeiro-rj-brasil    | 893990375 | Apartamento | 82   | 2         | 2        | 1            | 4747      | 3400 | 1215              | 420000   | Rua Ângelo Bitencourt | Vila Isabel | True   | True   | False       | https://www.quintoandar.com.br/imovel/893990375 |

## **📝 Considerações Finais**

**Limitações:** O projeto depende da estrutura do site do Quinto Andar, que pode mudar ao longo do tempo. Se houver alterações significativas no site, os scripts podem precisar de ajustes.

**Responsabilidade:** Este projeto é apenas para fins educacionais. Certifique-se de respeitar os termos de uso do site e não sobrecarregar os servidores com requisições excessivas.
