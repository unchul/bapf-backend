# Generated by Django 5.1.7 on 2025-06-25 12:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
        ('board', '0001_initial'),
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountAlarm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('alarm_type', models.CharField(choices=[('BOARD', '게시글 알림'), ('COMMENT', '댓글 알림')], default='COMMENT', max_length=15)),
                ('is_unread', models.BooleanField(default=True)),
                ('alarm_created_at', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='board.board')),
                ('comment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comment.comment')),
                ('recipient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient', to='account.account')),
            ],
            options={
                'db_table': 'account_alarm',
                'ordering': ['-alarm_created_at'],
            },
        ),
    ]
