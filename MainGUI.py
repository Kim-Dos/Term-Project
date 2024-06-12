# 구현해야할 것들
# C/C++ 연동 - 진행중

from tkinter import *
from tkinter import font
from tkinter import messagebox
from UpbitParsing import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import spam


class MAINGUI:
    PrintFavoriteCoin = True
    MarketPrice = True
    GraphWidget = False
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
        self.CoinCanvas = Canvas(self.LeftFrame, bg='white', height=400, width=550)
        self.CoinScrollBar = Scrollbar(self.LeftFrame, command=self.CoinCanvas.yview)
        self.CoinScrollBar.pack(side="right", fill="y")  # 스크롤바를 화면에 배치
        self.canvasFrame = Frame(self.CoinCanvas, bg='white', )
        self.CoinCanvas.create_window((0,0), window=self.canvasFrame)
        self.CoinCanvas.bind("<MouseWheel>", self.mouseWheel)
        # 모든 코인 불러오기
        self.ShowAllCoins()
        self.canvasFrame.update_idletasks()
        self.CoinCanvas.config(scrollregion=self.CoinCanvas.bbox("all"))
        self.CoinCanvas.pack(side="left", fill="both", expand=True)
        
        # 좌프레임에 박았는데 왜 우프레임에 있는지 모르겠지만 일단 사용
        self.GraphFrame = Frame(self.window)
        self.GraphFrame.pack(side='top')
        self.GraphCanvas = Canvas(self.GraphFrame, bg='white')
        self.GraphCanvas.pack(side='top')

    def InitRightFrame(self):
        # 우 프레임 (코인 검색, 잔고 확인 및 매매)
        self.RightFrame= Frame(self.window)
        self.RightFrame.pack(side='right', anchor='ne')

        Label(self.RightFrame).grid(row=0,column=0)
        # 코인 이름을 적을 곳
        self.CoinName = Entry(self.RightFrame, width=20, font=self.tempFont)
        self.CoinName.grid(row=1, column=1, columnspan=4)

        Label(self.RightFrame, width=5).grid(row=2,column=5)

        #코인 즐찾 버튼
        self.StarCoinButton = Button(self.RightFrame,width=10,font=self.tempFont, text='즐찾', command=self.Star)
        self.StarCoinButton.grid(row=3, column=1)
        # 코인 검색 버튼
        self.SearchCoinButton = Button(self.RightFrame,width=10,font=self.tempFont, text='검색', command=self.CoinSearch)
        self.SearchCoinButton.grid(row=3, column=2)

        self.PredPriceButton = Button(self.RightFrame,width=10,font=self.tempFont, text='예측', command=self.pricePredict)
        self.PredPriceButton.grid(row=3, column=3)

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
        self.BuyButton = Button(self.RightFrame, text='매수', font=self.tempFont, command=self.Buy)
        self.BuyButton.grid(row=14, column=1)
        self.SellButton = Button(self.RightFrame, text='매도', font=self.tempFont, command=self.Sell)
        self.SellButton.grid(row=14, column=2)

        Label(self.RightFrame, width=5).grid(row=0,column=5)

    def mouseWheel(self, event):
        self.CoinCanvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def PrintCurrentCash(self):
        accounts = self.User.currentAccount()
        self.tempFont = font.Font(size=14)
        for i in range(len(accounts)):
            if accounts[i]['currency'] == 'KRW':
                label = Label(self.CashFrame, text="종목 " + accounts[i]['currency'] + ", 보유량" + str(round(float(accounts[i]['balance']), 2)) + "원", bg='white')
            else:
                label = Label(self.CashFrame, text="종목 "+accounts[i]['currency']+", 보유량"+str(round(float(accounts[i]['balance']),5))+"개", bg='white')
            label.grid(row=i, column=0)

        for i in range(4-len(accounts)):
            label = Label(self.CashFrame, bg='white')
            label.grid(row=i+len(accounts), column=0)

    def GetCoinData(self):
        # # Switch Coins Lists
        if self.PrintFavoriteCoin:
            for widget in self.canvasFrame.winfo_children():
                widget.destroy()
            for coin in self.User.Star_List:
                coininfo = self.Coins.GetCoinInfo(coin)
                self.tempFont = font.Font(size=14)
                ko_name = self.Coins.change_korean_name(coininfo[0]['market'])
                if coininfo[0]['change'] == 'RISE':
                    label = Label(self.canvasFrame,font=self.tempFont,
                                  text= "["+coininfo[0]['market']+"] - "+ko_name+
                                        "  현재가:"+str(coininfo[0]['trade_price'])+"원 변화율:"+str(round(coininfo[0]['signed_change_rate']*100,2))+"%"
                                  , bg='white', foreground='red')
                    # label.bind('<Double-Button-3>',lambda event, name=coininfo[0]['market']: self.DelStar(event, name))  # 마우스 오른쪽 더블클릭
                    # label.pack()
                elif coininfo[0]['change'] == 'FALL':
                    label = Label(self.canvasFrame, font=self.tempFont,
                                  text="["+ coininfo[0]['market'] +"] - " + ko_name +
                                       "  현재가:" + str(coininfo[0]['trade_price']) + "원 변화율:" +str(round(coininfo[0]['signed_change_rate']*100,2))+"%"
                                  , bg='white', foreground='blue')
                label.bind('<Double-Button-3>',lambda event, name=coininfo[0]['market']: self.DelStar(event, name))  # 마우스 오른쪽 더블클릭
                label.pack()
            self.PrintFavoriteCoin = False
        else:
            #print All-List
            for widget in self.canvasFrame.winfo_children():
                widget.destroy()
            self.ShowAllCoins()
            self.PrintFavoriteCoin = True

        self.canvasFrame.update_idletasks()
        self.CoinCanvas.config(scrollregion=self.CoinCanvas.bbox("all"))

    def ShowCoinInfo(self, event, name):
        self.CoinName.insert(0, name)
        self.CoinSearch()
        self.CoinName.delete(0, END)
    def StarCatch(self, event, name):
        self.AddStarList(name)
    def DelStar(self, event, name):
        self.RemoveStarList(name)
    def RemoveStarList(self, name):
        response = messagebox.askyesno("즐겨찾기 제거", "즐겨찾기에서 제거 하시겠습니까?")
        if response:
            if self.User.removeStarList(name):
                messagebox.showinfo("즐찾 제거", "완료되었습니다!")
            else:
                messagebox.showinfo("즐찾 제거", "이미 존재하지 않거나 없는 코인입니다!")
    def AddStarList(self, name):
        response = messagebox.askyesno("즐겨찾기 추가", "즐겨찾기에 추가 하시겠습니까?")
        if response:
            if self.User.addStarList(name):
                messagebox.showinfo("즐찾 추가", "완료되었습니다!")
            else:
                messagebox.showinfo("즐찾 추가", "이미 존재하거나 없는 코인입니다! 또는 즐찾 개수가 10개 이상이됩니다!")

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
            label = Label(self.canvasFrame,font=self.tempFont, text='['+c['market']+'] - '+c['korean_name'], bg='white', foreground='green')
            label.pack()
            label.bind('<Double-Button-1>', lambda event, name=c['market']: self.ShowCoinInfo(event, name)) # 마우스 왼쪽 더블클릭
            label.bind('<Double-Button-3>', lambda event, name=c['market']: self.StarCatch(event, name)) # 마우스 오른쪽 더블클릭
    def Star(self):
        name = self.CoinName.get()
        self.AddStarList(name)

    def CoinSearch(self):
        self.sticklabel1.config(text='가격')
        self.sticklabel2.config(text='양')
        name = self.CoinName.get()
        fig = Figure(figsize=(6, 4), dpi= 64)
        if self.Coins.find_coin(name):
            coin = self.Coins.get_coin(name)
            df = get_ohlcv(ticker= coin['market'], count=20)
            ax = fig.add_subplot(1,1,1)
            new_idx = df.index.strftime('%d').tolist()
            ax.plot(new_idx, df['close'], label='Close Price')
            ax.set_title(self.Coins.change_market_name(name))
            if self.GraphWidget:
                self.GraphCanvas.get_tk_widget().destroy()
            else:
                self.GraphCanvas.destroy()
                self.GraphWidget = True
            self.GraphCanvas = FigureCanvasTkAgg(fig, master=self.GraphFrame)
            self.GraphCanvas.get_tk_widget().pack()
            self.GraphCanvas.draw()

    def pricePredict(self):
        name = self.CoinName.get()
        m_name = self.Coins.change_market_name(name)
        logs = get_ohlcv(ticker=m_name, count=20)
        # print(logs.get('close'))
        values = logs['close']
        print(type(values))
        s_value = values.to_string()
        psellPrice, pbuyPrice = spam.PredictPrice(s_value)
        # messagebox.showinfo("추천 매매가", "추천 매수:"+psellPrice+", 추천 매도:"+pbuyPrice)

    def Sell(self):
        name = self.CoinName.get()
        price = self.PriceEntry.get()
        volume = self.VolumeEntry.get()
        if self.MarketPrice:
            cnt = self.User.market_sell(name, price)
            if  0 > cnt:
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
        else:
            cnt = self.User.limit_sell(name, price, volume)
            if 0 > cnt:
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
        self.PrintCurrentCash()
    def Buy(self):
        name = self.CoinName.get()
        price = self.PriceEntry.get()
        volume = self.VolumeEntry.get()
        cnt = self.User.market_buy(name, price)
        if self.MarketPrice:
            if 0 > self.User.market_buy(name, price):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!(!'+str(cnt))
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
        else:
            if -1 == self.User.limit_buy(name, price, volume):
                self.sticklabel1.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
                self.sticklabel2.config(text='Error!!!!!!!!!!!!!!!!!'+str(cnt))
        self.PrintCurrentCash()

MAINGUI()