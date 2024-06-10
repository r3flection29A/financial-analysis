import streamlit as st
import seaborn as sns
from datetime import date

import ta
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import yfinance as yf
import pandas as pd
import fundamentus as fd
import MetaTrader5 as mt5

dict_intervals = {
    '1 minuto (Intraday)': '1m',
    '2 minutos': '2m',
    '5 minutos': '5m',
    '15 minutos': '15m',
    '30 minutos': '30m',
    '1 hora': '1h',
    '1 dia': '1d',
    '5 dias': '5d',
    '1 semana': '1wk',
    '1 mês': '1mo',
    '3 meses': '3mo'
}

dict_periods = {
    '1 dia': '1d',
    '5 dias': '5d',
    '1 mês': '1mo',
    '3 meses': '3mo',
    '6 meses': '6mo',
    '1 ano': '1y',
    '2 anos': '2y',
    '5 anos': '5y',
    '10 anos': '10y',
    'Ano até a data': 'ytd',
    'Máximo': 'max'
}

def home_page():
    st.title('Página Inicial')  
    st.markdown('---')    
    st.header('Veja e controle análises de ações em um lugar só!')  
    st.write('Criado por Tiago Floriano de Lima, João Pedro Roldan da Silva, Matheus Martins Gomes e Thiago Furtado Lima')

def now_market_page():
    st.title('Mercado agora')
    st.text('Por enquanto apenas aceitamos ações estrangeiras')

    st.markdown(date.today().strftime('%d/%m/%Y'))
    col1, col2 = st.columns(2)

    with col1:
        start = st.date_input("Você gostaria de especificar uma data de início?", value=None)
        end = st.date_input("Você gostaria de especificar uma data de fim?", value=None)
        interval = st.selectbox('Escolha o intervalo de tempo', list(dict_intervals.keys()))
        interval_value = dict_intervals[interval] # type: ignore
        period = st.selectbox('Escolha o período de tempo', list(dict_periods.keys()))
        period_value = dict_periods[period] # type: ignore

    with col2:
        option_text = st.text_input('Digite a ação ou índice que quer ver 👇')
        with st.spinner('Baixando cotações...'):
            if option_text:
                try:
                    if start is None or end is None:
                        data = yf.download(tickers=option_text, interval=interval_value, period=period_value)
                    else:
                        data = yf.download(option_text, start=start, end=end, interval=interval_value)
                    data = pd.DataFrame(data)
                except Exception:
                    st.error(f'Ação ou índice não encontrados! Verifique se está digitando corretamente!', icon="🚨")
    
    if len(option_text) == 0 or data.empty:
        st.warning('Nenhum dado foi encontrado para os parâmetros fornecidos!')
    else:
        st.write(f'## {option_text.upper()} gráficos')
        st.line_chart(data['Close'])

        # Plot usando matplotlib
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Close'))            
        fig.update_layout(title=f'{option_text.upper()} Preço de Fechamento',
                                      xaxis_title='Data',
                                      yaxis_title='Preço de Fechamento (USD)',
                                      height=600, width=1200)
        fig.update_layout(xaxis_rangeslider_visible=False)
        st.plotly_chart(fig)

    st.markdown('---')

    st.subheader('Indíces no momento')

    lista_indices = ['IBOV', 'S&P500', 'NASDAQ']

    indice = st.selectbox('Selecione o Índice', lista_indices)

    if indice == 'IBOV':
        indice_diario = yf.download('^BVSP', period='1d', interval='5m')
    if indice == 'S&P500':
        indice_diario = yf.download('^GSPC', period='1d', interval='5m')
    if indice == 'NASDAQ':
        indice_diario = yf.download('^IXIC', period='1d', interval='5m')

    fig = go.Figure(data=[go.Candlestick(x=indice_diario.index,
                        open=indice_diario['Open'],
                        high=indice_diario['High'],
                        low=indice_diario['Low'],
                        close=indice_diario['Close'])])
    fig.update_layout(title=indice, xaxis_rangeslider_visible=False)

    st.plotly_chart(fig)


