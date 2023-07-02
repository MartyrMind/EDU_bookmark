import datetime

from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from actions.models import Action


def create_action(user, verb, target=None):
    # проверим, что за последнюю минуту не было совершено аналогичных действий
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    # извлекли все действия определенного типа от одного пользователя за последнюю минуту
    similar_actions = Action.objects.filter(user_id=user.id, verb=verb, created__gte=last_minute)
    # ищем все действия над конкретным объектом за последнюю минуту
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct, target_id=target.id)

    if not similar_actions:  # если ничего не нашли, то создаем действие
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False
