from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd

from datetime import datetime, date, timedelta

from .models import Stock
from .plotting import plot_candlestick
from .iex_proxy import get_company_info, get_historical_data, get_intraday_data

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
    # iex_stock = iexstocks.Stock(stock.ticker, output_format='json', token=IEX_TOKEN)
    company = get_company_info(stock.ticker)
    # logo_url = iex_stock.get_logo()['url']
    # company = iex_stock.get_company()

    end = date.today()
    start = end - timedelta(days=60)
    df = get_historical_data(stock.ticker, start, end)
    df["time"] = df.index

    delta = timedelta(days=1)
    plot_script, plot_img = plot_candlestick(df, res=delta, width=1200, height=400)

    debug_str = ""
    context = {
        'company_name': company['companyName'],
        'stock': stock,
        'stock_img' : company['logo_url'],
        'plot_script': plot_script,
        'plot_img': plot_img,
        'df': df.to_html(),
        'debug_str': debug_str
    }

    return render(request, 'stockerapp/stockinfo.html', context)

# stock daily information
def stockdaily(request, ticker):
    stock = Stock(ticker=ticker)

    # iex_stock = iexstocks.Stock(stock.ticker, output_format='json', token=IEX_TOKEN)
    company = get_company_info(stock.ticker)
    # logo_url = iex_stock.get_logo()['url']
    # company = iex_stock.get_company()

    df = get_intraday_data(stock.ticker)
    df["time"] = df.index

    delta = timedelta(minutes=1)
    plot_script, plot_img = plot_candlestick(df, res=delta, width=1200, height=400)

    debug_str = ""
    context = {
        'company_name': company['companyName'],
        'stock': stock,
        'stock_img' : company['logo_url'],
        'plot_script': plot_script,
        'plot_img': plot_img,
        'df': df.to_html(),
        'debug_str': debug_str
    }

    return render(request, 'stockerapp/stockdaily.html', context)
