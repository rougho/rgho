from django import forms


# Define country choices for the phone number widget
COUNTRY_CHOICES = [
    ('1', '+1 (US/CA)'),
    ('44', '+44 (UK)'),
    ('33', '+33 (FR)'),
    ('49', '+49 (DE)'),
    ('39', '+39 (IT)'),
    ('34', '+34 (ES)'),
    ('81', '+81 (JP)'),
    ('86', '+86 (CN)'),
    ('91', '+91 (IN)'),
    ('55', '+55 (BR)'),
    ('61', '+61 (AU)'),
    ('7', '+7 (RU)'),
    ('82', '+82 (KR)'),
    ('52', '+52 (MX)'),
    ('27', '+27 (ZA)'),
    ('20', '+20 (EG)'),
    ('234', '+234 (NG)'),
    ('966', '+966 (SA)'),
    ('971', '+971 (AE)'),
    ('31', '+31 (NL)'),
]

class CountryPhoneWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(choices=[('', 'Code')] + COUNTRY_CHOICES, attrs={
                'class': 'form-select',
                'style': 'flex: 0 0 25%; max-width: 25%;'
            }),
            forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Phone number',
                'type': 'tel'
            })
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            if isinstance(value, str) and value.startswith('+'):
                # Try to split country code from number
                value_no_plus = value[1:]
                for code, label in COUNTRY_CHOICES:
                    if value_no_plus.startswith(code):
                        number = value_no_plus[len(code):].strip()
                        return [code, number]
                return ['', value]
            return ['', str(value)]
        return ['', '']

    def value_from_datadict(self, data, files, name):
        country_code = data.get(name + '_0', '')
        phone_number = data.get(name + '_1', '')
        if country_code and phone_number:
            return f"+{country_code}{phone_number}"
        elif phone_number:
            return phone_number
        return ''
