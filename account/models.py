from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings


# простым способом расширения стандартной модели User является создание модели профиля,
# которая содержит взаимосвязь один-к-одному со встроенной моделью User и любые доп. поля
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'


class Contact(models.Model):
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']

    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'


# если во взаимосвязи многие ко многим требуются дополнительные поля, то следует создать конкретно-прикладную модель
# c внешним ключом для каждой стороны взаимосвязи. В одну из связанных моделей следует добавить ManyToManyField и
# сообщить Django, что нужно использовать вашу модель через ключевое слово through

# хотим добавить во встроенный класс User то самое ManyToManyField
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self',
                                                            through=Contact,
                                                            related_name='followers',
                                                            symmetrical=False))
# при использовании промежуточной модели для многих-ко-многим, некоторые методы родственного менеджера отключаются
# например add(), remove(), create(). Вместо этого нужно манипулировать экземплярами промежуточной модели
