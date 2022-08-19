from django import forms

class FormStepOne(forms.Form):
    CHOICES = (('Option 1', '個人'),('Option 2', '團體'))
    join_type1 = forms.ChoiceField(choices=CHOICES, label='參與形式')

class FormStepTwo(forms.Form):
    job = forms.CharField(max_length=100)
    salary = forms.CharField(max_length=100)
    job_description = forms.CharField(widget=forms.Textarea)
