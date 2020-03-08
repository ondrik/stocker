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
        return stock.ticker + \
            ", amount: " + str(self.amount) + \
            ", unit price: " + str(self.unit_price) + \
            ", fee: " + str(fee) + \
            ", date: " + str(date)
