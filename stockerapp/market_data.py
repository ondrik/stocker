# A module providing market data

# we're using IEX Cloud
import iexfinance.stocks as iexstocks

# token for communicating with the IEX cloud
IEX_TOKEN='pk_599e4f6600584aa28e5aac9f10956ffd'

###########################################
def get_iex_stock(ticker):
    """get_iex_stock(ticker) -> iexstocks.Stock

Gets a stock with the given ticker.
"""
    return iexstocks.Stock(ticker, output_format='json', token=IEX_TOKEN)


###########################################
def get_company_info(ticker):
    """get_company_info(ticker) -> dict

Gets information about a~company and returns it using a dictionary.
"""
    res = dict()
    iex_stock = get_iex_stock(ticker)

    try:
        res['logo_url'] = iex_stock.get_logo()['url']
        company = iex_stock.get_company()
        res = dict(res, **company)
    except:
        assert False

    return res


###########################################
def get_daily_data(ticker, start, end=None):
    """get_daily_data(ticker, start, end) -> Pandas Data Frame

Gets daily data (open, close, high, low, volume) for days in the range
from start to end as a Panda's Data Frame.
"""
    try:
        # TODO: CACHE
        return iexstocks.get_historical_data(
            ticker,
            start=start,
            end=end,
            output_format='pandas',
            token=IEX_TOKEN)
    except:
        assert False


###########################################
def get_intraday_data(ticker, date=None):
    """get_intraday_data(ticker, date) -> Pandas Data Frame

Gets intraday data (open, close, high, low, volume) for date as a Panda's Data
Frame.
"""
    try:
        # TODO: CACHE
        return iexstocks.get_historical_intraday(
            ticker,
            date=date,
            output_format='pandas',
            token=IEX_TOKEN)
    except:
        assert False


###########################################
def refresh_stock_daily_cache(ticker):
    """refresh_stock_daily_cache(ticker) -> ()

Refreshes stock's daily data (if required)
"""
    # todo



    return


###########################################
def refresh_stock_intraday_cache(ticker):
    """refresh_stock_intraday_cache(ticker) -> ()

Refreshes stock's intraday data (if required)
"""
    # todo



    return

###########################################
def get_stock_price(ticker):
    """get_stock_price(ticker) -> price

Gets the current price of the stock with 'ticker'.
"""






    return 42

    # not working
    if False:
        iex_stock = get_iex_stock(ticker)
        return iex_stock.get_price()
