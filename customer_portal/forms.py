from django import forms
from customer_portal.models import Testimonial, Query


class TestimonialForm(forms.ModelForm):
  class Meta:
    model = Testimonial
    fields = ['name', 'email','text']


class QueryForm(forms.ModelForm):
  class Meta:
    model = Query
    fields = ['name','email','text']
