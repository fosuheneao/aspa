from django import forms
from .models import Store
from aspamain.models import Industry, Category

class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'industry', 'category', 'description', 'logo', 'website']
        widgets = {            
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Business Registration Name'}),
            'industry': forms.Select(attrs={'class': 'form-control industry-select'}),
            'category': forms.Select(attrs={'class': 'form-control'}),            
            'description': forms.Textarea(attrs={'class': 'form-control','rows': 3}),
            'logo': forms.FileInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()  # Initially empty

        if 'industry' in self.data:
            try:
                industry_id = int(self.data.get('industry'))
                self.fields['category'].queryset = Category.objects.filter(industry_id=industry_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input; ignore and default to empty queryset
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.industry.category_set.order_by('name')
