# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, fields


class Pet(Base):
    user = fields.ForeignKeyField("models.Cookie")
    name = fields.CharField(max_length=32, null=True)
    specie = fields.CharField(max_length=16)
    xp = fields.IntField(default=0)
    energy = fields.SmallIntField(default=10)
    fun = fields.SmallIntField(default=0)
    hunger = fields.SmallIntField(default=0)
    hygiene = fields.SmallIntField(default=0)
    love = fields.SmallIntField(default=0)

    class Meta:
        table = "pet"

    def __str__(self):
        return self.name if self.name else self.specie

    @classmethod
    async def find(cls, id: str, name: str = None, specie: str = None):
        return (
            await cls.filter(user_id=id, name=name).first()
            or await cls.filter(user_id=id, specie=specie).first()
        )
