from django import forms
from core.models import Operation, Third, Category


class OperationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    date = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "required input input-primary", "autocomplete": "off"}
        )
    )

    third = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "input input-primary",
                "autocomplete": "off",
                "type": "search",
                "placeholder": "Recherche par nom du tier",
                "hx-on:keyup": "document.getElementById('third-search-table').style.display='block'",
                "hx-post": "/third/search",
                "hx-trigger": "click, keyup[target.value.length > 1] delay:500ms",
                "hx-target": "#third-search-table",
                "hx-swap": "innerHTML",
            }
        ),
        label="Tier",
    )

    category = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={
                "class": "input input-primary",
                "autocomplete": "off",
                "type": "search",
                "placeholder": "Recherche par nom de la catégorie",
                "hx-on:keyup": "document.getElementById('category-search-table').style.display='block'",
                "hx-post": "/category/search",
                "hx-trigger": "click, keyup[target.value.length > 1] delay:500ms",
                "hx-target": "#category-search-table",
                "hx-swap": "innerHTML",
            }
        ),
        label="Catégorie",
    )

    value = forms.CharField(
        max_length=128,
        widget=forms.TextInput(
            attrs={"class": "required input input-primary", "autocomplete": "off"}
        ),
        label="Montant",
    )

    def clean_value(self):
        value = self.cleaned_data["value"]
        try:
            value = float(value.replace(",", "."))
        except Exception as e:
            raise forms.ValidationError("Montant doit être un nombre.")

        if isinstance(value, (int, float, complex)) and not isinstance(value, bool):
            return value
        raise forms.ValidationError("Montant doit être un nombre.")

    def clean_third(self):
        third = self.cleaned_data["third"]
        third_object = Third.objects.filter(name=third, user=self.user)
        return third_object[0]

    def clean_category(self):
        category = self.cleaned_data["category"]
        category_object = Category.objects.filter(name=category, user=self.user)
        return category_object[0]

    periodicity = forms.CharField(
        max_length=10,
        widget=forms.TextInput(
            attrs={
                "class": "required input input-primary w-10 input-sm",
                "autocomplete": "off",
                ":value": "counter",
            }
        ),
        label="Fréquence",
        initial=0,
    )
