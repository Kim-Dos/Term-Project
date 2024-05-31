import requests

# url = "https://api.upbit.com/v1/ticker?markets="

d = [
"KRW-BTC,KRW-ETH,KRW-NEO,KRW-MTL,KRW-XRP,KRW-ETC,KRW-SNT,KRW-WAVES,KRW-XEM,KRW-QTUM",
"KRW-LSK,KRW-STEEM,KRW-XLM,KRW-ARDR,KRW-ARK,KRW-STORJ,KRW-GRS,KRW-ADA,KRW-SBD,KRW-POWR",
"KRW-BTG,KRW-ICX,KRW-EOS,KRW-TRX,KRW-SC,KRW-ONT,KRW-ZIL,KRW-POLYX,KRW-ZRX,KRW-LOOM",
"KRW-BCH,KRW-BAT,KRW-IOST,KRW-CVC,KRW-IQ,KRW-IOTA,KRW-HIFI,KRW-ONG,KRW-GAS,KRW-UPP",
"KRW-ELF,KRW-KNC,KRW-BSV,KRW-THETA,KRW-QKC,KRW-BTT,KRW-MOC,KRW-TFUEL,KRW-MANA,KRW-ANKR",
"KRW-AERGO,KRW-ATOM,KRW-TT,KRW-GAME2,KRW-MBL,KRW-WAXP,KRW-HBAR,KRW-MED,KRW-MLK,KRW-STPT",
"KRW-ORBS,KRW-VET,KRW-CHZ,KRW-STMX,KRW-DKA,KRW-HIVE,KRW-KAVA,KRW-AHT,KRW-LINK,KRW-XTZ",
"KRW-BORA,KRW-JST,KRW-CRO,KRW-TON,KRW-SXP,KRW-HUNT,KRW-DOT,KRW-MVL,KRW-STRAX,KRW-AQT",
"KRW-GLM,KRW-META,KRW-FCT2,KRW-CBK,KRW-SAND,KRW-HPO,KRW-DOGE,KRW-STRIKE,KRW-PUNDIX,KRW-FLOW",
"KRW-AXS,KRW-STX,KRW-XEC,KRW-SOL,KRW-MATIC,KRW-AAVE,KRW-1INCH,KRW-ALGO,KRW-NEAR,KRW-AVAX",
"KRW-T,KRW-CELO,KRW-GMT,KRW-APT,KRW-SHIB,KRW-MASK,KRW-ARB,KRW-EGLD,KRW-SUI,KRW-GRT",
"KRW-BLUR,KRW-IMX,KRW-SEI,KRW-MINA,KRW-CTC,KRW-ASTR,KRW-ID,KRW-PYTH,KRW-MNT,KRW-AKT",
"KRW-ZETA,KRW-AUCTION"
]
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pyupbit

# 데이터 가져오기
coin = "BTC"
interval = "day"  # day, minute1, minute3, minute5, minute10, minute15, minute30, minute60
df = pyupbit.get_ohlcv(f"{coin}-USDT", interval=interval, count=30)

# 차트 그리기
root = tk.Tk()
root.title(f"{coin} Price Chart")

fig = Figure(figsize=(8, 6))
ax = fig.add_subplot(111)
ax.plot(df.index, df["close"], label=f"{coin} Price", color="b")
ax.set_xlabel("Date")
ax.set_ylabel("Price (USDT)")
ax.set_title(f"{coin} Price Chart")
ax.grid(True)
ax.legend()

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack()

root.mainloop()