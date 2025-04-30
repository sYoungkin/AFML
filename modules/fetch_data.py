import ccxt
import pandas as pd
import plotly.graph_objects as go


def fetch_binance_data(symbol='BTC/USDT', timeframe='1m', limit=1000):
    exchange = ccxt.binance()
    data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit, params = {"paginate": True})
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df

def plot_price_data(df):
    fig = go.Figure()

    # === Price Line ===
    fig.add_trace(go.Scatter(
        x=df.index, y=df['close'],
        mode='lines', name='Price', line=dict(color='black')
    ))
    fig.show()