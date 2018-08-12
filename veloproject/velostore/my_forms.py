from django import forms


class addPostForm(forms.Form):
    title = forms.CharField(max_length=50, widget=forms.Textarea)
    mark = forms.CharField(max_length=50, widget=forms.Textarea)
    price = forms.CharField(null=True, blank=True,
                             max_length=50, widget=forms.Textarea)  # храню в char field т.к. кроме как выводить с ней ничего делать не надо
    phone_number = forms.CharField(max_length=17, widget=forms.Textarea)
    email = forms.CharField(max_length=75, widget=forms.Textarea)