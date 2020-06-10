from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

from bootstrap_datepicker_plus import DatePickerInput

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=DatePickerInput(format='%m/%d/%Y'))

    class Meta:
        model = Profile
        fields = ('gender', 'birth_date')


class UserForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ['password']
        fields = ('username', 'first_name', 'last_name', 'email', )

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # https://code.djangoproject.com/ticket/8620
        [self.fields.pop(f) for f in self.fields.keys() if f in self.Meta.exclude]
        profile_kwargs = kwargs.copy()
        if 'instance' in kwargs:
            self.profile = kwargs['instance'].profile
            profile_kwargs['instance'] = self.profile

        self.profile_form = UserProfileForm(*args, **profile_kwargs)
        self.fields.update(self.profile_form.fields)
        self.initial.update(self.profile_form.initial)

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        self.errors.update(self.profile_form.errors)
        return cleaned_data

    def save(self, commit=True):
        self.profile_form.save(commit)
        return super(UserForm, self).save(commit)
