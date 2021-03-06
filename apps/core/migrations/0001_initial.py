# Generated by Django 2.0.6 on 2019-01-14 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=300, verbose_name='Rua')),
                ('number', models.CharField(blank=True, max_length=20, null=True, verbose_name='Número')),
                ('complement', models.CharField(blank=True, max_length=100, null=True, verbose_name='Complemento')),
                ('reference_point', models.CharField(blank=True, max_length=100, null=True, verbose_name='Ponto de referência')),
                ('latitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
            ],
            options={
                'verbose_name': 'Endereço',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='Cidade')),
                ('latitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
                ('cod_ibge', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cidade',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Razão Social')),
                ('fantasy', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome Fantasia')),
                ('cnpj', models.CharField(blank=True, max_length=22, null=True, verbose_name='CNPJ')),
                ('tse_date', models.DateField(blank=True, null=True, verbose_name='Data de registro no TSE')),
                ('comprovant', models.FileField(blank=True, null=True, upload_to='', verbose_name='Documentos')),
                ('url', models.URLField(blank=True, null=True, verbose_name='URL Website')),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Address')),
            ],
            options={
                'verbose_name': 'Empresa',
            },
        ),
        migrations.CreateModel(
            name='Neighborhood',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=100, null=True, verbose_name='Bairro')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.City')),
            ],
            options={
                'verbose_name': 'Bairro',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=10, verbose_name='CEP')),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('place_type', models.CharField(blank=True, max_length=80, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=12, max_digits=14, null=True)),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.City')),
                ('neighborhood', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.Neighborhood')),
            ],
            options={
                'verbose_name': 'Localidade',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uf', models.CharField(max_length=2, verbose_name='Estado')),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('cod_ibge', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Estado',
            },
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200, verbose_name='Descrição')),
                ('document_file', models.FileField(blank=True, null=True, upload_to='', verbose_name='Termo')),
            ],
            options={
                'verbose_name': 'Termo de uso',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='state',
            field=models.ForeignKey(blank=True, max_length=2, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='core.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.City'),
        ),
        migrations.AddField(
            model_name='address',
            name='neighborhood',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Neighborhood'),
        ),
        migrations.AddField(
            model_name='address',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.Place'),
        ),
        migrations.AddField(
            model_name='address',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='core.State'),
        ),
    ]
