import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import mplfinance as mpf

df = pd.read_csv("data/spy_prices_data.csv")

sns.set_style("darkgrid")

df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

plt.figure(figsize=(12, 6))

sns.lineplot(
    data=df, x="timestamp", y="close", color="green", linewidth=2
)

plt.title("Vývoj ceny SPY (Close Price)", fontsize=14, fontweight='bold')
plt.xlabel("Dátum", fontsize=12)
plt.ylabel("Close Price (USD)", fontsize=12)
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/vyvoj_cien_spy.png")
plt.show()

fig, axes = plt.subplots(
    nrows=2, ncols=1, figsize=(12, 8), sharex=True, gridspec_kw={"height_ratios": [3, 1]}
)

plt.title("SPY - Cena a Objem obchodov", fontsize=14, fontweight='bold')

# Close Price
axes[0].plot(
    df["timestamp"], df["close"], color="green"
)

axes[0].set_ylabel("Close Price (USD)")

# Volume
axes[1].bar(
    df["timestamp"], df["volume"], color="red", width=1
)

axes[1].set_ylabel("Objem")
axes[1].set_xlabel("Dátum")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/vyvoj_cien_a_objemu_spy.png")
plt.show()

df.set_index("timestamp", inplace=True)

market_colors = mpf.make_marketcolors(
    up="forestgreen", down="crimson", wick="inherit", volume="in", ohlc="black"
)

custom_style = mpf.make_mpf_style(
    marketcolors=market_colors, gridstyle="--", gridcolor="lightgray", y_on_right=False
)

# Candlestick
mpf.plot(
    data=df,
    type="candle",
    style=custom_style,
    title="SPY - Sviečkový graf (Candlestick)",
    ylabel="Cena (USD)",
    ylabel_lower="Objem",
    figratio=(14, 8),
    savefig="outputs/svieckovy_graf_spy.png",
)

df.reset_index("timestamp", inplace=True)

sns.set_style("darkgrid")

def calculate_rsi(data, column="close", period=14):
    delta = data[column].diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.ewm(alpha=1/period, min_periods=period, adjust=False).mean() # EMA
    avg_loss = loss.ewm(alpha=1/period, min_periods=period, adjust=False).mean() # EMA

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))

# Simple Moving Average (14 days)
df["SMA 14"] = df["close"].rolling(14).mean()

# Exponential Moving Average (14 days)
df["EMA 14"] = df["close"].ewm(alpha=1/14, min_periods=14, adjust=False).mean()

# Daily Return (%)
df["daily_return"] = df["close"].pct_change() * 100

# Volatility
df["volatility"] = df["close"].rolling(14).std()

# Relative Strength Index
df["RSI"] = calculate_rsi(data=df, period=14)

# Upper Bollinger Band
df["upper_band"] = df["SMA 14"] + 2 * df["volatility"]

# Lower Bollinger Band
df["lower_band"] = df["SMA 14"] - 2 * df["volatility"]

# Fast Exponential Moving Average (12 days)
df["EMA 12"] = df["close"].ewm(alpha=1/12, min_periods=12, adjust=False).mean()

# Slow Exponential Moving Average (26 days)
df["EMA 26"] = df["close"].ewm(alpha=1/26, min_periods=26, adjust=False).mean()

# Moving Average Convergence Divergence
df["MACD"] = df["EMA 12"] - df["EMA 26"]

# Signal Line
df["Signal"] = df["MACD"].ewm(alpha=1/9, min_periods=9, adjust=False).mean()

# MACD Histogram
df["MACD Histogram"] = df["MACD"] - df["Signal"]

# Crossed Up Points
df["crossed_up"] = (
    (df["MACD"].shift(1) <= df["Signal"].shift(1)) &
(df["MACD"] > df["Signal"])
)

# Crossed Down Points
df["crossed_down"] = (
    (df["MACD"].shift(1) >= df["Signal"].shift(1)) &
(df["MACD"] < df["Signal"])
)

