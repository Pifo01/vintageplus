import django
import os

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ProyectoBD.settings')
django.setup()

from appBD.models import Articulos, ArticuloMarca, CategoriaCard, VentaArticulo, Ventas, DatosUsuario
from django.contrib.auth.models import User

def delete_all_data():
    Articulos.objects.all().delete()
    ArticuloMarca.objects.all().delete()
    CategoriaCard.objects.all().delete()
    VentaArticulo.objects.all().delete()
    Ventas.objects.all().delete()
    DatosUsuario.objects.all().delete()
    # eliminar los usuarios que no tengan username "milky"
    User.objects.exclude(username='milky').delete()
    print("Todos los datos han sido eliminados.")

if __name__ == '__main__':
    delete_all_data()