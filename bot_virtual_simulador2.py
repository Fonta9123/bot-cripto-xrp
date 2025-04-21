import time
import pandas as pd
import requests
import ta
import os
from datetime import datetime
from evaluar_estrategia import evaluar_estrategia  # ✅ NUEVO

# Parámetros
porcentaje_operacion = 0.95
archivo_estado = 'estado_virtual.json'
archivo_historial = 'historial_virtual.csv'

# Función para obtener datos de KuCoin
def fetch_ohlcv(symbol="XRP-USDT", interval="15min", limit=100):
    url = f"https://api.kucoin.com/api/v1/market/candles?type={interval}&symbol={symbol}&limit={limit}"
    response = requests.get(url)
    data = response.json()

    ohlcv = []
    for item in reversed(data['data']):
        timestamp = datetime.fromtimestamp(int(item[0]) / 1000)
        ohlcv.append({
            'timestamp': timestamp,
            'open': float(item[1]),
            'high': float(item[3]),
            'low': float(item[4]),
            'close': float(item[2]),
            'volume': float(item[5])
        })

    return pd.DataFrame(ohlcv)

# Función para aplicar indicadores técnicos
def apply_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['macd'] = ta.trend.MACD(df['close']).macd_diff()
    df['tsi'] = ta.momentum.TSIIndicator(df['close']).tsi()
    df['vol_avg'] = df['volume'].rolling(window=14).mean()
    return df

# Leer estado actual de simulación
def leer_estado_actual():
    if not os.path.exists(archivo_estado):
        estado = {'usdt': 1000.0, 'xrp': 0.0}
        with open(archivo_estado, 'w') as f:
            f.write(str(estado))
        return estado['usdt'], estado['xrp']

    with open(archivo_estado, 'r') as f:
        estado = eval(f.read())
    return estado['usdt'], estado['xrp']

# Guardar estado actual
def guardar_estado(usdt, xrp):
    with open(archivo_estado, 'w') as f:
        f.write(str({'usdt': usdt, 'xrp': xrp}))

# Guardar historial
def guardar_historial(tipo, precio, cantidad, timestamp):
    nuevo = pd.DataFrame([{
        'tipo': tipo,
        'precio': precio,
        'cantidad': cantidad,
        'timestamp': timestamp
    }])

    if os.path.exists(archivo_historial):
        anterior = pd.read_csv(archivo_historial)
        df = pd.concat([anterior, nuevo], ignore_index=True)
    else:
        df = nuevo

    df.to_csv(archivo_historial, index=False)

# Simular operación
def simular_operacion(tipo, precio, timestamp, cantidad):
    usdt, xrp = leer_estado_actual()

    if tipo == 'compra':
        usdt -= cantidad * precio
        xrp += cantidad
        print(f"🟢 COMPRA: {cantidad:.2f} XRP a {precio:.4f} USDT")
    elif tipo == 'venta':
        usdt += cantidad * precio
        xrp -= cantidad
        print(f"🔴 VENTA: {cantidad:.2f} XRP a {precio:.4f} USDT")

    guardar_estado(usdt, xrp)
    guardar_historial(tipo, precio, cantidad, timestamp)

# Bucle principal
if __name__ == '__main__':
    while True:
        try:
            df = fetch_ohlcv()
            df = apply_indicators(df)
            señal_compra, señal_venta, precio_actual, timestamp = evaluar_estrategia(df)

            usdt, xrp = leer_estado_actual()
            print(f"\n📊 Estado actual: {usdt:.2f} USDT | {xrp:.2f} XRP")

            if señal_compra and usdt > 10:
                monto = usdt * porcentaje_operacion
                cantidad = monto / precio_actual
                simular_operacion('compra', precio_actual, timestamp, cantidad)

            elif señal_venta and xrp > 0:
                simular_operacion('venta', precio_actual, timestamp, xrp)

            else:
                print("⏸️ No se realiza ninguna operación.")

            time.sleep(60 * 15)

        except Exception as e:
            print(f"⚠️ Error: {e}")
            time.sleep(60)
