import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_userprofile_recent_course'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='recent_course',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='recent_course_updated_at',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bookmarked_subject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bookmarked_users', to='accounts.subject'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='bookmarked_subject_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
