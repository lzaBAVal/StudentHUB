from tortoise import fields
from tortoise.models import Model

from .institution import Institution


class Group(Model):
    id = fields.SmallIntField(pk=True)
    group_name = fields.CharField(max_length=20)
    institution: fields.ForeignKeyRelation[Institution] = fields.ForeignKeyField(
        'models.Institution', related_name='institution_id'
    )
    group_url_value = fields.CharField(max_length=255)
    sched_arhit = fields.TextField()
    sched_group = fields.TextField()
    lock = fields.BooleanField()

    class Meta:
        table = "group_students"

    def __str__(self):
        return f"id_inc={self.id}\n" \
               f"group_name={self.group_name}\n" \
               f"institution_id={self.institution}\n" \
               f"lock={self.lock}\n" \
               f"sched_group={self.sched_group}\n" \
               f"sched_arhit={self.sched_arhit}"

    def __repr__(self):
        return str(self)