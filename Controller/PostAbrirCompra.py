import pandas as pd
from binance.client import Client
import os

key_path = './Variaveis/Api_Key.txt'
secret_path = './Variaveis/Secret_Key.txt'

directory = './ConsumoApiBinance/Dados_OrdensDeCompra'

with open(key_path, 'r') as file:
    api_key = file.read().strip()

with open(secret_path, 'r') as file:
    api_secret = file.read().strip()

client = Client(api_key, api_secret)

symbol = 'BTCBRL'
quantity = 0.001  

# Obtenha informações sobre os filtros de NOTIONAL para o símbolo
exchange_info = client.get_exchange_info()
symbol_info = next((s for s in exchange_info['symbols'] if s['symbol'] == symbol), None)

if symbol_info is not None:
    notional_filter = next((f for f in symbol_info['filters'] if f['filterType'] == 'MIN_NOTIONAL'), None)

    if notional_filter is not None:
        ticker = client.get_ticker(symbol=symbol)
        current_price = float(ticker['lastPrice'])
        notional_value = quantity * current_price
        min_notional = float(notional_filter['minNotional'])

        if notional_value < min_notional:
            raise ValueError(f"O valor total da ordem é inferior ao mínimo permitido ({min_notional})")

        price = current_price + 10  # Ajuste conforme necessário

        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_LIMIT,
            quantity=quantity,
            price=price,
            timeInForce=Client.TIME_IN_FORCE_GTC
        )

        print("Ordem de Compra Aberta:")
        print(f"Símbolo: {order['symbol']}")
        print(f"Tipo: {order['side']}")
        print(f"Preço: {order['price']}")
        print(f"Quantidade: {order['origQty']}")
        print(f"Status: {order['status']}")

        data = {
            'Symbol': [order['symbol']],
            'Type': [order['side']],
            'Price': [order['price']],
            'Quantity': [order['origQty']],
            'Status': [order['status']],
        }

        df = pd.DataFrame(data)

        csv_filename = 'compra_aberta.csv'
        csv_filename = os.path.join(directory, csv_filename)
        df.to_csv(csv_filename, index=False)

        print(f"Informações da ordem salvas em {csv_filename}")
    else:
        print(f"Filtro MIN_NOTIONAL não encontrado para o símbolo {symbol}.")
else:
    print(f"Símbolo {symbol} não encontrado nas informações de câmbio.")
