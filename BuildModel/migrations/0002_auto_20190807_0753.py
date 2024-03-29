# Generated by Django 2.2.3 on 2019-08-07 07:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuildModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builddependency',
            name='buildproject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tobuild', to='BuildModel.BuildProject', unique=True, verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='builddependency',
            name='dependprojects',
            field=models.ManyToManyField(blank=True, related_name='depends', to='BuildModel.BuildProject', verbose_name='Depends'),
        ),
        migrations.AlterField(
            model_name='builddependency',
            name='dir',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Directory'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='buildmode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BuildModel.BuildMode', verbose_name='Build Mode'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='buildproject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BuildModel.BuildProject', verbose_name='Project'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='buildtype',
            field=models.CharField(choices=[('source', 'source'), ('package', 'package')], default='source', max_length=20, verbose_name='Build Type'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='desc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='precondition',
            field=models.TextField(blank=True, max_length=1000, null=True, verbose_name='Pre-condition'),
        ),
        migrations.AlterField(
            model_name='builddetail',
            name='runmode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BuildModel.RunMode', verbose_name='Run Mode'),
        ),
        migrations.AlterField(
            model_name='buildplan',
            name='buildconfig',
            field=models.ManyToManyField(to='BuildModel.BuildDetail', verbose_name='Build Config'),
        ),
        migrations.AlterField(
            model_name='buildplan',
            name='desc',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='buildplan',
            name='ostype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ConfigModel.OSType', verbose_name='OS Type'),
        ),
    ]
