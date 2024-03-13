from django import forms

from .models import Coupon

INPUT_CLASSES='w-full py-4 px-6 rounded-xl border'
class NewCouponForm(forms.ModelForm):
    class Meta:
        model=Coupon
        fields=('category','name','description','image',)
        widgets= {
            'category':forms.Select(attrs={
                'class': INPUT_CLASSES
            }),
            'name': forms.TextInput(attrs={
                 'class':INPUT_CLASSES
             }),
            'description':forms.Textarea(attrs={
                'class':INPUT_CLASSES
            }),
            'image': forms.FileInput(attrs={
                'class':INPUT_CLASSES
            })
        }

class EditCouponForm(forms.ModelForm):
    class Meta:
       model = Coupon
       fields = ('name', 'description', 'image','is_booked')
       widgets = {
        'name': forms.TextInput(attrs={
         'class': INPUT_CLASSES
         }),
        'description': forms.Textarea(attrs={
        'class': INPUT_CLASSES
         }),
        'image': forms.FileInput(attrs={
        'class': INPUT_CLASSES
        })
        }