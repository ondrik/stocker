from django.contrib import admin

from .models import Stock
from .models import Order

admin.site.register(Stock)
admin.site.register(Order)
