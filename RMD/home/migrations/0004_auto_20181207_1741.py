# Generated by Django 2.1.3 on 2018-12-07 20:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20181207_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userclassassociation',
            name='subject_class_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.SubjectClass'),
        ),
        migrations.AlterField(
            model_name='userclassassociation',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='moderador', to=settings.AUTH_USER_MODEL),
        ),
    ]