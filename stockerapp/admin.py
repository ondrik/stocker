from django.contrib import admin

from .models import *

admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Portfolio)
admin.site.register(StockDailyData)
