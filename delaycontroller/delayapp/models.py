from django.db import models

class vm(models.Model):
    name = models.CharField(max_length=500)
    hostname = models.CharField(max_length=500)
    user = models.CharField(max_length=500)
    password = models.CharField(max_length=500)
    interface = models.CharField(max_length=500, default="eth1")
    sshport = models.IntegerField()

    def __str__(self):
        return self.name