def actions_by_return():
    st.title('Analise os retornos mensais das ações aqui')

    col1, _ = st.columns(2)
    with col1:
        start = st.date_input("Você gostaria de especificar uma data de início?", value=None)            
        end = st.date_input("Você gostaria de especificar uma data de fim?", value=None)

    # Escolha entre Indices e Ações
    opcao = st.radio('Selecione', ['Indices', 'Ações'])

    # Campos específicos para cada opção
    if opcao == 'Indices':
        ticker = st.selectbox('Indice', ['BOVESPA', 'S&P 500 Financials', 'NASDAQ'])
        option_text = None
    elif opcao == 'Ações':
        ticker = None
        option_text = st.text_input('Digite a ação ou índice que quer ver 👇')

    # Botão de submissão do formulário
    analisar = st.button('Analisar')

    if analisar:
        retornos = None
        if opcao == 'Indices':
            if ticker == 'BOVESPA':
                retornos = yf.download('^BVSP', start=start, end=end)
            elif ticker == 'S&P 500 Financials':
                retornos = yf.download('^SP500-40', start=start, end=end)
            elif ticker == 'NASDAQ':
                retornos = yf.download('^IXIC', start=start, end=end)
        elif opcao == 'Ações':
            if len(option_text) == 0:
                st.warning('Nenhum dado foi encontrado para os parâmetros fornecidos!')
            else:
                retornos = yf.download(option_text, start=start, end=end)
        
        if retornos is not None and not retornos.empty:
           # Separar e agrupar os anos e meses
            retorno_mensal = retornos.groupby([retornos.index.year.rename('Year'), retornos.index.month.rename('Month')]).mean()
            # Criar matrix de retornos
            tabela_retornos = pd.DataFrame(retorno_mensal)
            tabela_retornos = pd.pivot_table(tabela_retornos, values='Close', index='Year', columns='Month')
            tabela_retornos.columns = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

            # Heatmap Interativo
            fig = px.imshow(tabela_retornos, 
                            labels=dict(x="Mês", y="Ano", color="Retorno Médio"),
                            x=tabela_retornos.columns, 
                            y=tabela_retornos.index, 
                            color_continuous_scale='RdYlGn',
                            title=f'Heatmap de Retornos Médios Mensais - {ticker if opcao == "Indices" else option_text}')
            fig.update_layout(margin=dict(l=0, r=0, t=50, b=100), annotations=[
                dict(
                    text="Quanto mais verde, maior o retorno médio<br>Quanto mais vermelho, menor o retorno médio",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=-0.35,
                    font=dict(size=12),
                    align="center"
                )
            ])
            st.plotly_chart(fig)

            # Criação do dataframe de Estatísticas dos Retornos Mensais
            stats = pd.DataFrame(tabela_retornos.mean(), columns=['Média'])
            stats['Mediana'] = tabela_retornos.median()
            stats['Maior'] = tabela_retornos.max()
            stats['Menor'] = tabela_retornos.min()
            stats['Positivos'] = tabela_retornos.gt(0).sum()/tabela_retornos.count()
            stats['Negativos'] = tabela_retornos.le(0).sum()/tabela_retornos.count()

            # Preparação dos dados para plotagem
            stats_a = stats[['Média', 'Mediana', 'Maior', 'Menor']].transpose()
            fig_a = px.imshow(stats_a, 
                              labels=dict(x="Mês", y="Métrica", color="Valor"),
                              x=stats_a.columns, 
                              y=stats_a.index, 
                              color_continuous_scale='RdYlGn',
                              title='Estatísticas dos Retornos Mensais')
            fig_a.update_layout(margin=dict(l=0, r=0, t=50, b=100), annotations=[
                dict(
                    text="Média: Retorno médio mensal<br>Mediana: Retorno no meio da distribuição<br>Maior: Maior retorno mensal<br>Menor: Menor retorno mensal",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=-0.25,
                    font=dict(size=12),
                    align="center"
                )
            ])
            st.plotly_chart(fig_a)

            stats_b = stats[['Positivos', 'Negativos']].transpose()
            fig_b = px.imshow(stats_b, 
                              labels=dict(x="Mês", y="Métrica", color="Percentual"),
                              x=stats_b.columns, 
                              y=stats_b.index,
                              title='Percentual de Meses Positivos e Negativos')
            fig_b.update_layout(margin=dict(l=0, r=0, t=50, b=100), annotations=[
                dict(
                    text="Positivos: Percentual de meses com retorno positivo<br>Negativos: Percentual de meses com retorno negativo",
                    showarrow=False,
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=-0.05,
                    font=dict(size=12),
                    align="center"
                )
            ])
            st.plotly_chart(fig_b)
        else:
            st.warning('Nenhum dado foi encontrado para os parâmetros fornecidos!')


