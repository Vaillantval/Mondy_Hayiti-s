from django import forms
from dashboard.models.Adress import Adress

PLACEHOLDER = {
    'full_name':    'Prénom et nom',
    'street':       'Numéro et nom de rue',
    'city':         'Ville',
    'more_details': 'Appartement, étage, instructions de livraison…',
}

class AdressForm(forms.ModelForm):
    class Meta:
        model  = Adress
        fields = ('full_name', 'phone', 'street', 'city', 'more_details', 'adress_type')
        widgets = {
            'full_name':    forms.TextInput(attrs={'class': 'ds-input', 'placeholder': PLACEHOLDER['full_name']}),
            'street':       forms.TextInput(attrs={'class': 'ds-input', 'placeholder': PLACEHOLDER['street']}),
            'city':         forms.TextInput(attrs={'class': 'ds-input', 'placeholder': PLACEHOLDER['city']}),
            'phone':        forms.TextInput(attrs={'class': 'ds-input', 'id': 'id_phone_hidden'}),
            'more_details': forms.Textarea(attrs={'class': 'ds-input ds-textarea', 'placeholder': PLACEHOLDER['more_details'], 'rows': 3}),
            'adress_type':  forms.Select(attrs={'class': 'ds-input ds-select'}),
        }
        labels = {
            'full_name':    'Nom complet',
            'street':       'Adresse',
            'city':         'Ville',
            'more_details': 'Complément',
            'phone':        'Téléphone',
            'adress_type':  'Type d\'adresse',
        }
