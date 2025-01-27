# Generated by Django 5.1.4 on 2025-01-07 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_feed_supp', models.CharField(max_length=100)),
                ('last_name_feed_supp', models.CharField(max_length=100)),
                ('email_feed_supp', models.EmailField(max_length=254)),
                ('contact_number_feed_supp', models.CharField(max_length=15)),
                ('subject_line', models.CharField(max_length=255)),
                ('details_feed_supp', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name_feed_supp', models.CharField(max_length=100)),
                ('last_name_feed_supp', models.CharField(max_length=100)),
                ('email_feed_supp', models.EmailField(max_length=254)),
                ('contact_number_feed_supp', models.CharField(max_length=15)),
                ('subject_line', models.CharField(max_length=255)),
                ('details_feed_supp', models.TextField()),
            ],
        ),
    ]
