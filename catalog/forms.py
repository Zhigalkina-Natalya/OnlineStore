from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Product, Category


BANNED_WORDS = ["казино", "криптовалюта", "крипта", "биржа", "дешево", "бесплатно", "обман", "полиция", "радар"]

class ProductForm(forms.ModelForm):
    """
    Форма для создания и редактирования продуктов с валидацией и стилями.
    """

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image',]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        """Добавляем базовую стилизацию Bootstrap."""
        super().__init__(*args, **kwargs)

        placeholders = {
            'name': 'Введите название товара',
            'description': 'Краткое описание (до 300 символов)',
            'price': 'Укажите цену (например, 199.99)',
        }

        # Стилизация
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

            if field_name in placeholders:
                field.widget.attrs.setdefault('placeholder', placeholders[field_name])

        # Для поля price задаём шаг и минимальное значение
        if 'price' in self.fields:
            self.fields['price'].widget = forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0'
            })

        if 'category' in self.fields:
            self.fields['category'].widget.attrs.update({'class': 'form-select'})

    def _check_banned(self, value, field_label):
        """
        Проверка наличия запрещённых слов (без учёта регистра).
        """
        if not value:
            return
        lower = value.lower()
        for bad in BANNED_WORDS:
            if bad in lower:
                raise ValidationError(f"Поле «{field_label}» содержит запрещённое слово: «{bad}».")

    def clean_name(self):
        name = self.cleaned_data.get('name')
        self._check_banned(name, "Название")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        self._check_banned(description, "Описание")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        try:
            if Decimal(price) < Decimal('0'):
                raise ValidationError("Цена не может быть отрицательной.")
        except (TypeError, ValueError):
            raise ValidationError("Введите корректную цену.")
        return price