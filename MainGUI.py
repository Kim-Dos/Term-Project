from tkinter import *
from UpbitParsing import *
class MAINGUI:
    PrinFavoriteCoin = False
    def __init__(self):
        self.window = Tk()
        self.window.geometry('1200x900')


        self.PrintCoinButton = Button(self.window, width= 40,height=2, text='모든 코인 / 즐겨 찾기', command=self.GetCoinData)
        self.PrintCoinButton.pack(side='top', anchor='sw')

        self.CoinName = Entry(self.window, width=40, )
        self.CoinName.pack(side='right', anchor='ne')
        self.SearchCoinButton = Button(self.window, text='검색', height= 2, command=self.CoinSearch)
        self.SearchCoinButton.pack(self.window, side='right', anchor='ne')


        self.SellButton = Button(self.window, text='매수', command=self.Sell)
        self.BuyButton = Button(self.window, text='매도', command=self.Buy)


        self.window.mainloop()
    def GetCoinData(self):
        pass

    def CoinSearch(self):
        pass

    def Sell(self):
        pass
    def Buy(self):
        pass

MAINGUI()