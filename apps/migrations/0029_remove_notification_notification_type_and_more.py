# Generated by Django 5.0.6 on 2024-06-05 02:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0028_notification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='notification_type',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='notificationtype_ptr',
        ),
        migrations.RemoveField(
            model_name='notification',
            name='recipient',
        ),
        migrations.DeleteModel(
            name='NotificationType',
        ),
        migrations.DeleteModel(
            name='Notification',
        ),
    ]
