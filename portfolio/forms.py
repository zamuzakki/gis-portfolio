from django import forms
from django.contrib.gis import forms as gis_forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Row, Column, Button
from .models import Profile, Expertise

class ProfileForm(forms.ModelForm):
    """
    Form to edit Profile
    """

    # For loction field, we will use OpenStreetMap Widget
    location = gis_forms.PointField(required=False, widget=gis_forms.OSMWidget(
            attrs={
                'default_lat': -7.7129,
                'default_lon': 110.0093,
                'default_zoom': 11,
                'map_width': 1050,
            }
        ),
    )
    # Expertise can have multiple value, so we will use Multiple ModelMultipleChoiceField
    expertise = forms.ModelMultipleChoiceField(required=False, queryset=Expertise.objects.all(),
                                               widget=forms.SelectMultiple(attrs={'style': 'width:100%;'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.attrs = {'id': 'profile-form'} #give id to form
        self.helper.layout = Layout(
            'photo',
            Row(
                Column(
                    Row(
                        Column('first_name', css_class='col-12 col-sm-4 input-sm '),
                        Column('last_name', css_class='col-12 col-sm-4 input-sm'),
                        Column('phone', css_class='col-12 col-sm-4 input-sm '),
                        css_class='row'
                    ),
                    css_class='col-md-12'
                ),
                css_class='form-row row'
            ),
            Row(
                Column(
                    Row(
                        Column('expertise', css_class='col-12 col-sm-4 input-sm'),
                        Column('address', css_class='col-12 col-sm-8 input-sm'),
                        css_class='row'
                    ),
                    css_class='col-md-12'
                ),
                css_class='form-row row'
            ),
            'location',
            Submit('submit', 'Save')
        )

    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ('user',)