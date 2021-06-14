from tortoise import fields
from tortoise.models import Model


class Institution(Model):
    id = fields.IntField(pk=True)
    instit_name = fields.TextField()
    url = fields.TextField()
    url_for_groups = fields.TextField()

    class Meta:
        table = "institution"

    def __str__(self):
        return f"Institution ID {self.id}, " \
               f"by name {self.instit_name}, " \
               f"url {self.url}, " \
               f"url_for_groups {self.url_for_groups}"

    def __repr__(self):
        return str(self)
