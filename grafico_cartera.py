import pandas as pd
import matplotlib.pyplot as plt
import ccxt

# Configura la moneda y exchange
symbol = 'XRP/USDT'
exchange = ccxt.binance()

archivo_operaciones = 'operaciones.csv'
capital_inicial = 1000

def obtener_precio_xrp(timestamp):
    # Buscar el precio más cercano al momento de la operación
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=500)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.resample('5min').pad()
    if timestamp in df.index:
        return df.loc[timestamp]['close']
    else:
        return df['close'].iloc[-1]

# Leer operaciones
df = pd.read_csv(archivo_operaciones)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Simular balance con cada operación
usdt = capital_inicial
xrp = 0
balances = []

for _, row in df.iterrows():
    precio_actual = obtener_precio_xrp(row['timestamp'])
    if row['tipo'] == 'compra':
        usdt -= row['precio'] * row['cantidad']
        xrp += row['cantidad']
    elif row['tipo'] == 'venta':
        usdt += row['precio'] * row['cantidad']
        xrp -= row['cantidad']
    valor_total = usdt + (xrp * precio_actual)
    balances.append((row['timestamp'], valor_total))

# Crear DataFrame para graficar
df_balances = pd.DataFrame(balances, columns=['timestamp', 'valor_total'])
df_balances.set_index('timestamp', inplace=True)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(df_balances.index, df_balances['valor_total'], marker='o', linestyle='-', color='blue')
plt.title('📈 Evolución de tu cartera virtual')
plt.xlabel('Fecha')
plt.ylabel('Valor total (USDT)')
plt.grid(True)
plt.tight_layout()
plt.show()
