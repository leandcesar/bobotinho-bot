# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, TimestampMixin, fields


class Channel(Base, TimestampMixin):
    user = fields.ForeignKeyField("models.User", unique=True)
    followers = fields.IntField(null=True, description="Twitch followers")
    banwords = fields.JSONField(default={})
    disabled = fields.JSONField(default={})
    online = fields.BooleanField(default=True)

    class Meta:
        table = "channel"
