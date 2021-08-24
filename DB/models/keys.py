from tortoise import fields
from tortoise.models import Model


class Key(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    key_md5 = fields.CharField(max_length=32)
    time_created = fields.DateField()
    time_start_use = fields.DateField(null=True)
    # group_id = fields.CharField(max_length=15)

    class Meta:
        table = "keys"

    def __repr__(self):
        return str(self)
