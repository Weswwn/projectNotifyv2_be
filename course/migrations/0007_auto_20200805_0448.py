# Generated by Django 3.0.7 on 2020-08-05 04:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_usercourses_sms_message_sid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usercourses',
            old_name='text_sent',
            new_name='did_text_send',
        ),
    ]
