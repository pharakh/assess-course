# Generated by Django 4.1.1 on 2022-09-30 14:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_app', '0038_prizename_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prizesgot',
            name='prize',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prize_name', to='assessment_app.prizename'),
        ),
    ]