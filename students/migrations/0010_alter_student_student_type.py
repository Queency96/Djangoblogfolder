# Generated by Django 5.1.1 on 2024-12-10 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0009_alter_student_student_type_alter_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Leader', 'Cohort Leader'), ('President', 'President'), ('Secretary', 'Secretary'), ('Vice', 'Vice President')], default='Student', max_length=9),
        ),
    ]