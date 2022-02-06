# -*- coding: utf-8 -*-
from tortoise import signals

from bobotinho.models import Cookie, Player, User


@signals.post_save(User)
async def update_user_name(sender, instance, created, using_db, update_fields):
    if not created and update_fields and "name" in update_fields:
        await Cookie.filter(id=instance.id).update(name=instance.name)
        await Player.filter(id=instance.id).update(name=instance.name)
