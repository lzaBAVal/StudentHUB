from tortoise import fields
from tortoise.models import Model


class Key(Model):
    id = fields.IntField(pk=True)
    chat_id = fields.BigIntField(unique=True)
    key_md5 = fields.CharField(max_length=32)
    time_created = fields.CharField(max_length=25)
    time_start_use = fields.CharField(max_length=25)
    group_name = fields.CharField(max_length=15)

    class Meta:
        table = "keys"

    def __str__(self):
        return f"Key ID {self.id}, id_chat {self.chat_id}, group_name {self.group_name}"

    def __repr__(self):
        return str(self)
