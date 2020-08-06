from django import forms


class VotingAdminForm(forms.ModelForm):
    def clean_end_date(self):
        end_date = self.cleaned_data['end_date']
        start_date = self.cleaned_data['start_date']

        if end_date <= start_date:
            raise forms.ValidationError('Дата окончания должна быть больше Даты начала')

        return end_date
