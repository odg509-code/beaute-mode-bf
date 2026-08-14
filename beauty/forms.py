from django import forms
from .models import Appointment
class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ('service','starts_at','note')
        widgets = {'starts_at':forms.DateTimeInput(attrs={'type':'datetime-local'}), 'note':forms.Textarea(attrs={'rows':3, 'placeholder':'Une précision pour l’institut ?'})}
    def __init__(self, *args, institute=None, **kwargs):
        super().__init__(*args, **kwargs)
        if institute: self.fields['service'].queryset = institute.services.all()
