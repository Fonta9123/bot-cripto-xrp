from velas_japonesas import (
    detect_bullish_engulfing,
    detect_morning_star,
    detect_three_white_soldiers,
    detect_hammer,
    detect_inverted_hammer,
    detect_piercing_line,
    detect_tweezer_bottoms,
    detect_bullish_harami,
    detect_dragonfly_doji,
    detect_doji,
    detect_bearish_engulfing,
    detect_evening_star,
    detect_three_black_crows,
    detect_shooting_star,
    detect_hanging_man,
    detect_dark_cloud_cover,
    detect_tweezer_tops,
    detect_bearish_harami,
    detect_gravestone_doji
)

def evaluar_estrategia(df):
    if df is None or df.empty:
        raise Exception("DataFrame vacío")

    open_ = df['open']
    high = df['high']
    low = df['low']
    close = df['close']

    velas_alcistas = {
        "Bullish Engulfing": detect_bullish_engulfing(open_, high, low, close),
        "Morning Star": detect_morning_star(open_, high, low, close),
        "Three White Soldiers": detect_three_white_soldiers(open_, high, low, close),
        "Hammer": detect_hammer(open_, high, low, close),
        "Inverted Hammer": detect_inverted_hammer(open_, high, low, close),
        "Piercing Line": detect_piercing_line(open_, high, low, close),
        "Tweezer Bottoms": detect_tweezer_bottoms(open_, high, low, close),
        "Bullish Harami": detect_bullish_harami(open_, high, low, close),
        "Dragonfly Doji": detect_dragonfly_doji(open_, high, low, close),
        "Doji": detect_doji(open_, high, low, close),
    }

    velas_bajistas = {
        "Bearish Engulfing": detect_bearish_engulfing(open_, high, low, close),
        "Evening Star": detect_evening_star(open_, high, low, close),
        "Three Black Crows": detect_three_black_crows(open_, high, low, close),
        "Shooting Star": detect_shooting_star(open_, high, low, close),
        "Hanging Man": detect_hanging_man(open_, high, low, close),
        "Dark Cloud Cover": detect_dark_cloud_cover(open_, high, low, close),
        "Tweezer Tops": detect_tweezer_tops(open_, high, low, close),
        "Bearish Harami": detect_bearish_harami(open_, high, low, close),
        "Gravestone Doji": detect_gravestone_doji(open_, high, low, close),
        "Doji": detect_doji(open_, high, low, close),
    }

    vela_alcista_detectada = None
    vela_bajista_detectada = None

    for nombre, serie in velas_alcistas.items():
        if serie[-1] == 1:
            vela_alcista_detectada = nombre
            break

    for nombre, serie in velas_bajistas.items():
        if serie[-1] == 1:
            vela_bajista_detectada = nombre
            break

    rsi = df['rsi'].iloc[-1]
    macd = df['macd'].iloc[-1]
    tsi = df['tsi'].iloc[-1]
    vol = df['volume'].iloc[-1]
    vol_avg = df['vol_avg'].iloc[-1]
    precio = df['close'].iloc[-1]
    timestamp = df['timestamp'].iloc[-1]

    señal_compra = vela_alcista_detectada is not None and rsi < 30 and macd > 0 and tsi > 0 and vol > vol_avg
    señal_venta = vela_bajista_detectada is not None and rsi > 70 and macd < 0 and tsi < 0 and vol > vol_avg

    if vela_alcista_detectada:
        print(f"📈 Patrón de vela alcista detectado: {vela_alcista_detectada}")
    if vela_bajista_detectada:
        print(f"📉 Patrón de vela bajista detectado: {vela_bajista_detectada}")

    return señal_compra, señal_venta, precio, timestamp
