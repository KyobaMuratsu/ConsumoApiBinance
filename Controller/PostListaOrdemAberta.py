import pandas as pd
from binance.client import Client
import os

key_path = './Variaveis/Api_Key.txt'
secret_path = './Variaveis/Secret_Key.txt'

directory = './ConsumoApiBinance/Dados_Ordens_Abertas'

with open(key_path, 'r') as file:
    api_key = file.read().strip()

with open(secret_path, 'r') as file:
    api_secret = file.read().strip()

client = Client(api_key, api_secret)

symbol = 'BTCUSDT'

open_orders = client.get_open_orders(symbol=symbol)

data = {
    'Symbol': [],
    'Type': [],
    'Price': [],
    'Quantity': [],
    'Status': [],
}

for order in open_orders:
    data['Symbol'].append(order['symbol'])
    data['Type'].append(order['side'])
    data['Price'].append(order['price'])
    data['Quantity'].append(order['origQty'])
    data['Status'].append(order['status'])

df = pd.DataFrame(data)

csv_filename = 'open_orders.csv'
csv_filename = os.path.join(directory, csv_filename)
df.to_csv(csv_filename, index=False)

print(f"Ordens abertas salvas em {csv_filename}")