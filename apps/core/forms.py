from django import forms
from apps.client.models import Usuario

class SignUpForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'email', 'oab', 'telefone']

    def __init__(self,*args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # GENERAL INFO
        self.fields['nome_completo'].widget.attrs['class'] = 'form-control'
        self.fields['nome_completo'].widget.attrs['placeholder'] = 'Nome Completo'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'

        self.fields['oab'].widget.attrs['class'] = 'form-control'
        self.fields['oab'].widget.attrs['placeholder'] = 'OAB'

        self.fields['telefone'].widget.attrs['class'] = 'form-control masked-phone'
        self.fields['telefone'].widget.attrs['placeholder'] = 'Telefone'

        self.fields['senha'].widget.attrs['class'] = 'form-control'
        self.fields['senha'].widget.attrs['placeholder'] = 'Senha'


class ConfirmSmsForm(forms.Form):
    sms_code = forms.CharField(min_length=4)
    
    def __init__(self,*args, **kwargs):
        super(ConfirmSmsForm, self).__init__(*args, **kwargs)

        # GENERAL INFO
        self.fields['sms_code'].widget.attrs['class'] = 'form-control masked-sms'
        self.fields['sms_code'].widget.attrs['placeholder'] = 'Código SMS'


class PhoneForm(forms.Form):
    phone = forms.CharField(max_length=20)
    
    def __init__(self,*args, **kwargs):
        super(PhoneForm, self).__init__(*args, **kwargs)

        # GENERAL INFO
        self.fields['phone'].widget.attrs['class'] = 'form-control masked-phone'


class ExtraInfoForm(forms.ModelForm):
    street = forms.CharField(label='Rua')
    number = forms.CharField(label='Número')
    city = forms.CharField(label='Cidade')
    neighborhood = forms.CharField(label='Bairro')
    state = forms.CharField(label='UF', max_length=2)
    zip_code = forms.CharField(label='CEP')
    latitude = forms.DecimalField(widget=forms.HiddenInput(), required = False)
    longitude = forms.DecimalField(widget=forms.HiddenInput(), required = False)
    cod_ibge = forms.IntegerField(widget=forms.HiddenInput(), required = False)

    class Meta:
        model = Usuario
        exclude = ['nome_completo', 'email', 'oab', 'telefone', 'user', 'confirmation_sms', 'sms_date', 'sms_code', 'sms_resends', 'tipo_usuario']
    
    def __init__(self,*args, **kwargs):
        super(ExtraInfoForm, self).__init__(*args, **kwargs)

        # ADDRESS
        self.fields['street'].widget.attrs['class'] = 'form-control'
        self.fields['street'].widget.attrs['placeholder'] = 'Rua'

        self.fields['state'].widget.attrs['class'] = 'form-control'
        self.fields['state'].widget.attrs['placeholder'] = 'UF'

        self.fields['number'].widget.attrs['class'] = 'form-control'
        self.fields['number'].widget.attrs['placeholder'] = 'Número'
        
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'Cidade'

        self.fields['neighborhood'].widget.attrs['class'] = 'form-control'
        self.fields['neighborhood'].widget.attrs['placeholder'] = 'Bairro'
        
        self.fields['zip_code'].widget.attrs['class'] = 'form-control masked-zipcode'
        self.fields['zip_code'].widget.attrs['placeholder'] = 'CEP'