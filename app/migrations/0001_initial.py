# Generated by Django 2.1.5 on 2020-03-11 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module_code', models.CharField(max_length=50)),
                ('module_name', models.CharField(max_length=50)),
                ('module_year', models.IntegerField(default=2000)),
                ('module_semester', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('professor_id', models.CharField(max_length=50)),
                ('professor_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate_score', models.IntegerField(default=0)),
                ('rate_module', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Module')),
                ('rate_professor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Professor')),
                ('rate_user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='module',
            name='module_taughtby',
            field=models.ManyToManyField(to='app.Professor'),
        ),
    ]