fig_1, axes_1 = plt.subplots(
    nrows=2, ncols=1, figsize=(12, 9), sharex=True
)

# Close Price
axes_1[0].plot(
    df["timestamp"], df["close"], label="Zatváracia cena (USD)", color="purple", alpha=0.6
)

# EMA 14
axes_1[0].plot(
    df["timestamp"], df["EMA 14"], label="EMA 14", color="darkorange", linewidth=2
)

axes_1[0].set_title("SPY – Cena a Exponenciálny kĺzavý priemer (EMA 14)", fontsize=12, fontweight='bold')
axes_1[0].set_ylabel("Cena (USD)")
axes_1[0].legend(loc="upper left")
axes_1[0].grid(True, linestyle="--", alpha=0.5)

# Close Price
axes_1[1].plot(
    df["timestamp"], df["close"], label="Zatváracia cena (USD)", color="purple", alpha=0.6
)

# SMA 14
axes_1[1].plot(
    df["timestamp"], df["SMA 14"], label="SMA 14", color="darkorange", linewidth=2
)

axes_1[1].set_title("SPY – Cena a Jednoduchý kĺzavý priemer (SMA 14)", fontsize=12, fontweight='bold')
axes_1[1].set_ylabel("Cena (USD)")
axes_1[1].set_xlabel("Dátum")
axes_1[1].legend(loc="upper left")
axes_1[1].grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/ema_a_sma_14_spy.png")
plt.show()

fig_2, axes_2 = plt.subplots(
    nrows=2, ncols=1, figsize=(12, 9), sharex=True
)

# Volatility
axes_2[0].plot(
    df["timestamp"], df["volatility"], label="Volatilita (20 dní)", color="crimson", linewidth=1.5
)

axes_2[0].set_title("Volatilita (Smerodajná odchýlka cien)", fontsize=14, fontweight='bold')
axes_2[0].set_ylabel("Volatilita")
axes_2[0].legend(loc="upper left")
axes_2[0].grid(True, linestyle="--", alpha=0.5)

# RSI
axes_2[1].plot(
    df["timestamp"], df["RSI"], label="RSI", color="darkorange", linewidth=2
)

axes_2[1].axhline(70, color="red", linestyle="--", alpha=0.7, label="Prekupené (70)")
axes_2[1].axhline(30, color="green", linestyle="--", alpha=0.7, label="Prepredané (30)")
axes_2[1].set_title("SPY – Relative Strength Index (RSI)", fontsize=14, fontweight='bold')
axes_2[1].set_ylabel("RSI")
axes_2[1].set_xlabel("Dátum")
axes_2[1].legend(loc="upper left")
axes_2[1].grid(True, linestyle="--", alpha=0.5)

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/volatilita_a_rsi_spy.png")
plt.show()

plt.figure(figsize=(12, 6))

# Daily Returns
plt.bar(
    df["timestamp"], df["daily_return"], label="Denný výnos (%)", color="forestgreen", alpha=0.7
)

plt.title("Denné percentuálne zmeny (Daily Returns)", fontsize=14, fontweight='bold')
plt.xlabel("Dátum", fontsize=12)
plt.ylabel("Zmena (%)", fontsize=12)
plt.axhline(0, color="black", linewidth=1, linestyle="--")
plt.legend(loc="upper left")
plt.grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/denne_vynosy_spy.png")
plt.show()

fig_3, ax = plt.subplots(figsize=(12, 6))

# Close Price
ax.plot(
    df["timestamp"], df["close"], label="Zatváracia cena (Close)", color="purple", linewidth=1.5
)

# SMA 14
ax.plot(
    df["timestamp"], df["SMA 14"], label="SMA 14 (Stred)", color="darkorange", linewidth=1.5
)

# Upper Bollinger Band
ax.plot(
    df["timestamp"], df["upper_band"], label="Horné pásmo (+2 STD)", color="crimson", linestyle="--", alpha=0.7
)

