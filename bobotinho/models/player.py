# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, TimestampMixin, UserMixin, fields


class Player(Base, UserMixin, TimestampMixin):
    class_ = fields.CharField(max_length=1)
    sub_class = fields.CharField(max_length=1, default="A", null=True)
    gender = fields.CharField(max_length=1)
    dungeon = fields.CharField(max_length=3, null=True)
    wins = fields.SmallIntField(default=0)
    defeats = fields.SmallIntField(default=0)
    level = fields.IntField(default=1)
    xp = fields.IntField(default=0)

    class Meta:
        table = "player"
