# Generated by Django 2.2.3 on 2019-08-02 02:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ConfigModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BuildDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
                ('buildtype', models.CharField(choices=[('source', 'source'), ('package', 'package')], default='source', max_length=20)),
                ('precondition', models.TextField(blank=True, max_length=1000, null=True)),
                ('options', models.TextField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'verbose_name': 'Build Option',
                'verbose_name_plural': 'Build Option',
                'db_table': 'ATM_BuildDetail',
            },
        ),
        migrations.CreateModel(
            name='BuildMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'ATM_BuildMode',
            },
        ),
        migrations.CreateModel(
            name='BuildProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'db_table': 'ATM_BuildProject',
            },
        ),
        migrations.CreateModel(
            name='RunMode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('desc', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'ATM_RunMode',
            },
        ),
        migrations.CreateModel(
            name='BuildPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('desc', models.CharField(blank=True, max_length=100, null=True)),
                ('version', models.CharField(default='latest', max_length=20)),
                ('gcc_version', models.CharField(blank=True, max_length=50, null=True)),
                ('archived', models.BooleanField(default=False)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ConfigModel.Branch')),
                ('buildconfig', models.ManyToManyField(to='BuildModel.BuildDetail')),
                ('ostype', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ConfigModel.OSType')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ConfigModel.Project')),
            ],
            options={
                'verbose_name': 'Build Plan',
                'verbose_name_plural': 'Build Plan',
                'db_table': 'ATM_BuildPlan',
            },
        ),
        migrations.AddField(
            model_name='builddetail',
            name='buildmode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BuildModel.BuildMode'),
        ),
        migrations.AddField(
            model_name='builddetail',
            name='buildproject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BuildModel.BuildProject'),
        ),
        migrations.AddField(
            model_name='builddetail',
            name='runmode',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='BuildModel.RunMode'),
        ),
        migrations.CreateModel(
            name='BuildDependency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dir', models.CharField(blank=True, max_length=50, null=True)),
                ('buildproject', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tobuild', to='BuildModel.BuildProject', unique=True)),
                ('dependprojects', models.ManyToManyField(blank=True, related_name='depends', to='BuildModel.BuildProject')),
            ],
            options={
                'verbose_name': 'Project Dependency',
                'verbose_name_plural': 'Project Dependency',
                'db_table': 'ATM_BuildDependency',
            },
        ),
    ]