# Lower Bollinger Band
ax.plot(
    df["timestamp"], df["lower_band"], label="Dolné pásmo (-2 STD)", color="forestgreen", linestyle="--", alpha=0.7
)

# Bollinger Tunnel
ax.fill_between(
    df["timestamp"], df["upper_band"], df["lower_band"], color="gray", alpha=0.15, label="Bollingerov tunel (95%)"
)

ax.set_title("SPY – Kompletné Bollingerove pásma v jednom grafe", fontsize=14, fontweight='bold')
ax.set_xlabel("Dátum", fontsize=12)
ax.set_ylabel("Cena (USD)", fontsize=12)
ax.legend(loc="upper left")
ax.grid(True, linestyle="--", alpha=0.5)

plt.tight_layout()

plt.savefig("outputs/bollingerove_pasma_spy.png")
plt.show()

fig_4, axes_3 = plt.subplots(
    nrows=3, ncols=1, figsize=(12, 10), sharex=True, gridspec_kw={"height_ratios": [2, 1.5, 1]}
)

# Close Price
axes_3[0].plot(
    df["timestamp"], df["close"], label="Zatváracia cena (Close)", color="purple", linewidth=0.6
)

# EMA 12
axes_3[0].plot(
    df["timestamp"], df["EMA 12"], label="EMA 12 (Rýchly)", color="dodgerblue", linewidth=1.5
)

# EMA 26
axes_3[0].plot(
    df["timestamp"], df["EMA 26"], label="EMA 26 (Pomalý)", color="darkorange", linewidth=1.5
)

axes_3[0].set_title("SPY – Cena a oba EMA", fontsize=14, fontweight="bold")
axes_3[0].set_ylabel("Cena (USD)")
axes_3[0].legend(loc="upper left")
axes_3[0].grid(True, linestyle="--", alpha=0.5)

# MACD
axes_3[1].plot(
    df["timestamp"], df["MACD"], label="MACD", color="dodgerblue", linewidth=1.5
)

# Signal Line
axes_3[1].plot(
    df["timestamp"], df["Signal"], label="Signal (EMA 9 z MACD)", color="darkorange", linewidth=1.5
)

axes_3[1].axhline(0, color="black", linewidth=1, linestyle="--", alpha=0.6)

up_points = df[df["crossed_up"]]

down_points = df[df["crossed_down"]]

# Crossed Up Points
axes_3[1].scatter(
    up_points["timestamp"], up_points["MACD"], color="green", marker="^", s=80, zorder=5, label="Cross ↑"
)

# Crossed Down Points
axes_3[1].scatter(
    down_points["timestamp"], down_points["MACD"], color="red", marker="v", s=80, zorder=5, label="Cross ↓"
)

axes_3[1].set_title("MACD vs Signálna línia", fontsize=14, fontweight="bold")
axes_3[1].set_ylabel("MACD")
axes_3[1].legend(loc="upper left")
axes_3[1].grid(True, linestyle="--", alpha=0.5)

colors = ["green" if v >= 0 else "red" for v in df["MACD Histogram"]]

# MACD Histogram
axes_3[2].bar(
    df["timestamp"], df["MACD Histogram"], color=colors, width=1, alpha=0.7
)

axes_3[2].axhline(0, color="black", linewidth=1)
axes_3[2].set_title("MACD Histogram (MACD − Signal)", fontsize=14, fontweight="bold")
axes_3[2].set_ylabel("Histogram")
axes_3[2].set_xlabel("Dátum")
axes_3[2].grid(True, linestyle="--", alpha=0.5)
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig("outputs/macd_spy.png")
plt.show()

plt.figure(figsize=(10, 8))

# Indicators Heatmap
sns.heatmap(
    df[["close", "RSI", "MACD", "volatility", "daily_return"]].corr(), annot=True, cmap="coolwarm", center=0
)

plt.title("Korelácia medzi indikátormi", fontsize=14, fontweight="bold")

plt.tight_layout()

plt.savefig("outputs/korelacna_heatmapa_spy.png")
plt.show()