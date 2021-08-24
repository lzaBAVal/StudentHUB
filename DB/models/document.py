from tortoise import fields
from tortoise.models import Model

# from .subject import Subject
# from .task import Task
from DB.models.task import Task
from DB.models.subject import Subject


class Document(Model):
    id = fields.IntField(pk=True)
    hash_file = fields.CharField(max_length=32)
    telegram_id = fields.CharField(max_length=255)
    task: fields.ForeignKeyRelation[Task] = fields.ForeignKeyField(
        "models.Task", related_name="task_doc_id"
    )
    subject: fields.ForeignKeyRelation[Subject] = fields.ForeignKeyField(
        "models.Subject", related_name="subject_doc_id"
    )

    class Meta:
        table = "doc"

    def __str__(self):
        return f"Key ID {self.id}, file_id {self.hash_file}, task {self.task}"

    def __repr__(self):
        return str(self)
