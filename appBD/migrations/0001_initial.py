# Generated by Django 3.1.1 on 2024-12-02 21:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticuloMarca',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('empresa', models.CharField(max_length=50)),
                ('linea', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Articulos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagenes/')),
                ('nombre', models.CharField(max_length=50, unique=True)),
                ('precio', models.IntegerField()),
                ('descripcion', models.CharField(max_length=150)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('color', models.CharField(choices=[('rojo', 'Rojo'), ('azul', 'Azul'), ('negro', 'Negro'), ('blanco', 'Blanco'), ('verde', 'Verde'), ('gris', 'Gris'), ('amarillo', 'Amarillo'), ('morado', 'Morado'), ('naranja', 'Naranja'), ('rosa', 'Rosa'), ('marrón', 'Marrón'), ('dorado', 'Dorado'), ('plateado', 'Plateado')], max_length=20)),
                ('genero', models.CharField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('unisex', 'Unisex'), ('niño', 'Niño'), ('niña', 'Niña'), ('preescolar', 'Preescolar'), ('escolar', 'Escolar')], max_length=20)),
                ('talla', models.CharField(choices=[('XS', 'XS'), ('S', 'S'), ('M', 'M'), ('L', 'L'), ('XL', 'XL'), ('XXL', 'XXL')], max_length=20)),
                ('tipo', models.CharField(choices=[('camisa', 'Camisa'), ('pantalon', 'Pantalón'), ('falda', 'Falda'), ('chaqueta', 'Chaqueta'), ('abrigo', 'Abrigo'), ('sueter', 'Suéter'), ('vestido', 'Vestido'), ('short', 'Short'), ('blusa', 'Blusa')], max_length=20)),
                ('marca', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appBD.articulomarca')),
            ],
        ),
        migrations.CreateModel(
            name='DatosUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.IntegerField(default=12345678, unique=True)),
                ('digito_verificador', models.CharField(default=1, max_length=1)),
                ('apellido_Paterno', models.CharField(max_length=100)),
                ('apellido_Materno', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=254)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('codigo_postal', models.CharField(max_length=15)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SoporteTicket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('mensaje', models.TextField()),
                ('resuelto', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='VentaArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('articulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBD.articulos')),
                ('datos', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='appBD.datosusuario')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('total', models.IntegerField()),
                ('articulos', models.ManyToManyField(through='appBD.VentaArticulo', to='appBD.Articulos')),
            ],
        ),
        migrations.AddField(
            model_name='ventaarticulo',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appBD.ventas'),
        ),
        migrations.CreateModel(
            name='CategoriaCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, unique=True)),
                ('imagen', models.ImageField(upload_to='imagenes/')),
                ('marca', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='appBD.articulomarca')),
            ],
        ),
    ]
