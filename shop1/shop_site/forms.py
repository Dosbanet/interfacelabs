from django import forms

class CheckoutForm(forms.Form):
    """Checkout form for related page.

    Really barebones, Johnes.
    """
    addr = forms.CharField(label='Where your order will be delivered', max_length=1000)
    when = forms.DateField(label='When your order will be delivered', input_formats=['%Y-%m-%d'])
    mail = forms.EmailField(label='Confirmation mail will be send to specified address')
