# -*- coding: utf-8 -*-
from bobotinho.database.base import Base, ContentMixin, TimestampMixin, fields


class Bug(Base, TimestampMixin, ContentMixin):
    author = fields.CharField(max_length=64)
    source = fields.CharField(max_length=64)

    class Meta:
        table = "bug"
