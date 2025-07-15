from django import forms
from .models import Contact, MailingList, Mailing

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'opt_out': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contacts': forms.SelectMultiple(attrs={'class': 'form-control'})
        }

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ['subject', 'body', 'mailing_lists', 'status']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
            'mailing_lists': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
