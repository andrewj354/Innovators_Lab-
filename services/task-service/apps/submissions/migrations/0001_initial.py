# Generated migration for Submission model

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_id', models.IntegerField()),
                ('team_id', models.IntegerField()),
                ('code', models.TextField()),
                ('language', models.CharField(max_length=50)),
                ('status', models.CharField(choices=[('submitted', 'Submitted'), ('evaluating', 'Evaluating'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('partial', 'Partial')], default='submitted', max_length=20)),
                ('passed_tests', models.IntegerField(default=0)),
                ('total_tests', models.IntegerField(default=0)),
                ('score', models.FloatField(default=0.0)),
                ('is_locked', models.BooleanField(default=False)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('evaluated_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'submissions',
                'ordering': ['-submitted_at'],
            },
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['task_id'], name='submissions_task_idx'),
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['team_id'], name='submissions_team_idx'),
        ),
        migrations.AddIndex(
            model_name='submission',
            index=models.Index(fields=['status'], name='submissions_status_idx'),
        ),
    ]
