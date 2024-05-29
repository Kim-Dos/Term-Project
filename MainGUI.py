from tkinter import *
from tkinter import font
from UpbitParsing import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Matplotlib 창 생성
# figure = plt.figure(figsize=(5, 4), dpi=100)
# axes = figure.add_subplot(111)

# Matplotlib 그래프를 Tkinter 앱에 추가하기
# canvas = FigureCanvasTkAgg(figure, master=app)
# canvas.draw()
# canvas.get_tk_widget().pack()

class MAINGUI:
    PrintFavoriteCoin = False
    MarketPrice = True
    User = USER_INFO()
    Coins = UPBIT_INFO()
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1024x720')
        self.tempFont = font.Font(size=20, weight='bold')

        # 좌 우  프레임 분리
        self.InitLeftFrame()

        self.InitRightFrame()

        self.window.mainloop()

    def InitLeftFrame(self):
        # 좌 프레임 (코인 정보 및 시장가 및 그래프 확인)
        self.LeftFrame = Frame(self.window)
        self.LeftFrame.pack(side='left', anchor='nw')
        # 모든 코인 보기 or 즐찾 코인 보기 변경창
        self.PrintCoinButton = Button(self.LeftFrame, width= 30, font=self.tempFont, text='모든 코인 / 즐겨 찾기', command=self.GetCoinData)
        self.PrintCoinButton.pack(side='top')
        # 스크롤 바를 통해서 원화 코인 들의 정보를 지정 더블클릭으로 검색과 같은 기능
        # 스크롤바를 캔버스에 넣고, 캔버스를 프레임에 담아서 보냄
        self.CoinCanvas = Canvas(self.LeftFrame, bg='white')
        self.CoinScrollBar = Scrollbar(self.LeftFrame, command=self.CoinCanvas.yview)
        self.CoinScrollBar.pack(side="right", fill="y")  # 스크롤바를 화면에 배치
        self.canvasFrame = Frame(self.CoinCanvas)
        self.CoinCanvas.create_window((0,0), window=self.canvasFrame)
        self.ShowAllCoins()

        self.canvasFrame.update_idletasks()
        self.CoinCanvas.config(scrollregion=self.CoinCanvas.bbox("all"))
        self.CoinCanvas.pack(side="top", fill="both", expand=True)

        self.GraphFrame = Frame(self.window)
        self.GraphFrame.pack(side='top')
        self.GraphCanvas = Canvas(self.GraphFrame, bg='white')
        self.GraphCanvas.pack(side='top')

    def InitRightFrame(self):

        self.RightFrame= Frame(self.window)
        self.RightFrame.pack(side='right', anchor='ne')

        Label(self.RightFrame).grid(row=0,column=0)
        # 코인 이름을 적을 곳
        self.CoinName = Entry(self.RightFrame, width=20, font=self.tempFont)
        self.CoinName.grid(row=1, column=1, columnspan=4)

        Label(self.RightFrame, width=5).grid(row=2,column=5)
        # 코인 검색 버튼
        self.SearchCoinButton = Button(self.RightFrame,width=10,font=self.tempFont, text='검색', command=self.CoinSearch)
        self.SearchCoinButton.grid(row=3, column=2)

        # 현재 보유 잔고
        self.CashFrame = Frame(self.RightFrame, bg='white')
        # self.CurrentCashCanvas = Canvas(self.RightFrame, bg='white')
        self.PrintCurrentCash()
        # self.CurrentCashCanvas.grid()
        self.CashFrame.grid(row=4,column=1, rowspan=3, columnspan=3)


        self.tempFont= font.Font(size=20,weight='bold')
        # 시장가, 지정가 전환
        self.MarketPriceButton = Button(self.RightFrame, text='시장가', font=self.tempFont, bg='light gray', state='disabled', command=self.ChangePrice)
        self.MarketPriceButton.grid(row=8, column=1)
        self.LimitPriceButton = Button(self.RightFrame, text='지정가', font=self.tempFont, bg='white', command=self.ChangePrice)
        self.LimitPriceButton.grid(row=8, column=2)

        Label(self.RightFrame, width=20,height=2).grid(row=9,column=1)

        self.tempFont = font.Font(size=20)
        # 금액을 적는 칸
        self.PriceEntry = Entry(self.RightFrame, width=10, font=self.tempFont)
        self.PriceEntry.grid(row=12, column= 1)
        # 양을 적는 칸
        self.VolumeEntry = Entry(self.RightFrame, width=10, font=self.tempFont)
        self.VolumeEntry.grid(row=12, column= 2)
        # 간단한 표시
        self.sticklabel1 = Label(self.RightFrame, width=20,height=2, text='가격')
        self.sticklabel1.grid(row=13,column=1)
        self.sticklabel2 = Label(self.RightFrame, width=20,height=2, text='양')
        self.sticklabel2.grid(row=13,column=2)

        # 매수 매도 버튼
        self.SellButton = Button(self.RightFrame, text='매수', font=self.tempFont, command=self.Sell)
        self.SellButton.grid(row=14, column=1)
        self.BuyButton = Button(self.RightFrame, text='매도', font=self.tempFont, command=self.Buy)
        self.BuyButton.grid(row=14, column=2)

        Label(self.RightFrame, width=5).grid(row=0,column=5)

    def PrintCurrentCash(self):
        accounts = self.User.currentAccount()
        self.tempFont = font.Font(size=14)
        for i in range(len(accounts)):
            label = Label(self.CashFrame, text= "종목 "+accounts[i]['currency']+", 자산"+accounts[i]['balance'], bg='white')
            label.grid(row=i, column=0)

        for i in range(4-len(accounts)):
            label = Label(self.CashFrame, bg='white')
            label.grid(row=i+len(accounts), column=0)

    def GetCoinData(self):
        # PrintCoinGraph
        pass
    def ShowCoinInfo(self, event):
        #PrintCointGraph
        pass
    def ChangePrice(self):
        if self.MarketPrice == True:
            self.MarketPrice = False
            self.LimitPriceButton['state'] = 'disabled'
            self.MarketPriceButton['state'] = 'active'
            self.MarketPriceButton['bg'] = 'white'
            self.LimitPriceButton['bg'] = 'light gray'
        else:
            self.MarketPrice = True
            self.LimitPriceButton['state'] = 'active'
            self.MarketPriceButton['state'] = 'disabled'
            self.MarketPriceButton['bg'] = 'light gray'
            self.LimitPriceButton['bg'] = 'white'


    def ShowAllCoins(self):
        self.tempFont= font.Font(size=14)
        for c in self.Coins.KRW_List:
            label = Label(self.canvasFrame,font=self.tempFont, text='['+c['market']+']   '+c['korean_name'])
            label.pack()
            label.bind('<Double-Button-1>', self.ShowCoinInfo)

    def CoinSearch(self):
        self.sticklabel1.config(text='가격')
        self.sticklabel2.config(text='양')
        name = self.CoinName.get()
        if self.Coins.find_coin(name):
            self.Coins.get_coin(name)


    def Sell(self):
        name = self.CoinName.get()
        price = self.PriceEntry.get()
        volume = self.VolumeEntry.get()
        if self.MarketPrice:
            if -1 == self.User.market_sell(name, price):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!')
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!')
        else:
            if -1 == self.User.limit_sell(name, price, volume):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!')
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!')
        self.PrintCurrentCash()
    def Buy(self):
        name = self.CoinName.get()
        price = self.PriceEntry.get()
        volume = self.VolumeEntry.get()
        if self.MarketPrice:
            if -1 == self.User.market_buy(name, price):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!')
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!')
        else:
            if -1 == self.User.limit_buy(name, price, volume):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!')
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!')
        self.PrintCurrentCash()

MAINGUI()