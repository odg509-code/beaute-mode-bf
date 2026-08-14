from django import forms

from .models import Payment


class CheckoutForm(forms.Form):
    delivery_city = forms.CharField(label='Ville', max_length=80)
    delivery_address = forms.CharField(
        label='Adresse de livraison',
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Quartier, rue et repère utile'}),
    )
    payment_method = forms.ChoiceField(label='Mode de paiement', choices=Payment.Method.choices)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['delivery_city'].initial = user.city or 'Ouagadougou'
