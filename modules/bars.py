import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
import plotly.graph_objects as go

def build_tick_imbalance_bars(df, imbalance_threshold=10):
    bars = []
    theta_t = 0
    bar_data = []
    b_t_prev = 1
    new_bar = False
    df = df.sort_index().copy()
    df = df[['open', 'high', 'low', 'close', 'volume']].dropna()

    for i in range(1, len(df)):
        
        delta = df['close'].iloc[i] - df['close'].iloc[i-1]
        if new_bar:
            b_t = b_t_prev
            new_bar = False
        else: 
            if delta == 0:
                b_t = b_t_prev
            else:
                b_t = int(np.sign(delta))

        b_t_prev = b_t
        theta_t += b_t
        bar_data.append(df.iloc[i])

        if abs(theta_t) >= imbalance_threshold:
            bar_df = pd.DataFrame(bar_data)
            o = bar_df['open'].iloc[0]
            h = bar_df['high'].max()
            l = bar_df['low'].min()
            c = bar_df['close'].iloc[-1]
            v = bar_df['volume'].sum()
            t = bar_df.index[-1]
            bars.append({'time':t, 'open':o, 'high':h, 'low':l, 'close': c, 'volume':v})
            new_bar = True
            theta_t = 0
            bar_data = []

    bars_df = pd.DataFrame(bars)
    return bars_df

def plot_candles(bars_df, title="Tick Imbalance Bars"):
    fig, ax = plt.subplots(figsize=(14, 6))
    width = 0.6
    for i in range(len(bars_df)):   
        o, h, l, c = bars_df.iloc[i][['open', 'high', 'low', 'close']]
        color = 'green' if c >= o else 'red'
        ax.plot([i, i], [l, h], color='black')
        ax.add_patch(plt.Rectangle((i - width/2, min(o, c)), width, abs(c - o), color=color))
    ax.set_title(title)
    ax.set_xlabel('Bar Index')
    ax.set_ylabel('Price')
    ax.grid(True) 
    plt.show()

def plot_candles_with_volume(bars_df, title="Tick Imbalance Bars"):
    import matplotlib.pyplot as plt

    bars_df = bars_df.reset_index(drop=True)
    fig, (ax_price, ax_vol) = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                                           gridspec_kw={'height_ratios': [3, 1]})

    width = 0.6

    for i in range(len(bars_df)):
        o, h, l, c = bars_df.iloc[i][['open', 'high', 'low', 'close']]
        v = bars_df.iloc[i]['volume']
        color = 'green' if c >= o else 'red'

        # Candle (Price)
        ax_price.plot([i, i], [l, h], color='black', linewidth=1)
        ax_price.add_patch(plt.Rectangle((i - width/2, min(o, c)),
                                         width,
                                         abs(c - o),
                                         color=color))

        # Volume bar
        ax_vol.bar(i, v, width=width, color=color)
    ax_price.set_title(title)
    ax_price.set_ylabel("Price")
    ax_vol.set_ylabel("Volume")
    ax_vol.set_xlabel("Bar Index (event-based)")
    ax_price.grid(True)
    ax_vol.grid(True)
    plt.tight_layout()
    plt.show()

def plot_candles_with_volume_time(bars_df, title="Tick Imbalance Bars (Time X-Axis)"):
    import matplotlib.pyplot as plt
    import pandas as pd
    import matplotlib.dates as mdates

    # Ensure 'time' is a datetime index
    if 'time' in bars_df.columns:
        bars_df = bars_df.set_index('time')

    fig, (ax_price, ax_vol) = plt.subplots(2, 1, figsize=(14, 8), sharex=True,
                                           gridspec_kw={'height_ratios': [3, 1]})

    width = pd.Timedelta(minutes=2)  # candle width — adjust to suit your bar frequency
    #width = width = pd.Timedelta(...) 

    for time, row in bars_df.iterrows():
        o, h, l, c = row[['open', 'high', 'low', 'close']]
        v = row['volume']
        color = 'green' if c >= o else 'red'

        # Candle wick
        ax_price.plot([time, time], [l, h], color='black', linewidth=1)

        # Candle body
        ax_price.add_patch(plt.Rectangle((time - width / 2, min(o, c)),
                                         width,
                                         abs(c - o),
                                         color=color))

        # Volume bar
        ax_vol.bar(time, v, width=width, color=color)

    # Format x-axis as datetime
    ax_price.set_title(title)
    ax_price.set_ylabel("Price")
    ax_vol.set_ylabel("Volume")
    ax_vol.set_xlabel("Time")

    ax_price.grid(True)
    ax_vol.grid(True)

    ax_vol.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d\n%H:%M'))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()