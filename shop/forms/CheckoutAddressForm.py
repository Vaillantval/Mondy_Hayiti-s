from django import forms
from dashboard.models.Adress import Adress


class CheckoutAddressForm(forms.ModelForm):
    ADDRESS_TYPE_CHOICES = [("billing", "Billing"), ("shipping", "Shipping")]
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))

    address_type = forms.ChoiceField(
        choices=ADDRESS_TYPE_CHOICES,
        widget=forms.Select(attrs={"class": "form-control custom-text-input"}),
    )

    class Meta:
        model = Adress
        fields = (
            "email",
            "full_name",
            "phone",
            "street",
            "city",
            "more_details",
            "address_type",
        )

        widgets = {
            "full_name": forms.TextInput(
                attrs={"class": "form-control custom-text-input"}
            ),
            "street": forms.TextInput(
                attrs={"class": "form-control custom-text-input"}
            ),
            "city": forms.TextInput(attrs={"class": "form-control custom-text-input"}),
            "phone": forms.TextInput(
                attrs={"class": "form-control custom-text-input", "id": "id_phone"}
            ),
            "more_details": forms.Textarea(
                attrs={"class": "form-control custom-textarea"}
            ),
        }
