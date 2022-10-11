# Generated by Django 4.1.1 on 2022-09-26 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assessment_app', '0012_questions_delete_queandans_alter_idnumbers_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursename',
            name='number',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='coursename',
            name='type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='formsample',
            name='courses',
            field=models.ManyToManyField(related_name='courses_assinged', to='assessment_app.course'),
        ),
        migrations.AddField(
            model_name='questions',
            name='q_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='term',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='coursename',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.DeleteModel(
            name='Form',
        ),
    ]