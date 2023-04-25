# Generated by Django 4.1.7 on 2023-04-18 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=100)),
                ('sum_count', models.PositiveIntegerField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('transfer_type', models.CharField(choices=[('transfer', 'перевод'), ('buy', 'покупка'), ('achievement', 'ачивка')], max_length=50)),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='отправитель', to='users.bankaccount')),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='получатель', to='users.bankaccount')),
            ],
            options={
                'verbose_name': 'Перевод',
                'verbose_name_plural': 'Переводы',
            },
        ),
    ]
