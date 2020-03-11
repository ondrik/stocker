from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from datetime import datetime, date, timedelta

# required models
from .models import Stock, Order, Portfolio

from .plotting import plot_candlestick
from .iex_proxy import get_company_info, get_historical_data, get_intraday_data


# index
def index(request):
    stock_list = Stock.objects.order_by('ticker')
    portfolio_list = Portfolio.objects.order_by('name')
    context = {
        'stock_list': stock_list,
        'portfolio_list': portfolio_list,
    }
    return render(request, 'stockerapp/index.html', context)


# stock information
def stockinfo(request, ticker):

    stock = get_object_or_404(Stock, ticker=ticker)

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
    stock = get_object_or_404(Stock, ticker=ticker)

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


# information about portfolio
def portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    stocks = Stock.objects.order_by('ticker')
    orders = portfolio.order_set.all()
    context = {
        'portfolio': portfolio,
        'stock_list': stocks,
        'order_list': orders
    }

    return render(request, 'stockerapp/portfolio.html', context)


# adding a new order
def new_order(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    stock = get_object_or_404(Stock, ticker=request.POST["ticker"])
    datetime_str = request.POST["datetime"]
    try:
        date = datetime.strptime(datetime_str, '%d.%m.%Y %H:%M:%S')
    except:
        assert False

    newOrd = Order()
    newOrd.stock = stock
    newOrd.portfolio = portfolio
    newOrd.amount = request.POST["amount"]
    newOrd.unit_price = request.POST["unit_price"]
    newOrd.fee = request.POST["fee"]
    newOrd.date = date
    newOrd.save()

    return HttpResponseRedirect(reverse('stockerapp:portfolio', args=(portfolio_id,)))
