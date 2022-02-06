# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, ContentMixin, TimestampMixin, fields


class Suggest(Base, TimestampMixin, ContentMixin):
    author = fields.CharField(max_length=64)
    source = fields.CharField(max_length=64)

    class Meta:
        table = "suggest"
