from django import forms


class UserRatingForm(forms.Form):
    rate_star_max_length = 10
    rate_star_choices = [(i, str(i)) for i in range(rate_star_max_length,0,-1)]

    e_rating = forms.CharField(label='Efficiency', widget=forms.RadioSelect(choices=rate_star_choices))
    q_rating = forms.CharField(label='Quality', widget=forms.RadioSelect(choices=rate_star_choices))
    l_rating = forms.CharField(label='Length', widget=forms.RadioSelect(choices=rate_star_choices))