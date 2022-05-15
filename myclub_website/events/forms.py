from django import forms


class BuyTicketForm(forms.Form):
    first_name = forms.CharField(label="First Name", max_length=64, required=True)
    last_name = forms.CharField(label="Last Name", max_length=64, required=True)
    email = forms.EmailField(label="Email", max_length=255, required=True)
    # tickets = forms.IntegerField(min_value=1, required=True)

    def __init__(self, *args, **kwargs) -> None:
        available_tickets = kwargs.pop("available_tickets", 1)
        super().__init__(*args, **kwargs)
        self.fields['tickets'] = forms.IntegerField( required=True, min_value=1, max_value=available_tickets)
