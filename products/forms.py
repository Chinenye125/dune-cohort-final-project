from django import forms
from .models import Category, Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'category', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Product name'}),
            'price': forms.NumberInput(attrs={'min': '0'}),
        }

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError('Price must be greater than 0.')
        return price


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
