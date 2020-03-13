from django.db import models

from .iex_proxy import get_company_info


# A class representing a stock
class Stock(models.Model):
    ticker = models.CharField(max_length=10)
    company_name = models.CharField(max_length=200, default="")
    logo_url = models.CharField(max_length=200, default="")

    # conversion to string
    def __str__(self):
        return self.ticker + ": " + self.company_name

    # update the model
    def refresh_info(self):
        try:
            company_info = get_company_info(self.ticker)
            self.company_name = company_info["companyName"]
            self.logo_url = company_info["logo_url"]
            self.save()
        except:
            assert False


# A class representing a portfolio of stocks
class Portfolio(models.Model):
    name = models.CharField(max_length=100)

    # conversion to string
    def __str__(self):
        return self.name

    # get all stocks currently held
    def get_current_stocks(self):
        cur_stocks = dict()
        orders = self.order_set.all()
        for order in orders:
            ticker = order.stock.ticker
            # first time adding the ticker
            if not ticker in cur_stocks:
                cur_stocks[ticker] = {'stock': order.stock, 'amount': order.amount}
            else:
                cur_stocks[ticker]['amount'] += order.amount

        cur_stocks = {key:value for (key,value) in cur_stocks.items() if value['amount'] != 0}

        return cur_stocks


# A class representing a buying or selling order
class Order(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=20, decimal_places=6)
    fee = models.DecimalField(max_digits=20, decimal_places=6)
    date = models.DateTimeField("Execution date and time")

    # conversion to string
    def __str__(self):
        return self.stock.ticker + \
            ", amount: " + str(self.amount) + \
            ", unit price: " + str(self.unit_price) + \
            ", fee: " + str(self.fee) + \
            ", date: " + str(self.date)
