# -*- coding: utf-8 -*-
from bobotinho.models.base import Base, TimestampMixin, ContentMixin, fields, timezone


class Reminder(Base, TimestampMixin, ContentMixin):
    from_user = fields.ForeignKeyField("models.User", related_name="reminders_from")
    to_user = fields.ForeignKeyField("models.User", related_name="reminders_to")
    channel = fields.ForeignKeyField("models.User", related_name="reminders_channel")
    scheduled_for = fields.DatetimeField(null=True)

    class Meta:
        table = "reminder"

    @property
    def scheduled_to(self):
        return self.scheduled_for - timezone.now()
