from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_userprofile_bookmarked_subject'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectBookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_by', to='accounts.subject')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subject_bookmarks', to='accounts.user')),
            ],
        ),
        migrations.AddIndex(
            model_name='subjectbookmark',
            index=models.Index(fields=['user', '-created_at'], name='accounts_su_user_id_5c74ee_idx'),
        ),
    ]
