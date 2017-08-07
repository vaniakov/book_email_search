from django import forms


class IndexForm(forms.Form):
    query = forms.CharField(label="Query", widget=forms.TextInput(
        attrs={'placeholder': 'What we will search in books?',
               'class': 'form-control'}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(
        attrs={'placeholder': 'Your email for search results.',
               'class': 'form-control'}))
    time_limit = forms.IntegerField(label='Limit query', required=False,
                                    widget=forms.NumberInput(
                                        attrs={'placeholder': 'Seconds',
                                               'class': 'form-control'}))
