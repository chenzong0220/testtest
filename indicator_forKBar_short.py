import requests, datetime, os, time
import numpy as np
import matplotlib.dates as mdates
# from talib.abstract import *  # 若需要技術指標可解開此行

# 算K棒
class KBar():
    def __init__(self, date, cycle=1):
        # K棒的頻率（分鐘）
        self.TAKBar = {
            'time': np.array([]),
            'open': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
            'close': np.array([]),
            'volume': np.array([])
        }
        self.current = datetime.datetime.strptime(date + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        self.cycle = datetime.timedelta(minutes=cycle)

    def AddPrice(self, time, open_price, close_price, low_price, high_price, volume):
        # 若尚未建立任何 KBar（避免 IndexError）
        if self.TAKBar['time'].size == 0:
            self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
            self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
            self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
            self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
            self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
            self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 1

        # 同一根K棒
        if time <= self.current:
            self.TAKBar['close'][-1] = close_price
            self.TAKBar['volume'][-1] += volume
            self.TAKBar['high'][-1] = max(self.TAKBar['high'][-1], high_price)
            self.TAKBar['low'][-1] = min(self.TAKBar['low'][-1], low_price)
            return 0
        else:
            # 跨過多個週期，更新 self.current
            while time > self.current:
                self.current += self.cycle
            self.TAKBar['time'] = np.append(self.TAKBar['time'], self.current)
            self.TAKBar['open'] = np.append(self.TAKBar['open'], open_price)
            self.TAKBar['high'] = np.append(self.TAKBar['high'], high_price)
            self.TAKBar['low'] = np.append(self.TAKBar['low'], low_price)
            self.TAKBar['close'] = np.append(self.TAKBar['close'], close_price)
            self.TAKBar['volume'] = np.append(self.TAKBar['volume'], volume)
            return 1

    def GetTime(self):
        return self.TAKBar['time']

    def GetOpen(self):
        return self.TAKBar['open']

    def GetHigh(self):
        return self.TAKBar['high']

    def GetLow(self):
        return self.TAKBar['low']

    def GetClose(self):
        return self.TAKBar['close']

    def GetVolume(self):
        return self.TAKBar['volume']




            
