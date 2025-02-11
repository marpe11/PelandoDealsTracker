
# 🚀 PelandoDealsTracker

**Automated Web Scraper for Tracking Real-Time Deals from Pelando.com.br**  
*Salve promoções, preços e links em um arquivo Excel organizado!*

---

## 📌 Visão Geral

Este script Python automatiza a extração das últimas promoções do [Pelando.com.br](https://www.pelando.com.br), usando **Selenium** e **BeautifulSoup** para coleta de dados. Os resultados são salvos em um arquivo Excel (`ofertas_pelando.xlsx`), evitando duplicatas e mantendo registros sequenciais com IDs. Ideal para caçadores de promoções, desenvolvedores ou entusiastas de dados!

---

## ✨ Funcionalidades

- **Modo Invisível**: Execução em segundo plano sem abrir o navegador.
- **Rolagem Dinâmica**: Carrega mais ofertas simulando rolagem do usuário.
- **Gerenciamento Inteligente no Excel**:
  - Cria colunas: `ID`, `Produto`, `Valor`, `Link`.
  - Filtra duplicatas e adiciona novas entradas em ordem cronológica.
  - Converte preços para formato numérico (ex: `R$ 999,99` → `999.99`).
- **Tolerante a Erros**: Ignora dados faltantes e suprime logs desnecessários.
- **Leve**: Baixo consumo de recursos e dependências mínimas.

---

## ⚙️ Instalação

1. **Pré-requisitos**:
   - Python 3.8+
   - Navegador Chrome instalado.

2. **Instale as dependências**:
   ```bash
   pip install selenium beautifulsoup4 pandas openpyxl webdriver-manager
   ```

3. **Clone o repositório**:
   ```bash
   git clone https://github.com/seu-usuario/PelandoDealsTracker.git
   cd PelandoDealsTracker
   ```

---

## 🖥️ Como Usar

1. **Execute o script**:
   ```bash
   python main.py
   ```

2. **Resultado**:
   - Um arquivo `ofertas_pelando.xlsx` será criado/atualizado.
   - Novos registros aparecerão no terminal (ex: `🔎 Dados atualizados! Novos registros: 5`).

---

## 🔧 Personalização

Ajuste o script modificando:
- **Número de rolagens**: Mude `range(5)` em `main()` para carregar mais ofertas.
- **Caminho do Excel**: Altere `file_path` em `gerenciar_excel()`.
- **Logs**: Controle logs do Selenium com `TF_CPP_MIN_LOG_LEVEL`.

---


## 🙌 Créditos

- Desenvolvido com [Selenium](https://selenium.dev), [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) e [Pandas](https://pandas.pydata.org).
- Inspirado pela necessidade de monitorar promoções automaticamente. 😉




