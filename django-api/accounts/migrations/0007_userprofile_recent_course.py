import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_achievement_userachievement'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='recent_course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recent_users', to='accounts.course'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='recent_course_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
