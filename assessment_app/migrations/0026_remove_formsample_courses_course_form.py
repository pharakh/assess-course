# Generated by Django 4.1.1 on 2022-09-27 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_app', '0025_coursename_number_alter_coursename_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formsample',
            name='courses',
        ),
        migrations.AddField(
            model_name='course',
            name='form',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='which_formsample', to='assessment_app.formsample'),
        ),
    ]