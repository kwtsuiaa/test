from django import forms
from .models import vm
class mainform(forms.Form):
    Delay_vm = forms.ModelChoiceField(queryset=vm.objects.all().order_by('name'))
    Delay_Time = forms.IntegerField(required=False)
