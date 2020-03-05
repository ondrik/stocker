from django.http import HttpResponse
from django.shortcuts import render

import iexfinance.stocks as iexstocks
import pandas as pd

from datetime import datetime, date, timedelta


from .models import Stock
from .plotting import plot_candlestick

# token for communicating with the IEX cloud
IEX_TOKEN='pk_599e4f6600584aa28e5aac9f10956ffd'

# index
def index(request):
    stock_list = Stock.objects.order_by('ticker')
    context = {
        'stock_list': stock_list
    }
    return render(request, 'stockerapp/index.html', context)

# stock information
def stockinfo(request, ticker):

    stock = Stock(ticker=ticker)


    # iex_stock = iexstocks.Stock(stock.ticker, output_format='pandas', token=IEX_TOKEN)
    iex_stock = iexstocks.Stock(stock.ticker, output_format='json', token=IEX_TOKEN)
    logo_url = iex_stock.get_logo()['url']
    company = iex_stock.get_company()

    end = date.today()
    start = end - timedelta(days=60)
    df = iexstocks.get_historical_data(stock.ticker, start, end, output_format='pandas',
                                     token=IEX_TOKEN)
    df["time"] = df.index

    delta = timedelta(days=1)
    plot_script, plot_img = plot_candlestick(df, res=delta, width=1200, height=400)

    debug_str = ""
    debug_str += str(iex_stock) + "\n"
    debug_str += str(logo_url)
    context = {
        'company_name': company['companyName'],
        'stock': stock,
        'stock_img' : logo_url,
        # 'cur_price': iex_stock,
        'plot_script': plot_script,
        'plot_img': plot_img,
        'df': df.to_html(),
        'debug_str': debug_str
    }

    return render(request, 'stockerapp/stockinfo.html', context)

# stock daily information
def stockdaily(request, ticker):
    stock = Stock(ticker=ticker)

    iex_stock = iexstocks.Stock(stock.ticker, output_format='json', token=IEX_TOKEN)
    logo_url = iex_stock.get_logo()['url']
    company = iex_stock.get_company()

    df = iexstocks.get_historical_intraday(stock.ticker, output_format='pandas',
                                     token=IEX_TOKEN)
    df["time"] = df.index

    delta = timedelta(minutes=1)
    plot_script, plot_img = plot_candlestick(df, res=delta, width=1200, height=400)

    debug_str = ""
    debug_str += str(iex_stock) + "\n"
    debug_str += str(logo_url)
    context = {
        'company_name': company['companyName'],
        'stock': stock,
        'stock_img' : logo_url,
        # 'cur_price': iex_stock,
        'plot_script': plot_script,
        'plot_img': plot_img,
        'df': df.to_html(),
        'debug_str': debug_str
    }

    return render(request, 'stockerapp/stockdaily.html', context)
