# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, UserMixin, TimestampMixin, fields


class Cookie(Base, UserMixin, TimestampMixin):
    count = fields.SmallIntField(default=0)
    daily = fields.SmallIntField(default=1)
    donated = fields.SmallIntField(default=0)
    received = fields.SmallIntField(default=0)
    stocked = fields.SmallIntField(default=0)

    class Meta:
        table = "cookie"

    async def use_daily(self):
        self.daily -= 1
        await self.save()

    async def consume(self, amount: int = 1):
        if self.stocked >= amount:
            self.stocked -= amount
        else:
            amount -= self.stocked
            self.stocked = 0
            self.daily -= amount
        self.count += amount
        await self.save()

    async def donate(self, amount: int = 1):
        self.daily -= amount
        self.donated += amount
        await self.save()

    async def receive(self, amount: int = 1):
        self.stocked += amount
        self.received += amount
        await self.save()

    async def stock(self, amount: int = 1):
        self.stocked += amount
        await self.save()
