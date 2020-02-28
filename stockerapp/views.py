from django.http import HttpResponse
from django.shortcuts import render

import iexfinance.stocks as iexstocks
import pandas as pd
import bokeh.plotting as bkplt
import bokeh.embed as bkem

from datetime import datetime, date, timedelta


from .models import Stock

# index
def index(request):
    stock_list = Stock.objects.order_by('ticker')
    context = {
        'stock_list': stock_list
    }
    return render(request, 'stockerapp/index.html', context)

# stock information
def stockinfo(request, ticker):
    IEX_TOKEN='pk_599e4f6600584aa28e5aac9f10956ffd'

    stock = Stock(ticker=ticker)

    context = {
        'stock': stock
    }

    end = date.today()
    start = end - timedelta(days=30)
    df = iexstocks.get_historical_data(ticker, start, end, output_format='pandas',
                                     token=IEX_TOKEN)

    plot = bkplt.figure(plot_width=400, plot_height=400)

    # x = [1,2,3,4,5]
    # y = [1,2,3,4,5]
    # plot.line(x, y, line_width=2)
    plot.line(df.index, df['close'], line_width=2)

    plot_script, plot_img = bkem.components(plot)

    debug_str = ""
    context = {
        'stock': stock,
        'plot_script': plot_script,
        'plot_img': plot_img,
        'df': df.to_html(),
        'debug_str': debug_str
    }

    return render(request, 'stockerapp/stockinfo.html', context)
