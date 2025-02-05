# Generated by Django 5.0.6 on 2024-06-25 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('course', models.CharField(max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=70, unique=True)),
            ],
            options={
                'verbose_name': 'Course Participant',
                'verbose_name_plural': 'Course Participants',
            },
        ),
    ]
