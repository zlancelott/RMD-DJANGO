# Generated by Django 2.1.3 on 2018-11-26 13:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=1)),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='LessonFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('file_image', models.ImageField(upload_to='photos/')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='lessonFile_author', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lesson', to='home.Lesson')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=30)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Course')),
            ],
        ),
        migrations.CreateModel(
            name='SubjectClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=10)),
                ('code', models.CharField(max_length=30)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('lesson_files', models.ManyToManyField(to='home.LessonFile')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Subject')),
            ],
        ),
        migrations.CreateModel(
            name='UserClassAssociation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_mod', models.BooleanField(default=False)),
                ('subject_class_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.SubjectClass')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='lessonfile',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Subject'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.SubjectClass'),
        ),
        migrations.AddField(
            model_name='user',
            name='subject_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.SubjectClass'),
        ),
    ]
