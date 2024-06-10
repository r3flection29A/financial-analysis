# Documentação do Projeto Financial Analysis

## Índice

- [Introdução](#introdução)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Features do Aplicativo](#features-do-aplicativo)
  - [Análise Técnica](#análise-técnica)
  - [Retornos Mensais](#retornos-mensais)
  - [Análise Fundamentalista](#análise-fundamentalista)
  - [Investir](#investir)
  - [Mercado Agora](#mercado-agora)
- [TO DO](#to-do)

## Introdução

Este documento fornece uma visão geral e instruções sobre como rodar o aplicativo Streamlit chamado **Financial Analysis**. Este aplicativo permite a análise técnica e fundamentalista de ações, backtesting de estratégias de investimento, consulta de retornos mensais, e até mesmo a realização de investimentos através do MetaTrader.

## Pré-requisitos

Antes de rodar o projeto, certifique-se de que você tem os seguintes componentes instalados em sua máquina:

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## Instalação

1. **Clone o repositório do projeto:**

   ```bash
   git clone https://github.com/r3flection29A/financial-analysis.git
   cd financial-analysis
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3. **Instale as dependências do projeto:**

    ```bash
    pip install -r requirements.txt
    ```

## Como rodar o projeto

Para iniciar o aplicativo Streamlit, execute o seguinte comando no terminal dentro do diretório do projeto:
    ```bash  
    streamlit run app.py
    ```

Isso iniciará o servidor Streamlit e abrirá o aplicativo no seu navegador padrão, geralmente acessível via *localhost*.

## Features do Aplicativo

### Análise Técnica

A seção de Análise Técnica oferece diversos indicadores para análise de ações:

- RSI (Relative Strength Index): Mede a velocidade e a mudança dos movimentos de preço.
- POO (Price Oscillator): Um indicador de momentum.
- Backtest Simples: Permite a simulação de uma estratégia de investimento ao longo do tempo para avaliar sua performance.

### Retornos Mensais

Esta seção mostra os retornos mensais de uma ação ou índice selecionado. Você pode visualizar a performance histórica em uma tabela ou gráfico para analisar tendências e sazonalidades.

### Análise fundamentalista 

Na seção de Análise Fundamentalista, você pode consultar os principais indicadores financeiros de uma empresa, tais como:

- Dividendos: Histórico de pagamento de dividendos.
- Lucro: Lucro líquido anual.
- Dívida: Nível de endividamento da empresa.

### Investir 

A página Investir permite realizar investimentos diretamente através do MetaTrader, proporcionando uma interface integrada para facilitar suas operações no mercado financeiro.

### Mercado agora

Na seção Mercado Agora, você tem acesso a informações em tempo real ou em intervalos específicos sobre o mercado, incluindo índices e ações. Esta seção é ideal para monitorar o desempenho e tomar decisões informadas rapidamente.

## TO DO

- [ ] Adicionar indice de cointegração
- [ ] Adicionar mais indices na tela 'Mercado agora'
- [ ] Backtest completo

#### Feito por João Pedro Roldan, Matheus Martins Gomes, Tiago Floriano de Lima e Thiago Furtado Lima
