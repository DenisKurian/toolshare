# Generated by Django 5.1.5 on 2025-02-28 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Guest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tbl_user',
            name='user_photo',
            field=models.FileField(default='profiles/user/default.jpg', upload_to='profiles/user'),
        ),
    ]
