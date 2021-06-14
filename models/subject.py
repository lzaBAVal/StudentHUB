from tortoise import fields
from tortoise.models import Model

from .student import Student
from .group import Group


class Subject(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    group: fields.ForeignKeyRelation[Group] = fields.ForeignKeyField(
        "models.Group", related_name="group_id"
    )
    user: fields.ForeignKeyRelation[Student] = fields.ForeignKeyField(
        "models.Student", related_name="user_id"
    )
    date_creation = fields.DateField()

    class Meta:
        table = "subject"

    def __str__(self):
        return f"Key ID {self.id}, task_subject name {self.name}, start date {self.date_creation}"

    def __repr__(self):
        return str(self)
