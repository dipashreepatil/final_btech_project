
from django import forms

COMPANIES = [
    ('Amazon','amazon'),
    ('Apple','apple'),
    ('Microsoft','microsoft'),
    ('Google','google'),
    ('Gamestop','gamestop'),
    ('IBM','ibm'),
    ('Tesla','tesla'),
    ('JP Morgan','jp morgan'),
    ('Facebook','facebook'),
    ('Netflix','netflix'),
]
class SearchForm(forms.Form):
    search_words = forms.ChoiceField(choices = COMPANIES,widget=forms.Select)
   
   
   
class CompanySearchForm(forms.Form):
    search_words = forms.ChoiceField(choices = COMPANIES,widget=forms.Select)
   
