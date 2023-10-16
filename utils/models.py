from django.db import models

# Create your models here.
    
class DOCX(models.Model):
    docx_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

class PDF(models.Model):
    docx = models.ForeignKey(DOCX, on_delete=models.CASCADE)
    pdf_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
