# Generated by Django 4.2.1 on 2024-03-13 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdf_reader", "0002_remove_uploadedpdf_title"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="uploadedpdf",
            name="pdf_file",
        ),
        migrations.AddField(
            model_name="uploadedpdf",
            name="pdf_files",
            field=models.FileField(blank=True, null=True, upload_to="pdfs/"),
        ),
    ]
