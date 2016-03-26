from django import forms
from .models import Text

class TextForm(forms.Form): 
	class Meta:
		model=Text
