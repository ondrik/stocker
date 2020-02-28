from django.db import models


# A class representing a stock
class Stock(models.Model):
    ticker = models.CharField(max_length=10)

    def __str__(self):
        return self.ticker



class Order(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    unit_price = models.DecimalField(max_digits=20, decimal_places=6)
    fee = models.DecimalField(max_digits=20, decimal_places=6)
    date = models.DateTimeField('Execution date and time')

    def __str__(self):
        return stock.ticker + \
            ", amount: " + str(self.amount) + \
            ", unit price: " + str(self.unit_price) + \
            ", fee: " + str(fee) + \
            ", date: " + str(date)
