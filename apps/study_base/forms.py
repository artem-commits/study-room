from django import forms
from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'participants', 'is_deleted', 'deleted_at', ]
        labels = {
            'name': 'Название комнаты',
            'topic': 'Тема',
            'description': 'Описание',
        }
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'Опишите вашу комнату...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Введите название комнаты...'}),
        }