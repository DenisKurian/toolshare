# Generated by Django 5.1.5 on 2025-03-02 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0014_alter_tbl_gallery_gallery_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_gallery',
            name='gallery_file',
            field=models.FileField(default='Assets/default.jpg', upload_to='Assets/gallery'),
        ),
    ]
