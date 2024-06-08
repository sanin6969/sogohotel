from django import forms

class ContactForm(forms.Form):
    Type_of_room = forms.ChoiceField(choices=[
        ('Single Room', 'Single Room'),
        ('Family Room', 'Family Room'),
        ('Presidential Room', 'Presidential Room')
    ])
    Number_of_Rooms = forms.IntegerField()
    Check_in = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Check_out = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    Time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    No_of_persons = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        if 'is_active' not in self.fields:
            self.initial['is_active'] = True


class RoomAvailabilityForm(forms.Form):
    room_type = forms.ChoiceField(choices=[
        ('Single Room', 'Single Room'),
        ('Family Room', 'Family Room'),
        ('Presidential Room', 'Presidential Room'),
    ])
    no_of_rooms = forms.IntegerField(min_value=1)
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_in_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))