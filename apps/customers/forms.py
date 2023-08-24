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

    def clean_document_id(self, *args, **kwargs):
        document_id = self.cleaned_data.get('document_id')
        if not document_id.isnumeric():
            raise forms.ValidationError('Id must contain only numbers')
        return document_id
