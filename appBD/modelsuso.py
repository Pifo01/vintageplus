from django.db import transaction
from django.shortcuts import render
from .models import Ventas, VentaArticulo, Articulos

def crear_venta(articulos_cantidades: list[int, int] = None) -> None:
    """
    Crea una nueva venta y asocia los artículos con sus respectivas cantidades.
    
    :param articulos_cantidades: Lista de tuplas (articulo_id, cantidad)
    """
    with transaction.atomic():
        # Crear una nueva venta
        venta = Ventas.objects.create(total=0)  # El total se actualizará más adelante

        total: int = 0
        for articulo_id, cantidad in articulos_cantidades:
            # Recuperar el artículo
            articulo: Articulos = Articulos.objects.get(id=articulo_id)
            
            # Crear la relación en VentaArticulo
            VentaArticulo.objects.create(venta=venta, articulo=articulo, cantidad=cantidad)
            
            # Actualizar el total de la venta
            total += articulo.precio * cantidad
        
        # Actualizar el total de la venta
        venta.total = total
        venta.save()

# Ejemplo de uso
articulos_cantidades = [
    (1, 2),  # Artículo con ID 1, cantidad 2
    (2, 1)   # Artículo con ID 2, cantidad 1
]
crear_venta(articulos_cantidades)


def ultimas_ventas(request):
    # Obtener las últimas 5 ventas ordenadas por fecha descendente
    ventas = Ventas.objects.order_by('-fecha')[:5]
    
    # Pasar las ventas al contexto de la plantilla
    context: dict[str | any] = {
        'ventas': ventas
    }
    
    # Renderizar la plantilla
    return render(request, 'ultimas_ventas.html', context)