from joblib import Parallel, delayed
from binance import Client
import pandas as pd
import time
import os

if __name__ == '__main__':
    key = './Variaveis/Api_Key.txt'
    secret = './Variaveis/Secret_Key.txt'

    with open(key, 'r') as file:
        api_key = file.read().strip()
    with open(secret, 'r') as file:
        api_secret = file.read().strip()


directory = './ConsumoApiBinance/Dados_CSV_ListaMoedasPossui'

client = Client(api_key, api_secret)

account_info = client.get_account()

balances = account_info['balances']

data = {
    'Asset': [],
    'Total': [],
    'Free': [],
    'Locked': [],
}

for balance in balances:
    asset = balance['asset']
    free = float(balance['free'])
    locked = float(balance['locked'])
    
    total = free + locked

    if total > 0:
        data['Asset'].append(asset)
        data['Total'].append(total)
        data['Free'].append(free)
        data['Locked'].append(locked)

df = pd.DataFrame(data)

# Save to CSV
csv_filename = 'account_balances.csv'
csv_filename = os.path.join(directory, csv_filename)
df.to_csv(csv_filename, index=False)

print(f"Account balances saved to {csv_filename}")

tempoInicial = time.time()
print(f"O tempo foi de: {time.time() - tempoInicial}")