from joblib import Parallel, delayed
from binance import Client
import pandas as pd
import time
import os
from datetime import datetime, timedelta

def formatar_par(par):

    par_formatado = ''.join(filter(str.isalnum, par)).upper()
    if "USD" in par_formatado:
        par_formatado += "T"
    if "UNI7083" in par_formatado:
        par_formatado = par_formatado.replace("7083", "")
    return par_formatado

def obter_dados(par):
    try:
        data_final = datetime.now()
        data_inicial = data_final - timedelta(days=720)
        klines = client.get_klines(symbol=par, interval=Client.KLINE_INTERVAL_1DAY, startTime=int(data_inicial.timestamp()) * 1000)
        return par, klines
    except Exception as e:
        print(f"Erro ao obter dados para {par}: {e}")
        return par, None

def processar_dados(pares_moedas, directory='./ConsumoApiBinance/Dados_CSV_Pares'):
    frames = Parallel(n_jobs=-1)(delayed(obter_dados)(par) for par in pares_moedas)

    dados_ohlc = {par: klines for par, klines in frames if klines is not None}

    for par, ohlc_data in dados_ohlc.items():
        if ohlc_data is not None:
            df = pd.DataFrame(ohlc_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
            df['timestamp'] = pd.to_datetime(df['timestamp'] / 1000, unit='s') 
            df.set_index('timestamp', inplace=True)  
            
            csv_filename = f'dados_{par}.csv'
            csv_filename = os.path.join(directory, csv_filename)
            df.to_csv(csv_filename)
            print(f"Arquivo CSV gerado com sucesso para o par {par}: {csv_filename}")

    print("Todos os arquivos CSV foram gerados com sucesso.")

if __name__ == '__main__':
    key = './Variaveis/Api_Key.txt'
    secret = './Variaveis/Secret_Key.txt'

    with open(key, 'r') as file:
        api_key = file.read().strip()
    with open(secret, 'r') as file:
        api_secret = file.read().strip()

    client = Client(api_key, api_secret)

    pares_moedas = ['ADA-USD', 'ADA-BTC', 'ADA-ETH', 'AVAX-USD', 'AVAX-BTC', 'ALICE-USD', 'ALPHA-USD', 'AR-USD', 'BADGER-USD', 'BNB-USD', 'BNB-BTC', 'BNB-ETH', 'BNB-EUR', 'BTC-ETH', 'BTC-EUR', 'BTC-USD', 'CAKE-USD', 'DOT-USD', 'DOGE-USD', 'ENJ-USD', 'ETH-BTC', 'ETH-USD', 'ETH-EUR', 'LINK-USD', 'LTC-USD', 'LTC-BTC', 'MATIC-USD', 'MATIC-BTC', 'PERP-USD', 'SCRT-USD', 'SHIB-USD', 'SUSHI-USD', 'SOL-USD', 'TRX-USD', 'TRX-BTC', 'UNI7083-USD', 'XRP-USD', 'XRP-BTC', 'XRP-ETH','YGG-USD']
    
    tempoInicial = time.time()
    pares_moedas_formatadas = [formatar_par(par) for par in pares_moedas]
    processar_dados(pares_moedas_formatadas)
    print(f"O tempo foi de: {time.time() - tempoInicial}")
