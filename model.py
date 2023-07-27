from tortoise import fields
from tortoise.models import Model

class DBsiswa(Model):
    id = fields.IntField(pk=True)
    nama = fields.CharField(max_length=225)
    hobi = fields.CharField(max_length=255)

    class Meta:
        table = "dbsiswa"

    def __str__(self):
        return self.id