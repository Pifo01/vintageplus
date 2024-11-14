from django.contrib.auth.models import User
from django.db import models

from .articulos import TIPO_CHOICES, COLOR_CHOICES, GENERO_CHOICES, TALLAS_CHOICES


class ArticuloMarca(models.Model):
    nombre = models.CharField(max_length=50)
    empresa = models.CharField(max_length=50)
    linea = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.nombre


class Articulos(models.Model):
    imagen = models.ImageField(upload_to='imagenes/') 
    nombre = models.CharField(max_length=50)
    precio = models.IntegerField()
    descripcion = models.CharField(max_length=150)
    stock = models.IntegerField()
    marca = models.ForeignKey(ArticuloMarca, on_delete=models.CASCADE, default=1, null=False)
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES)
    talla = models.CharField(max_length=20, choices=TALLAS_CHOICES)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)


class CategoriaCard(models.Model):
    titulo = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='imagenes/')  
    marca = models.ForeignKey(ArticuloMarca, on_delete=models.CASCADE, default=1, null=False)

class SoporteTicket(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    nombre = models.CharField(max_length=50)
    correo = models.EmailField()
    mensaje = models.TextField()
    resuelto = models.BooleanField(default=False)

class DatosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    nombre = models.CharField(max_length=100, null=False) 
    rut = models.IntegerField(unique=True, default=12345678, null=False)  # Agregado unique=True
    digito_verificador = models.CharField(default=1, max_length=1, null=False)
    apellido_Paterno = models.CharField(max_length=100, null=False)
    apellido_Materno = models.CharField(max_length=100, null=False)
    correo = models.EmailField(null=False)
    direccion = models.CharField(max_length=100, null=False)
    telefono = models.CharField(max_length=15, null=False)
    codigo_postal = models.CharField(max_length=15, null=False)

    def rut_completo(self):
        rut_str = f"{self.rut:,}".replace(",", ".")
        return f"{rut_str}-{self.digito_verificador}"

class Ventas(models.Model):
    fecha = models.DateField(auto_now_add=True)
    total = models.IntegerField()
    articulos = models.ManyToManyField(Articulos, through='VentaArticulo')

class VentaArticulo(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    datos = models.ForeignKey(DatosUsuario, on_delete=models.CASCADE, null=True, blank=True)