def invest_page():
    st.title('Investir (MetaTrader)')
    st.write('Nesta página, você pode fazer negociações usando o MetaTrader.')

    # Campo de entrada para a chave de API
    api_key = st.text_input('Chave de API do MetaTrader', type='password')

    # Verifica se a chave de API é válida no MetaTrader5
    if api_key:
        # Tenta se conectar ao MetaTrader5 com a chave de API fornecida
        if not mt5.initialize():
            st.error('Falha ao conectar ao MetaTrader5. Verifique se a plataforma está aberta e tente novamente.')
            return
        
        if not mt5.login(login='', server='', password=api_key):
            st.error('Chave de API inválida. Verifique suas credenciais e tente novamente.')
            mt5.shutdown()
            return

        st.success('Chave de API válida. Você pode enviar ordens agora.')
        mt5.shutdown()

    # Campos de entrada para os detalhes da negociação
    with st.form(key='invest_form'):
        st.header('Detalhes da Negociação')
        pair = st.text_input('Ticker da Ação (ex: AAPL para Apple Inc.)', max_chars=6)
        volume = st.number_input('Volume da Negociação', min_value=1, step=1)
        trade_type = st.selectbox('Tipo de Negociação', ['Compra', 'Venda'])

        submit_button = st.form_submit_button(label='Enviar Ordem')

    if submit_button:
        if not mt5.initialize():
            st.error('Falha ao conectar ao MetaTrader5. Verifique se a plataforma está aberta e tente novamente.')
            return

        # Autenticação com a chave de API
        if not mt5.login(login='', server='', password=api_key):
            st.error('Falha na autenticação com a chave de API. Verifique suas credenciais e tente novamente.')
            mt5.shutdown()
            return

        # Define o tipo de negociação
        action = mt5.ORDER_TYPE_BUY if trade_type == 'Compra' else mt5.ORDER_TYPE_SELL

        # Envia a ordem
        request = {
            "action": action,
            "symbol": pair,
            "volume": volume,
            "type": mt5.ORDER_TYPE_MARKET,
            "price": 0,
            "sl": 0,
            "tp": 0,
            "deviation": 0,
            "magic": 0,
            "comment": "Ordem de negociação enviada via Streamlit"
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            st.error(f'Falha ao enviar a ordem: {result.comment}')
        else:
            st.success(f'Ordem de {trade_type} de {volume} lotes de {pair} enviada com sucesso para o MetaTrader5.')

        # Desconecta do MetaTrader5
        mt5.shutdown()


def analysis_page():
    st.title('Análise Técnica de Ações')

    # Escolha das datas
    col1, _ = st.columns(2)
    with col1:
        start = st.date_input("Data de início", value=pd.to_datetime("2020-01-01"))            
        end = st.date_input("Data de fim", value=pd.to_datetime("today"))

    # Campo de texto para inserir o ticker
    ticker = st.text_input('Digite o nome do índice ou ação que quer ver 👇')

    # Botão de submissão do formulário
    analisar = st.button('Analisar')

    if analisar:
        data = yf.download(ticker, start=start, end=end)
        
        if data is not None and not data.empty:
            # RSI
            data['RSI'] = ta.momentum.RSIIndicator(data['Close']).rsi()

            # MACD
            macd = ta.trend.MACD(data['Close'])
            data['MACD'] = macd.macd()
            data['Signal Line'] = macd.macd_signal()
            data['MACD Hist'] = macd.macd_diff()

            # Bollinger Bands
            bb = ta.volatility.BollingerBands(data['Close'])
            data['BB_High'] = bb.bollinger_hband()
            data['BB_Low'] = bb.bollinger_lband()

            # Moving Averages
            data['SMA50'] = data['Close'].rolling(window=50).mean()
            data['SMA200'] = data['Close'].rolling(window=200).mean()
            data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()

            # Volume
            data['Volume'] = data['Volume']

            # Backtest Simples (Estratégia de Cruzamento de Médias Móveis)
            data['Position'] = np.where(data['SMA50'] > data['SMA200'], 1, -1)
            data['Strategy Returns'] = data['Position'].shift(1) * data['Close'].pct_change()

            # Calcular os retornos cumulativos da estratégia
            data['Cumulative Market Returns'] = (1 + data['Close'].pct_change()).cumprod()
            data['Cumulative Strategy Returns'] = (1 + data['Strategy Returns']).cumprod()

            # Suporte e Resistência
            data['Support'] = data['Low'].rolling(window=20).min()
            data['Resistance'] = data['High'].rolling(window=20).max()

            # Oscilador Estocástico
            stoch = ta.momentum.StochasticOscillator(data['High'], data['Low'], data['Close'])
            data['%K'] = stoch.stoch()
            data['%D'] = stoch.stoch_signal()

            # Average True Range (ATR)
            data['ATR'] = ta.volatility.AverageTrueRange(data['High'], data['Low'], data['Close']).average_true_range()

            # Insights de Investimento
            insight = ""
            last_close = data['Close'].iloc[-1]
            last_rsi = data['RSI'].iloc[-1]
            last_macd = data['MACD'].iloc[-1]
            last_signal_line = data['Signal Line'].iloc[-1]
            last_stoch_k = data['%K'].iloc[-1]
            last_stoch_d = data['%D'].iloc[-1]

            if last_rsi > 70:
                insight += "RSI está acima de 70, sugerindo que o ativo está sobrecomprado. "
                st.write(insight)
            elif last_rsi < 30:
                insight += "RSI está abaixo de 30, sugerindo que o ativo está sobrevendido. "
                st.write(insight)

            if last_macd > last_signal_line:
                insight += "Sinal de compra do MACD. "
                st.write(insight)

            elif last_macd < last_signal_line:
                insight += "Sinal de venda do MACD. "
                st.write(insight)

            if last_stoch_k > last_stoch_d and last_stoch_k > 80:
                insight += "Oscilador Estocástico indica sobrecompra. "
                st.write(insight)

            elif last_stoch_k < last_stoch_d and last_stoch_k < 20:
                insight += "Oscilador Estocástico indica sobrevenda. "
                st.write(insight)

            if insight == "":
                insight = "Não há insights de investimento claros com base nos indicadores analisados."
                st.write(insight)

            # Plotting
            fig = make_subplots(rows=5, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.3, 0.3, 0.3, 0.3, 0.1])

            # Price Plot
            fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Preço de Fechamento'), row=1, col=1)

            # RSI Plot
            fig.add_trace(go.Scatter(x=data.index, y=data['RSI'], mode='lines', name='RSI'), row=2, col=1)
            fig.add_hline(y=70, line=dict(color='red', dash='dash'), row=2, col=1)
            fig.add_hline(y=30, line=dict(color='green', dash='dash'), row=2, col=1)

            # MACD Plot
            fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], mode='lines', name='MACD'), row=3, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['Signal Line'], mode='lines', name='Linha de Sinal'), row=3, col=1)
            fig.add_trace(go.Bar(x=data.index, y=data['MACD Hist'], name='Histograma MACD'), row=3, col=1)

            # Bollinger Bands Plot
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_High'], mode='lines', name='Banda Superior Bollinger', line=dict(color='red', dash='dash')), row=4, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['BB_Low'], mode='lines', name='Banda Inferior Bollinger', line=dict(color='green', dash='dash')), row=4, col=1)

            # Backtest Plot
            fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative Market Returns'], mode='lines', name='Retorno Acumulado do Mercado'), row=5, col=1)
            fig.add_trace(go.Scatter(x=data.index, y=data['Cumulative Strategy Returns'], mode='lines', name='Retorno Acumulado da Estratégia'), row=5, col=1)

            # Layout
            fig.update_layout(title='Análise Técnica e Backtest', template='plotly_white', height=1000)

            st.plotly_chart(fig)
        else:
            st.warning('Nenhum dado foi encontrado para os parâmetros fornecidos!')

