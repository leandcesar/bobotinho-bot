# -*- coding: utf-8 -*-
from tortoise import fields, timezone
from tortoise.models import Model


class Base(Model):
    id = fields.IntField(pk=True)

    class Meta:
        abstract = True

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self.id})"


class TimestampMixin:
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    @property
    def created_ago(self):
        return timezone.now() - self.created_at

    @property
    def updated_ago(self):
        return timezone.now() - self.updated_at


class UserMixin:
    id = fields.IntField(pk=True, description="Twitch ID")
    name = fields.CharField(unique=True, index=True, max_length=64, description="Twitch username")


class ContentMixin:
    content = fields.CharField(max_length=500, null=True, description="Twitch message content")
