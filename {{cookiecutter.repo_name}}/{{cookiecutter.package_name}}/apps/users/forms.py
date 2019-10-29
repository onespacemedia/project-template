from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class ProjectPasswordResetForm(PasswordResetForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['email'].widget.attrs['placeholder'] = self.fields['email'].label


class ProjectSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].help_text = "Your password must be at least 8 characters long and cannot be entirely numeric"
        self.fields['new_password2'].help_text = "Enter the same password for verification."

        self.fields['new_password1'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password1'].widget.attrs['placeholder'] = self.fields['new_password1'].label

        self.fields['new_password2'].widget.attrs['class'] = 'frm-Form_Input'
        self.fields['new_password2'].widget.attrs['placeholder'] = self.fields['new_password2'].label
