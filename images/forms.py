import requests
from django import forms
from django.core.files.base import ContentFile
from django.utils.text import slugify

from images.models import Image


class ImageCreateForm(forms.ModelForm):  # форма для передачи новых изображений на обработку
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        # пользователи не будут вводить URL-адрес изображения прямо в форму
        # вместо этого им будет предоставлен JS инструмент
        widgets = {
            'url': forms.HiddenInput
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = url.split('.')[-1].lower()
        print(extension)
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions')
        return url

    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)  # создали новый экземпляр изображения
        image_url = self.cleaned_data['url']
        name = slugify(image.title)
        extension = image_url.split('.')[-1].lower()
        image_name = f'{name}.{extension}'
        response = requests.get(image_url)
        # у модели есть поле image, передаем туда объект ContentFile,
        # экземпляр которого заполнен содержимым скачанного файла
        # save=False нужен для того, чтобы объект не сохранялся в БД
        image.image.save(image_name, ContentFile(response.content), save=False)

        if commit:  # сохраняем поведение, как в оригинальном методе save модельной формы
            image.save()
        return image
