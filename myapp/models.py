from django.db import models

# Create your models here.

class Data(models.Model):
    pl = models.CharField(max_length=100)
    topic = models.CharField(max_length=200)
    status = models.CharField(max_length=200,null=True)
    html_doc = models.FileField(upload_to='html_files/',null=True)
    examples = models.CharField(max_length=1000,null=True)
    time_in = models.CharField(max_length=200,null=True)
    time_out = models.CharField(max_length=200,null=True)