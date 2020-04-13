import calendar

import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup


# https://finance.yahoo.com/quote/NVDA?p=NVDA
# https://finance.yahoo.com/quote/AAPL/key-statistics?p=AAPL&.tsrc=fin-srch

class metrics:
    def __init__(self, comp):
        self.url = ('https://finance.yahoo.com/quote/' + comp 
                        + '?p=' + comp)
        
        parse_html_url = urlopen(self.url)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_1 = BeautifulSoup(html_page, "html.parser")

        
        self.url_2 = ('https://finance.yahoo.com/quote/' + comp 
                        + '/key-statistics?p=' + comp)
        parse_html_url = urlopen(self.url_2)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_2 = BeautifulSoup(html_page, "html.parser")
        
        # 10-Day alphaquery
        self.url_3 = ('https://www.alphaquery.com/stock/' + comp + 
                     '/volatility-option-statistics/10-day/put-call-ratio-volume')
        parse_html_url = urlopen(self.url_3)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_3 = BeautifulSoup(html_page, "html.parser")
        
        # 30-Day alphaquery
        self.url_4 = ('https://www.alphaquery.com/stock/' + comp + 
                     '/volatility-option-statistics/30-day/put-call-ratio-volume')
        parse_html_url = urlopen(self.url_4)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_4 = BeautifulSoup(html_page, "html.parser")
        
        # 60-Day alphaquery
        self.url_5 = ('https://www.alphaquery.com/stock/' + comp + 
                     '/volatility-option-statistics/60-day/put-call-ratio-volume')
        parse_html_url = urlopen(self.url_5)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_5 = BeautifulSoup(html_page, "html.parser")
        
        self.url_6 = ('https://ycharts.com/indicators/10_year_treasury_rate')
        parse_html_url = urlopen(self.url_6)
        html_page = parse_html_url.read()
        parse_html_url.close()
        self.soup_page_6 = BeautifulSoup(html_page, "html.parser")
        
    # volume
    def volume(self):
        val = self.soup_page_1.findAll("td", {"data-test": "TD_VOLUME-value"})
        val = str(val).split('</')[0]
        val = str(val).split('reactid')[2]
        val = str(val).split('>')[1]
        val = val.split(',')
        val = val[0] + val[1]
        val = float(val)
        return val
    
    # equity movement w.r.t. S&P 500
    def beta(self):
        val = self.soup_page_1.findAll("td", {'data-test': 'BETA_5Y-value'})
        val = str(val).split('span')[1]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    
    # price / earnings
    def pe(self):
        val = self.soup_page_1.findAll("td", {'data-test': 'PE_RATIO-value'})
        val = str(val).split('span')[1]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    
    # earnings per share
    def eps(self):
        val = self.soup_page_1.findAll("td", {'data-test': 'EPS_RATIO-value'})
        val = str(val).split('span')[1]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    
    # for some reason the wrangled earnings date is 
    # one day before the one listed **fix**
    def earnings_date(self):
        val = self.soup_page_1.findAll("td", {'data-test': 'EARNINGS_DATE-value'})
        val = str(val).split('span')[1]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = str(val)
        return val
    
    # dividend (in percentage)
    def div(self):
        # dividend in percent
        val = self.soup_page_1.findAll("td", {"data-test": "DIVIDEND_AND_YIELD-value"})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = val.split('(')[1]
        val = val.split('%')[0]
        val = float(val)
        return val
    
    
    # market capitlaization 
    def mktCap(self):
        val = self.soup_page_2.findAll("td", {'class': 'Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
        val = self.soup_page_2.findAll("td", {'data-reactid': '20'})
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        try:
            val = val.strip('M')
            val = float(val)
        except Exception:
            try:
                val = val.strip('B')
                val = float(val)
            except Exception:
                val = val.strip('T')
                val = float(val)
        return val
    
    # enterprise value
    def entValuation(self):        
        val = self.soup_page_2.findAll("td", {'class': 'Fz(s) Fw(500) Ta(end) Pstart(10px) Miw(60px)'})
        val = self.soup_page_2.findAll("td", {'data-reactid': '27'})
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        try:
            val = val.strip('M')
            val = float(val)
        except Exception:
            try: 
                val = val.strip('B')
                val = float(val)
            except Exception:
                val = val.strip('T')
                val = float(val)
        return val
    
    # price / earnings growth ratio (great: 0.0-0.5, terrible: 2.0 <)
    def PEG(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '53'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = float(val)
        return val
    
    # price/sales
    def ps(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '61'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = float(val)
        return val
    
    # price/book
    def pb(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '69'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = float(val)
        return val
    
    # 50-day moving average
    def fifty_ma(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '142'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = float(val)
        return val
    
    # 200-day moving average
    def two_hund_ma(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '149'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        val = float(val)
        return val
    
    # average volume over the last 3 mnth period
    def avg_vol_three_mnth(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '162'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        try:
            val = val.strip('M')
            val = float(val)
        except Exception:
            try:
                val = val.strip('B')
                val = float(val)
            except Exception:
                val = val.strip('T')
                val = float(val)
        return val
    
    # average volume over the last 10 day period
    def avg_vol_ten_day(self):
        val = self.soup_page_2.findAll("td", {'data-reactid': '169'})
        val = str(val).split('>')[1]
        val = val.split('<')[0]
        try:
            val = val.strip('M')
            val = float(val)
        except Exception:
            try:
                val = val.strip('B')
                val = float(val)
            except Exception:
                val = val.strip('T')
                val = float(val)
        return val
    
    # Put-Call Ratio 
    # 1.0 > x > 0.7 :: bearish (market will move lower)
    # 0.5 < x < 0.7 :: bullish (market will move higher)
    #
    # put-call ratio 10-Day (volume)
    def pcr_10(self):
        val = self.soup_page_3.findAll("div", {"class": "indicator-figure-inner"})
        val = val[7]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    #
    # put-call ratio 30-Day (volume)
    def pcr_30(self):
        val = self.soup_page_4.findAll("div", {"class": "indicator-figure-inner"})
        val = val[7]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    #
    # put-call ratio 60-Day (volume)
    def pcr_60(self):
        val = self.soup_page_5.findAll("div", {"class": "indicator-figure-inner"})
        val = val[7]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = float(val)
        return val
    
    # risk-free rate (%)
    def riskFreeRate(self):
        val = self.soup_page_6.findAll("td", {"class": "col2"})[0]
        val = str(val).split('>')[1]
        val = str(val).split('<')[0]
        val = str(val).split('%')[0]
        val = str(val).strip('\n')
        val = float(val)
        return val
    
