# Generated by Django 4.1.1 on 2022-09-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_app', '0005_coursename_term_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formsample',
            name='question',
            field=models.ManyToManyField(blank=True, related_name='questions', to='assessment_app.queandans'),
        ),
    ]