# A module providing a proxy for the IEX Cloud

import iexfinance.stocks as iexstocks

# token for communicating with the IEX cloud
IEX_TOKEN='pk_599e4f6600584aa28e5aac9f10956ffd'

###########################################
def get_company_info(ticker):
    """get_company_info(ticker) -> dict

Gets information about a~company and returns it using a dictionary.
"""
    res = dict()
    iex_stock = iexstocks.Stock(ticker, output_format='json', token=IEX_TOKEN)

    try:
        res['logo_url'] = iex_stock.get_logo()['url']
        company = iex_stock.get_company()
        res = dict(res, **company)
    except:
        assert False

    return res


###########################################
def get_historical_data(ticker, start, end=None):
    """get_historical_data(ticker, start, end) -> Pandas Data Frame

Gets historical data (open, close, high, low, volume) for days in the range
from start to end as a Panda's Data Frame.
"""
    try:
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
        return iexstocks.get_historical_intraday(
            ticker,
            date=date,
            output_format='pandas',
            token=IEX_TOKEN)
    except:
        assert False
