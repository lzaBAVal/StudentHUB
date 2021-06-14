from tortoise import fields
from tortoise.models import Model

from .subject import Subject


class Task(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField(
        "models.Subject", related_name='subject_id_for_task', on_delete=fields.CASCADE
    )
    description = fields.CharField(max_length=512, default='None')
    variant_start = fields.SmallIntField()
    variant_end = fields.SmallIntField()
    user_variant = fields.JSONField()

    class Meta:
        table = "task"

    def __str__(self):
        return f"Key ID {self.id}, task_name {self.name}, task_subject {self.subject}"

    def __repr__(self):
        return str(self)