def papers():
    st.title('Informações fundamentalistas')

    lista_tickers = fd.list_papel_all()

    comparar = st.checkbox('Comparar 2 ativos')

    col1, col2 = st.columns(2)

    with col1:
        with st.expander('Ativo 1', expanded=True):
            papel1 = st.selectbox('Selecione o Papel', lista_tickers)
            info_papel1 = fd.get_detalhes_papel(papel1)
            st.write('**Empresa:**', info_papel1['Empresa'][0])
            st.write('**Setor:**', info_papel1['Setor'][0])
            st.write('**Subsetor:**', info_papel1['Subsetor'][0])
            st.write('**Valor de Mercado:**',f"R$ {info_papel1['Valor_de_mercado'][0]:,.2f}")
            st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel1['Patrim_Liq'][0]):,.2f}")
            st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel1['Receita_Liquida_12m'][0]):,.2f}")
            st.write('**Dívida Bruta:**', f"R$ {float(info_papel1['Div_Bruta'][0]):,.2f}")
            st.write('**Dívida Líquida:**', f"R$ {float(info_papel1['Div_Liquida'][0]):,.2f}")
            st.write('**P/L:**', f"{float(info_papel1['PL'][0]):,.2f}")
            st.write('**Dividend Yield:**', f"{info_papel1['Div_Yield'][0]}")

    if comparar:
        with col2:
            with st.expander('Ativo 2', expanded=True):
                papel2 = st.selectbox('Selecione o 2º Papel', lista_tickers)
                info_papel2 = fd.get_detalhes_papel(papel2)
                st.write('**Empresa:**', info_papel2['Empresa'][0])
                st.write('**Setor:**', info_papel2['Setor'][0])
                st.write('**Subsetor:**', info_papel2['Subsetor'][0])
                st.write('**Valor de Mercado:**',f"R$ {info_papel2['Valor_de_mercado'][0]:,.2f}")
                st.write('**Patrimônio Líquido:**', f"R$ {float(info_papel2['Patrim_Liq'][0]):,.2f}")
                st.write('**Receita Liq. 12m:**', f"R$ {float(info_papel2['Receita_Liquida_12m'][0]):,.2f}")
                st.write('**Dívida Bruta:**', f"R$ {float(info_papel2['Div_Bruta'][0]):,.2f}")
                st.write('**Dívida Líquida:**', f"R$ {float(info_papel2['Div_Liquida'][0]):,.2f}")
                st.write('**P/L:**', f"{float(info_papel2['PL'][0]):,.2f}")
                st.write('**Dividend Yield:**', f"{info_papel2['Div_Yield'][0]}")     


def main():
    
    st.sidebar.image(r'assets/logo.png')
    st.sidebar.title('Financial Analysis')
    st.sidebar.markdown('---')

    choices = ['Home', 'Mercado Agora', 
               'Investir (MetaTrader)', 
               'Retornos',
               'Análise Técnica','Análise Fundamentalista']
    choice = st.sidebar.radio("Páginas", choices)

    if choice == 'Home':
        home_page()

    if choice == 'Mercado Agora':
        now_market_page()

    if choice == 'Retornos':
        actions_by_return()

    if choice == 'Investir (MetaTrader)':
        invest_page()
    
    if choice ==  'Análise Técnica':
        analysis_page()

    if choice == 'Análise Fundamentalista':
        papers()

    return choice

if __name__ == '__main__':
    main()
