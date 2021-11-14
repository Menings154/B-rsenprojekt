from Classes import *
from selenium import webdriver
from googlesearch import search
import requests
from bs4 import BeautifulSoup

sandp = Sandp500()
sandp.scrap_tickers()

dic_crv = {}
for ticker in sandp.tickers:
    try:
        df = sandp.load_stock(ticker)
        crv = sandp.calculate_crv(df)
        if crv >= 3:
            dic_crv[ticker] = crv
    except KeyError:
        pass

crv_names = []
for ticker in dic_crv.keys():
    index = sandp.tickers.index(ticker)
    crv_names.append(sandp.names[index])

# Ersten 5 Googleergebnisse als links speichern und dann per Email senden

links = []
for count, name in enumerate(crv_names):
    links.append([])
    for j in search(name, num=5, stop=5, pause=2):
        links[count].append(j)

body = f'Here are todays recomendations:\r'
for count, name in enumerate(crv_names):
    body += f'{name}: CRV = {dic_crv[data.tickers[count]]}\r'
    for i in links[count]:
        body += f'{i}\r'
body += '\r'
body += 'Hope the mail is useful!'

data.send_mail(email='zenz.finanzen@gmail.com', subject='Good stocks', body=body)
