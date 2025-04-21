
def detect_bullish_engulfing(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] < open_[i-1] and close[i] > open_[i]:
            if close[i] > open_[i-1] and open_[i] < close[i-1]:
                result[i] = 1
    return result

def detect_morning_star(open_, high, low, close):
    result = [0] * len(close)
    for i in range(2, len(close)):
        if close[i-2] < open_[i-2] and abs(close[i-1] - open_[i-1]) < abs(close[i-2] - open_[i-2]) * 0.5:
            if close[i] > open_[i] and close[i] > ((open_[i-2] + close[i-2]) / 2):
                result[i] = 1
    return result

def detect_three_white_soldiers(open_, high, low, close):
    result = [0] * len(close)
    for i in range(2, len(close)):
        if (close[i-2] > open_[i-2] and close[i-1] > open_[i-1] and close[i] > open_[i] and
            close[i-2] < close[i-1] < close[i]):
            result[i] = 1
    return result

def detect_hammer(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        lower_shadow = open_[i] - low[i] if close[i] > open_[i] else close[i] - low[i]
        upper_shadow = high[i] - close[i] if close[i] > open_[i] else high[i] - open_[i]
        if lower_shadow > 2 * body and upper_shadow < body:
            result[i] = 1
    return result

def detect_inverted_hammer(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        upper_shadow = high[i] - close[i] if close[i] > open_[i] else high[i] - open_[i]
        lower_shadow = open_[i] - low[i] if close[i] > open_[i] else close[i] - low[i]
        if upper_shadow > 2 * body and lower_shadow < body:
            result[i] = 1
    return result

def detect_piercing_line(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] < open_[i-1] and close[i] > open_[i]:
            if open_[i] < close[i-1] and close[i] > (open_[i-1] + close[i-1]) / 2:
                result[i] = 1
    return result

def detect_tweezer_bottoms(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if low[i] == low[i-1]:
            if close[i] > open_[i] and close[i-1] < open_[i-1]:
                result[i] = 1
    return result

def detect_bullish_harami(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] < open_[i-1] and open_[i] < close[i] and close[i] < open_[i-1] and open_[i] > close[i-1]:
            result[i] = 1
    return result

def detect_dragonfly_doji(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        lower_shadow = min(open_[i], close[i]) - low[i]
        if body < (high[i] - low[i]) * 0.1 and lower_shadow > body * 2:
            result[i] = 1
    return result

def detect_bearish_engulfing(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] > open_[i-1] and close[i] < open_[i]:
            if close[i] < open_[i-1] and open_[i] > close[i-1]:
                result[i] = 1
    return result

def detect_evening_star(open_, high, low, close):
    result = [0] * len(close)
    for i in range(2, len(close)):
        if close[i-2] > open_[i-2] and abs(close[i-1] - open_[i-1]) < abs(close[i-2] - open_[i-2]) * 0.5:
            if close[i] < open_[i] and close[i] < ((open_[i-2] + close[i-2]) / 2):
                result[i] = 1
    return result

def detect_three_black_crows(open_, high, low, close):
    result = [0] * len(close)
    for i in range(2, len(close)):
        if (close[i-2] < open_[i-2] and close[i-1] < open_[i-1] and close[i] < open_[i] and
            close[i-2] > close[i-1] > close[i]):
            result[i] = 1
    return result

def detect_shooting_star(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        upper_shadow = high[i] - max(open_[i], close[i])
        lower_shadow = min(open_[i], close[i]) - low[i]
        if upper_shadow > 2 * body and lower_shadow < body:
            result[i] = 1
    return result

def detect_hanging_man(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        lower_shadow = min(open_[i], close[i]) - low[i]
        upper_shadow = high[i] - max(open_[i], close[i])
        if lower_shadow > 2 * body and upper_shadow < body:
            result[i] = 1
    return result

def detect_dark_cloud_cover(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] > open_[i-1] and open_[i] > close[i-1] and close[i] < (open_[i-1] + close[i-1]) / 2:
            result[i] = 1
    return result

def detect_tweezer_tops(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if high[i] == high[i-1]:
            if close[i] < open_[i] and close[i-1] > open_[i-1]:
                result[i] = 1
    return result

def detect_bearish_harami(open_, high, low, close):
    result = [0] * len(close)
    for i in range(1, len(close)):
        if close[i-1] > open_[i-1] and open_[i] > close[i] and close[i] > open_[i-1] and open_[i] < close[i-1]:
            result[i] = 1
    return result

def detect_gravestone_doji(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        upper_shadow = high[i] - max(open_[i], close[i])
        if body < (high[i] - low[i]) * 0.1 and upper_shadow > body * 2:
            result[i] = 1
    return result

def detect_doji(open_, high, low, close):
    result = [0] * len(close)
    for i in range(len(close)):
        body = abs(close[i] - open_[i])
        if body < (high[i] - low[i]) * 0.1:
            result[i] = 1
    return result
