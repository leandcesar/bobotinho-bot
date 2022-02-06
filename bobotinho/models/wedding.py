# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, TimestampMixin, fields


class Wedding(Base, TimestampMixin):
    user_1 = fields.ForeignKeyField("models.Cookie", related_name="user_1")
    user_2 = fields.ForeignKeyField("models.Cookie", related_name="user_2")
    divorced = fields.BooleanField(default=False)

    class Meta:
        table = "wedding"

    async def divorce(self):
        self.divorced = True
        await self.save()

    async def spouse(self, name: str):
        await self.fetch_related("user_1", "user_2")
        return self.user_1 if self.user_2.name == name else self.user_2

    @classmethod
    async def find(cls, id_1: int, id_2: int = None):
        if not id_2:
            return (
                await cls.filter(user_1_id=id_1, divorced=False).first()
                or await cls.filter(user_2_id=id_1, divorced=False).first()
            )
        return (
            await cls.filter(user_1_id=id_1, user_2_id=id_2, divorced=False).first()
            or await cls.filter(user_1_id=id_2, user_2_id=id_1, divorced=False).first()
        )

    @classmethod
    async def find_all(cls, id: int):
        return (
            await cls.filter(user_1_id=id, divorced=False).all()
            + await cls.filter(user_2_id=id, divorced=False).all()
        )
