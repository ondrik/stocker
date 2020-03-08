from django.contrib import admin

from .models import Stock
from .models import Order
from .models import Portfolio

admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Portfolio)
