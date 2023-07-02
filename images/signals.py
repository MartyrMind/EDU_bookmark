from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from images.models import Image


# декорируем функцию, указывая ее как функцию-получатель сигналов
# соединяем ее с функцией Image.users_like, чтобы функция вызывалась только если сигнал
# m2m_changed был запущен этим отправителем
@receiver(m2m_changed, sender=Image.users_like.through)
def users_like_changed(sender, instance, **kwargs):
    instance.total_likes = instance.users_like.count()
    instance.save()
