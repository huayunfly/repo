"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _


class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder': 'Password'}))


class TimelineForm(forms.Form):
    day = forms.ChoiceField(label='daySelect')
    project = forms.ChoiceField(label='projectSelect')
    percentage = forms.DecimalField(lable='percentageInput')
    # using disabled attribute is not safe unless you believe your user.
    # Instead:
    # <div>
    #    <label>projectCategory</label>
    #    <p>Customer</p>
    # </div>
    category = forms.CharField(label='projectCategory', disabled=True)
