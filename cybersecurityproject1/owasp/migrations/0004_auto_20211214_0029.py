# Generated by Django 3.1.2 on 2021-12-13 22:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('owasp', '0003_remove_videoitem_votes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videofeedback',
            name='comment',
            field=models.TextField(verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='date',
            field=models.DateTimeField(verbose_name='Date published'),
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='videoLink',
            field=models.CharField(max_length=500, verbose_name='Video link'),
        ),
        migrations.AlterField(
            model_name='videoitem',
            name='videoTitle',
            field=models.CharField(max_length=200, verbose_name='Video title'),
        ),
        migrations.CreateModel(
            name='ProfileInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, verbose_name='Username')),
                ('email', models.CharField(max_length=200, verbose_name='E-mail')),
                ('phone', models.TextField(max_length=50, verbose_name='Phone number')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
