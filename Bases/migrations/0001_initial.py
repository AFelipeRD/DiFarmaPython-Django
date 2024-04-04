# Generated by Django 4.1.3 on 2022-11-20 19:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ControlTemperatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fechacontrol', models.DateField(max_length=255, null=True)),
                ('horacontrol', models.TimeField(max_length=255, null=True)),
                ('humedad', models.IntegerField(null=True)),
                ('temperatura', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'ControlTemperatura',
                'verbose_name_plural': 'ControlTemperaturas',
            },
        ),
        migrations.CreateModel(
            name='Egreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pedido', models.DateField(max_length=255)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('pagado', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('comentarios', models.TextField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('ticket', models.BooleanField(default=True)),
                ('desglosar', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now_add=True, null=True)),
            ],
            options={
                'verbose_name': 'Egreso',
                'verbose_name_plural': 'Egresos',
                'order_with_respect_to': 'fecha_pedido',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.IntegerField(null=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('nproveedor', models.CharField(max_length=50, null=True)),
                ('precio', models.IntegerField(null=True)),
                ('cantidad', models.IntegerField()),
                ('laboratorio', models.CharField(max_length=50, null=True)),
                ('presentacion', models.CharField(blank=True, max_length=50, null=True)),
                ('ml', models.IntegerField(blank=True, null=True)),
                ('mg', models.IntegerField(blank=True, null=True)),
                ('vencimiento', models.DateField(max_length=255, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('numpedido', models.IntegerField(null=True)),
                ('fechapedido', models.DateField(max_length=255, null=True)),
                ('contacto', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
            },
        ),
        migrations.CreateModel(
            name='ProductosEgreso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=20)),
                ('precio', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('iva', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('total', models.DecimalField(decimal_places=2, default=0, max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('entregado', models.BooleanField(default=True)),
                ('devolucion', models.BooleanField(default=False)),
                ('egreso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bases.egreso')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bases.producto')),
            ],
            options={
                'verbose_name': 'Producto Egreso',
                'verbose_name_plural': 'Productos Egreso',
                'order_with_respect_to': 'created',
            },
        ),
    ]
