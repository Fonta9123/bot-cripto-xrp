
import time
import pandas as pd
import requests
import ta
import os
from datetime import datetime

# ===== FUNCIONES DE ESTRATEGIA Y VELAS INTEGRADAS =====
def detectar_patron_vela(row, tipo):
    if tipo == 'bullish':
        return row['close'] > row['open'] and (row['close'] - row['open']) > 0.01
    else:
        return row['open'] > row['close'] and (row['open'] - row['close']) > 0.01

def evaluar_estrategia(df):
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['macd'] = ta.trend.MACD(df['close']).macd_diff()
    df['tsi'] = ta.momentum.TSIIndicator(df['close']).tsi()
    df['vol_avg'] = df['volume'].rolling(window=14).mean()

    df['candle_bull'] = df.apply(lambda x: detectar_patron_vela(x, 'bullish'), axis=1)
    df['candle_bear'] = df.apply(lambda x: detectar_patron_vela(x, 'bearish'), axis=1)

    rsi = df['rsi'].iloc[-1]
    macd = df['macd'].iloc[-1]
    tsi = df['tsi'].iloc[-1]
    vol = df['volume'].iloc[-1]
    vol_avg = df['vol_avg'].iloc[-1]
    precio = df['close'].iloc[-1]
    timestamp = df['timestamp'].iloc[-1]
    vela_bull = df['candle_bull'].iloc[-1]
    vela_bear = df['candle_bear'].iloc[-1]

    señal_compra = (rsi < 35 and macd > 0 and tsi > 0 and vol > vol_avg) or vela_bull
    señal_venta = (rsi > 65 and macd < 0 and tsi < 0 and vol > vol_avg) or vela_bear

    return señal_compra, señal_venta, precio, timestamp

# ===== FUNCIONES DEL BOT =====

porcentaje_operacion = 0.95
archivo_estado = 'estado_virtual.json'
archivo_historial = 'historial_virtual.csv'

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

def leer_estado_actual():
    if not os.path.exists(archivo_estado):
        estado = {'usdt': 1000.0, 'xrp': 0.0}
        with open(archivo_estado, 'w') as f:
            f.write(str(estado))
        return estado['usdt'], estado['xrp']
    with open(archivo_estado, 'r') as f:
        estado = eval(f.read())
    return estado['usdt'], estado['xrp']

def guardar_estado(usdt, xrp):
    with open(archivo_estado, 'w') as f:
        f.write(str({'usdt': usdt, 'xrp': xrp}))

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

if __name__ == '__main__':
    while True:
        try:
            df = fetch_ohlcv()
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
