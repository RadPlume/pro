from django import forms

class MapVariables(forms.Form):
    STABILITY_CHOICES = (
        ('A', 'a'),
        ('B', 'b'),
        ('C', 'c'),
        ('D', 'd'),
        ('E', 'e'),
        ('F', 'f'),
        ('G', 'g'),
    )

    reactors = forms.CharField()
    downwind = forms.IntegerField(min_value=0, max_value=500)
    off_centre = forms.IntegerField(max_value=500)
    stability = forms.ChoiceField(choices=STABILITY_CHOICES, widget=forms.RadioSelect())
    