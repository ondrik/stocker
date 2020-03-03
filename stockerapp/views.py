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


    # iex_stock = iexstocks.Stock(stock.ticker, output_format='pandas', token=IEX_TOKEN)
    iex_stock = iexstocks.Stock(stock.ticker, output_format='json', token=IEX_TOKEN)
    logo_url = iex_stock.get_logo()['url']
    company = iex_stock.get_company()

    end = date.today()
    start = end - timedelta(days=60)
    df = iexstocks.get_historical_data(stock.ticker, start, end, output_format='pandas',
                                     token=IEX_TOKEN)
    df["date"] = df.index

    plot = bkplt.figure(
            x_axis_type='datetime',
            plot_width=1200,
            plot_height=400)

    # x = [1,2,3,4,5]
    # y = [1,2,3,4,5]
    # plot.line(x, y, line_width=2)
    # plot.line(df.index, df['close'], line_width=2)
    inc = df.close > df.open
    dec = df.open > df.close
    w = 12*60*60*1000 # half day in ms

    plot.segment(df.date, df.high, df.date, df.low, color="black")
    plot.vbar(df.date[inc], w, df.open[inc], df.close[inc], fill_color="#D5E1DD", line_color="black")
    plot.vbar(df.date[dec], w, df.open[dec], df.close[dec], fill_color="#F2583E", line_color="black")


    plot_script, plot_img = bkem.components(plot)

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
