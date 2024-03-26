from django.db import models


class UploadedPDF(models.Model):
    pdf_files = models.FileField(upload_to='pdfs/', blank=True, null=True)
