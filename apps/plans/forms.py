from django import forms
from .models import PlansInifo


class PlanAddInfoForm(forms.ModelForm):
    class Meta:
        model = PlansInifo
        fields = ['company_id', 'project_name', 'project_year','plan_type', 'project_type','project_basis','project_status']