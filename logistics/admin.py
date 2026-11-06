
from django.contrib import admin

from .models import (
    Customer,
    Bus,
    Driver,
    Route,
    BusTrip,
    Shipment,
    Payment,
)


admin.site.register(Customer)
admin.site.register(Bus)
admin.site.register(Driver)
admin.site.register(Route)
admin.site.register(BusTrip)
admin.site.register(Shipment)
admin.site.register(Payment)
