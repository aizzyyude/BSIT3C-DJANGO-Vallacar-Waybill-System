
from django.db import models
from django.utils import timezone


class Customer(models.Model):
    customer_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    address = models.TextField()

    def __str__(self):
        return self.customer_name

    class Meta:
        ordering = ["customer_name"]


class Bus(models.Model):
    bus_number = models.CharField(max_length=50, unique=True)
    plate_number = models.CharField(max_length=30, unique=True)
    bus_type = models.CharField(max_length=80)
    capacity = models.PositiveIntegerField(default=0)

    status = models.CharField(
        max_length=30,
        choices=[
            ("Available", "Available"),
            ("On Trip", "On Trip"),
            ("Maintenance", "Maintenance"),
        ],
        default="Available"
    )

    def __str__(self):
        return self.bus_number


class Driver(models.Model):
    driver_name = models.CharField(max_length=150)
    license_number = models.CharField(max_length=80, unique=True)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True)

    status = models.CharField(
        max_length=30,
        choices=[
            ("Available", "Available"),
            ("On Trip", "On Trip"),
        ],
        default="Available"
    )

    def __str__(self):
        return self.driver_name


class Route(models.Model):
    route_name = models.CharField(max_length=150)
    origin = models.CharField(max_length=150)
    destination = models.CharField(max_length=150)
    distance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    fare = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return f"{self.origin} - {self.destination}"


class BusTrip(models.Model):
    bus = models.ForeignKey(
        Bus,
        on_delete=models.PROTECT
    )

    driver = models.ForeignKey(
        Driver,
        on_delete=models.PROTECT
    )

    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT
    )

    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(
        max_length=30,
        choices=[
            ("Scheduled", "Scheduled"),
            ("Departed", "Departed"),
            ("Completed", "Completed"),
            ("Cancelled", "Cancelled"),
        ],
        default="Scheduled"
    )

    def __str__(self):
        return f"{self.bus} - {self.route}"


class Shipment(models.Model):

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Transit", "In Transit"),
        ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]

    waybill_number = models.CharField(
        max_length=50,
        unique=True
    )

    sender = models.ForeignKey(
        Customer,
        on_delete=models.PROTECT,
        related_name="sent_shipments"
    )

    receiver_name = models.CharField(max_length=150)
    receiver_phone = models.CharField(max_length=20)

    destination = models.CharField(max_length=150)

    route = models.ForeignKey(
        Route,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    trip = models.ForeignKey(
        BusTrip,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    cargo_description = models.TextField()

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    shipping_fee = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.waybill_number

    class Meta:
        ordering = ["-created_at"]


class Payment(models.Model):

    shipment = models.ForeignKey(
        Shipment,
        on_delete=models.PROTECT
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        choices=[
            ("Cash", "Cash"),
            ("GCash", "GCash"),
            ("Bank Transfer", "Bank Transfer"),
        ],
        default="Cash"
    )

    payment_status = models.CharField(
        max_length=30,
        choices=[
            ("Paid", "Paid"),
            ("Partial", "Partial"),
            ("Unpaid", "Unpaid"),
        ],
        default="Unpaid"
    )

    payment_date = models.DateField(default=timezone.localdate)

    reference_number = models.CharField(
        max_length=100,
        blank=True
    )

    def __str__(self):
        return f"Payment - {self.shipment.waybill_number}"
