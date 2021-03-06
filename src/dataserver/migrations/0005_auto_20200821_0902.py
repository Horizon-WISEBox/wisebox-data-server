# Generated by Django 3.0.6 on 2020-08-21 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dataserver', '0004_devicesession_location'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='description',
            new_name='notes',
        ),
        migrations.RenameField(
            model_name='location',
            old_name='description',
            new_name='notes',
        ),
        migrations.AddField(
            model_name='location',
            name='organisation',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='dataserver.Organisation'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('name', 'organisation')},
        ),
        migrations.AddIndex(
            model_name='location',
            index=models.Index(fields=['name'], name='dataserver__name_e112aa_idx'),
        ),
    ]
