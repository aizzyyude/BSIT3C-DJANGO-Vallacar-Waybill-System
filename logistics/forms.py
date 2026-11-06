
from django import forms
from django.forms import modelform_factory

from .models import (
    Customer, Bus, Driver, Route,
    BusTrip, Shipment, Payment
)


def get_record_form(model):

    class StyledForm(forms.ModelForm):

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

            for field in self.fields.values():
                field.widget.attrs["class"] = "form-control"

        class Meta:
            fields = "__all__"

    return modelform_factory(
        model,
        form=StyledForm,
        fields="__all__"
    )


MODEL_FORMS = {
    "customers": get_record_form(Customer),
    "buses": get_record_form(Bus),
    "drivers": get_record_form(Driver),
    "routes": get_record_form(Route),
    "trips": get_record_form(BusTrip),
    "waybills": get_record_form(Shipment),
    "payments": get_record_form(Payment),
}
