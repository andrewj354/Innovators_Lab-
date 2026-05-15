# Generated migration for Task and TaskRequirement models

from django.db import migrations, models
import django.db.models.deletion
import django.core.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tournament_id', models.IntegerField()),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('difficulty', models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=20)),
                ('status', models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', max_length=20)),
                ('time_limit', models.IntegerField(help_text='Time limit in minutes', validators=[django.core.validators.MinValueValidator(1)])),
                ('memory_limit', models.IntegerField(help_text='Memory limit in MB', validators=[django.core.validators.MinValueValidator(1)])),
                ('points', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'tasks',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TaskRequirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input_data', models.TextField()),
                ('expected_output', models.TextField()),
                ('is_sample', models.BooleanField(default=False, help_text='Is this a sample test case?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requirements', to='tasks.task')),
            ],
            options={
                'db_table': 'task_requirements',
                'ordering': ['id'],
            },
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['tournament_id'], name='tasks_tournament_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status'], name='tasks_status_idx'),
        ),
    ]
