from django import forms
from .models import Customer


class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = [
            'phone_number',
            'address',
            'document_id'
        ]

        labels = {
            'phone_number': '',
            'address': '',
            'document_id': '',
        }
