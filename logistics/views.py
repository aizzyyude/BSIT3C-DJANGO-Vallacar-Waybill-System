
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum

from .models import (
    Shipment,
    Bus,
    Driver,
    Route,
    BusTrip,
    Customer,
    Payment,
)

from .forms import MODEL_FORMS


MODULES = {
    "waybills": {
        "model": Shipment,
        "title": "Waybills & Shipments",
        "search": [
            "waybill_number",
            "receiver_name",
            "destination",
        ],
        "columns": [
            "waybill_number",
            "sender",
            "receiver_name",
            "destination",
            "weight",
            "status",
        ],
    },
    "buses": {
        "model": Bus,
        "title": "Buses",
        "search": ["bus_number", "plate_number"],
        "columns": [
            "bus_number", "plate_number", "bus_type",
            "capacity", "status"
        ],
    },
    "drivers": {
        "model": Driver,
        "title": "Drivers",
        "search": ["driver_name", "license_number"],
        "columns": [
            "driver_name", "license_number", "phone", "status"
        ],
    },
    "routes": {
        "model": Route,
        "title": "Routes",
        "search": ["route_name", "origin", "destination"],
        "columns": [
            "route_name", "origin", "destination",
            "distance", "fare"
        ],
    },
    "trips": {
        "model": BusTrip,
        "title": "Bus Trips",
        "search": ["bus__bus_number", "driver__driver_name"],
        "columns": [
            "bus", "driver", "route",
            "departure_time", "status"
        ],
    },
    "customers": {
        "model": Customer,
        "title": "Customers",
        "search": ["customer_name", "phone", "email"],
        "columns": [
            "customer_name", "phone", "email", "address"
        ],
    },
    "payments": {
        "model": Payment,
        "title": "Payments",
        "search": ["reference_number", "shipment__waybill_number"],
        "columns": [
            "shipment", "amount", "payment_method",
            "payment_status", "payment_date"
        ],
    },
}


@login_required
def dashboard(request):

    shipments = Shipment.objects.all()

    context = {
        "total_shipments": shipments.count(),
        "transit_shipments": shipments.filter(
            status="In Transit"
        ).count(),
        "delivered_shipments": shipments.filter(
            status="Delivered"
        ).count(),
        "pending_shipments": shipments.filter(
            status="Pending"
        ).count(),
        "cancelled_shipments": shipments.filter(
            status="Cancelled"
        ).count(),

        "total_buses": Bus.objects.count(),
        "total_routes": Route.objects.count(),
        "total_drivers": Driver.objects.count(),
        "total_customers": Customer.objects.count(),

        "total_revenue": Payment.objects.filter(
            payment_status="Paid"
        ).aggregate(total=Sum("amount"))["total"] or 0,

        "recent_shipments": shipments.select_related(
            "sender", "route", "trip"
        )[:10],
    }

    context["chart_data"] = {
        "delivered": context["delivered_shipments"],
        "transit": context["transit_shipments"],
        "pending": context["pending_shipments"],
        "cancelled": context["cancelled_shipments"],
    }

    return render(request, "dashboard.html", context)


def get_module(module):
    if module not in MODULES:
        return None
    return MODULES[module]


@login_required
def record_list(request, module):

    config = get_module(module)

    if not config:
        return redirect("dashboard")

    model = config["model"]
    records = model.objects.all()
    query = request.GET.get("q", "").strip()

    if query:
        search_filter = Q()

        for field in config["search"]:
            search_filter |= Q(**{f"{field}__icontains": query})

        records = records.filter(search_filter)

    records = records.order_by("-pk")

    return render(request, "record_list.html", {
        "module": module,
        "title": config["title"],
        "records": records,
        "columns": config["columns"],
        "query": query,
    })


@login_required
def record_create(request, module):

    config = get_module(module)

    if not config:
        return redirect("dashboard")

    model = config["model"]
    FormClass = MODEL_FORMS[module]

    if request.method == "POST":
        form = FormClass(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, "Record successfully added.")
            return redirect("record_list", module=module)
    else:
        form = FormClass()

    return render(request, "record_form.html", {
        "form": form,
        "title": "Add " + config["title"],
        "module": module,
    })


@login_required
def record_edit(request, module, pk):

    config = get_module(module)

    if not config:
        return redirect("dashboard")

    record = get_object_or_404(config["model"], pk=pk)
    FormClass = MODEL_FORMS[module]

    if request.method == "POST":
        form = FormClass(request.POST, instance=record)

        if form.is_valid():
            form.save()
            messages.success(request, "Record updated successfully.")
            return redirect("record_list", module=module)
    else:
        form = FormClass(instance=record)

    return render(request, "record_form.html", {
        "form": form,
        "title": "Edit " + config["title"],
        "module": module,
    })


@login_required
def record_delete(request, module, pk):

    config = get_module(module)

    if not config:
        return redirect("dashboard")

    record = get_object_or_404(config["model"], pk=pk)

    if request.method == "POST":
        try:
            record.delete()
            messages.success(request, "Record deleted successfully.")
        except Exception:
            messages.error(
                request,
                "Cannot delete this record because it is linked to other records."
            )

        return redirect("record_list", module=module)

    return render(request, "record_delete.html", {
        "record": record,
        "title": config["title"],
        "module": module,
    })

    def map_view(request):
        return render(request, 'map.html')



@login_required
def reports(request):

    return render(request, "record_list.html", {
        "module": "reports",
        "title": "Reports",
        "records": Shipment.objects.all(),
        "columns": [
            "waybill_number",
            "sender",
            "destination",
            "shipping_fee",
            "status",
        ],
        "query": "",
        "is_report": True,

        
    })
    