from django import forms

class PredictionForm(forms.Form):
    age = forms.IntegerField(label="Age", min_value=0, max_value=120)
    cholesterol = forms.FloatField(label="Cholesterol Level (mg/dL)")
    blood_pressure = forms.FloatField(label="Blood Pressure (mmHg)")
    smoking = forms.ChoiceField(label="Smoking", choices=[(1, "Yes"), (0, "No")])
    diabetes = forms.ChoiceField(label="Diabetes", choices=[(1, "Yes"), (0, "No")])
