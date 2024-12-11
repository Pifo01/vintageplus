# Variables del proyecto
from .models import Articulos, ArticuloMarca, CategoriaCard, VentaArticulo, Ventas, SoporteTicket, DatosUsuario
from .articulos import COLOR_CHOICES, TIPO_CHOICES, GENERO_CHOICES, TALLAS_CHOICES, PRECIOS
from .forms import ArticuloForm, ArticuloMarcaForm, MarcasCardsForm, DatosCompraForm
from .forms import EditarUsuarioForm
from .forms import SoporteTicketForm
from .forms import UserRegisterForm
from .forms import LoginForm

# Librerias
from django.contrib.auth.decorators import login_required
from django.contrib.sessions.models import Session
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.db import transaction
from django.db.models import Q
from django.conf import settings
from collections import Counter
from datetime import datetime, timedelta
import os
from django.db.models import Prefetch
import json
from django.utils.dateparse import parse_date
from collections import Counter
from django.db.models import Prefetch, Q
from datetime import timedelta, datetime
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import CategoriaCard

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()

            usuario = User.objects.create_user(
                username = form.cleaned_data.get('username'),
                password = form.cleaned_data.get('password'),
                email = form.cleaned_data.get('correo'),
            )
            usuario.save()

            # Buscar DatosUsuario y establecer el valor de usuario
            datos_usuario = DatosUsuario.objects.get(correo=form.cleaned_data.get('correo'))
            datos_usuario.user = usuario
            datos_usuario.save()

            # Autenticar al usuario y iniciar sesión
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                response = redirect("/")
                return response
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})



def SesionIniciada(request) -> bool:
    return request.user.is_authenticated

def VerArticulo(request, id):
    try:
        articulo = Articulos.objects.get(id=id, activo=True)
        todos = Articulos.objects.filter(activo=True).order_by('?')[:9]
        data = {"Articulo": articulo, 'todos': todos}
        return render(request, 'ver-articulo.html', data)
    except Articulos.DoesNotExist:
        messages.error(request, 'El artículo no existe o está deshabilitado.')
        return redirect('index')  # Redirigir a una página segura

def IndexPagina(request):
    articulos = Articulos.objects.filter(activo=True).order_by('?')[:9]
    return render(request, 'index.html', {'Articulos': articulos})

def Index_Create(request):
    if SesionIniciada(request):
        Articulo=Articulos.objects.all() #Select * from Articulo
        Marca=ArticuloMarca.objects.all() #Select * from MarcaS
        cards=CategoriaCard.objects.all() #Select * from Color
        data={'Marca':Marca,'Articulo':Articulo, 'cards':cards, 'EsAdmin':True}
        return render(request,'index-create.html',data)

    return redirect('login')

def Index_Create2(request):
    if SesionIniciada(request):
        Articulo=Articulos.objects.all() #Select * from Articulo
        Marca=ArticuloMarca.objects.all() #Select * from MarcaS
        cards=CategoriaCard.objects.all() #Select * from Color
        data={'Marca':Marca,'Articulo':Articulo, 'cards':cards, 'EsAdmin':True}
        return render(request,'index-create-style.html',data)

    return redirect('login')


def Index_Image(request, image):
    image_path = os.path.join(settings.MEDIA_ROOT, 'imagenes/'+ image)
    try:
        img_file = open(image_path, 'rb')  
        return FileResponse(img_file, content_type='image/jpeg')
    except FileNotFoundError:
        return render("Imagen no encontrada", status=404)

## Cards de articulos ##

def Index_usuario(request):
    articulos = Articulos.objects.filter(activo=True)
    data = {'Articulo': articulos}
    return render(request, 'index.html', data)

def Index_Marcas(request):
    cards = CategoriaCard.objects.filter(activo=True)  
    data = {'cards': cards}
    return render(request, 'marcas.html', data)

def Index_ArticulosMarcaBuscar(request, id):
    Marca = ArticuloMarca.objects.get(id=id) 
    Articulo = Articulos.objects.filter(marca=id, activo=True) 
    data = {'Articulo': Articulo, 'Marca': Marca}
    return render(request, 'marcasbuscadas.html', data)

def Create_Articulos(request):
    form=ArticuloForm()
    if request.method=='POST':
        form=ArticuloForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/categoria")
    data={'form':form,'titulo':'Agregar Articulos'}
    return render(request,'create-Articulos.html',data)

def Create_cards(request):
    if request.method=='POST':
        form=MarcasCardsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/categoria")

    form=MarcasCardsForm()
    data={'form':form,'titulo':'Agregar cards'}
    return render(request,'create-Articulos.html',data)


def Update_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id)
    form=ArticuloForm(instance=Articulo)
    if request.method=='POST':
        form=ArticuloForm(request.POST,request.FILES, instance=Articulo)
        if form.is_valid(): #todos los datos se cargaron
            Articulo.imagen=form.cleaned_data['imagen']
            Articulo.nombre=form.cleaned_data['nombre']
            Articulo.precio=form.cleaned_data['precio']
            Articulo.descripcion=form.cleaned_data['descripcion']
            Articulo.color=form.cleaned_data['color']
            Articulo.genero=form.cleaned_data['genero']
            Articulo.marca=form.cleaned_data['marca']
            Articulo.talla=form.cleaned_data['talla']
            Articulo.tipo=form.cleaned_data['tipo']
            Articulo.save()
        return redirect("/dashboard/articulos")
    data={'form':form,'titulo':'Actualizar Articulos'}
    return render(request,'create-Articulos.html',data)


def Update_cards(request,id):
    cards=CategoriaCard.objects.get(id=id)
    form=MarcasCardsForm(instance=cards)
    if request.method=='POST':
        form=MarcasCardsForm(request.POST,request.FILES, instance=cards)
        if form.is_valid(): #todos los datos se cargaron
            cards.titulo=form.cleaned_data['titulo']
            cards.imagen=form.cleaned_data['imagen']
            MarcaNueva=form.cleaned_data['marca']
            cards.marca=MarcaNueva
            cards.save()
        return redirect("/dashboard/categoria")
    data={'form':form,'titulo':'Actualizar card','prev':'/dashboard/categoria/'}
    return render(request,'create-Articulos.html',data)


def Update_ArticuloMarca(request, id):
    # Obtener la instancia del modelo
    Marca = ArticuloMarca.objects.get(id=id)
    
    # Inicializar el formulario con la instancia existente
    if request.method == 'POST':
        form = ArticuloMarcaForm(request.POST, request.FILES, instance=Marca)
        if form.is_valid():
            # Guardar directamente usando el formulario
            form.save()
            return redirect("/dashboard/marcas")
    else:
        form = ArticuloMarcaForm(instance=Marca)
    
    # Preparar el contexto para la plantilla
    data = {'form': form, 'titulo': 'Actualizar Marca de Artículos'}
    return render(request, 'create-Articulos.html', data)


def Update_Usuario(request, id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    form=EditarUsuarioForm(instance=datos_usuario)
    if request.method=='POST':
        form=EditarUsuarioForm(request.POST, request.FILES, instance=datos_usuario)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/usuarios")
    data={'form':form,'titulo':'Actualizar Usuario','prev':'/dashboard/usuarios/'}
    return render(request,'create-Articulos.html',data)



def Create_ArticuloMarca(request):
    form = ArticuloMarcaForm()
    if request.method == 'POST':
        form = ArticuloMarcaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("/dashboard/marcas")
    data = {'form': form, 'titulo': 'Agregar Marca de Articulos'}
    return render(request, 'create-Articulos.html', data)


@login_required(login_url='login')
def Anular_ArticuloMarca(request, id):
    if not request.user.is_staff:
        raise PermissionDenied

    Marca = get_object_or_404(ArticuloMarca, pk=id)
    
    Marca.activo = False
    Marca.save()

    return redirect('/dashboard/marcas') 

def Toggle_ArticuloMarca(request, marca_id):
    # Obtener la marca usando el ID
    marca = get_object_or_404(ArticuloMarca, id=marca_id)
    
    # Cambiar el estado de 'activo'
    marca.activo = not marca.activo  # Cambia el valor (True a False y viceversa)
    marca.save()

    # Redirigir de vuelta a la lista de marcas
    return redirect('/dashboard/marcas')

def View_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id, activo=True)
    data={"Articulo": Articulo}
    return render(request,'ver-Articulo.html',data)

def View_Usuario(request,id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    data={"datos_usuario": datos_usuario}
    return render(request,'perfil.html',data)

def View_Ticket(request,id):
    Ticket=SoporteTicket.objects.get(id=id)
    data={"Ticket": Ticket}
    return render(request,'ver-ticket.html',data)

def View_cards(request,id):
    card=CategoriaCard.objects.get(id=id)
    data={"card": card}
    return render(request,'ver-card.html',data)

def View_ArticuloMarca(request,id):
    Marca=ArticuloMarca.objects.get(id=id)
    data={"Marca": Marca}
    return render(request,'ver-Marca.html',data)

def Vermercaderia(request):
    if request.method=='POST':
        # Usar la variable "request.body"
        print(request.body)
        body_unicode = request.body.decode('utf-8')
        articulos = json.loads(body_unicode)
        
        # Comienzo de añadir articulos

        # art.id y art.cantidad
        for art in articulos:
            articulo = Articulos.objects.get(id=art['id'])
            articulo.stock = articulo.stock + int(art['cantidad'])
            articulo.save()
        # Fin de añadir articulos

        return HttpResponse(status=200)
    Articulo = Articulos.objects.all()
    data={"Articulo": Articulo}
    return render(request, 'index-admin-mercaderias.html', data)


def Delete_Usuario(request,id):
    datos_usuario=DatosUsuario.objects.get(id=id)
    datos_usuario.activo = False
    datos_usuario.save()
    return redirect("/dashboard/usuarios")


def Delete_Articulos(request,id):
    Articulo=Articulos.objects.get(id=id)
    Articulo.activo = False
    Articulo.save()
    return redirect("/dashboard/articulos")

def Disable_Articulos(request, id):
    try:
        articulo = Articulos.objects.get(id=id)
        articulo.activo = False  # Marcamos como deshabilitado
        articulo.save()
        messages.success(request, f'El artículo "{articulo.nombre}" ha sido deshabilitado.')
    except Articulos.DoesNotExist:
        messages.error(request, 'El artículo no existe.')
    return redirect("/dashboard/articulos")


def Delete_cards(request,id):
    cards=CategoriaCard.objects.get(id=id)
    cards.activo = False
    cards.save()
    return redirect("/dashboard/categoria")


def Delete_ArticuloMarca(request,id):
    MarcaArticulo=ArticuloMarca.objects.get(id=id)
    MarcaArticulo.activo = False
    MarcaArticulo.save()
    return redirect("/dashboard/marcas")

def Index_catalogo(request):
    Articulo = Articulos.objects.filter(stock__gt=0, activo=True)
    Marca = ArticuloMarca.objects.all()  
    
    if request.GET.get('precio'):

        Articulo = Articulos.objects.none()
        GetPrecios = request.GET.get('precio').split(',')
        for precio in GetPrecios:
            PrecioNumero = int(precio)
            Articulo = Articulo | Articulos.objects.filter(precio__range=[PrecioNumero-10000, PrecioNumero], activo=True)
    
    if request.GET.get('color'):
        Colores = request.GET.get('color').split(',')
        Articulo = Articulo.filter(color__in=Colores, activo=True)

    if request.GET.get('genero'):
        Generos = request.GET.get('genero').split(',')
        Articulo = Articulo.filter(genero__in=Generos, activo=True)
    
    if request.GET.get('marca'):
        Marcas = request.GET.get('marca').split(',')
        Articulo = Articulo.filter(marca__in=Marcas, activo=True)
    
    if request.GET.get('talla'):
        Tallas = request.GET.get('talla').split(',')
        Articulo = Articulo.filter(talla__in=Tallas, activo=True)
    
    if request.GET.get('tipo'):
        Tipos = request.GET.get('tipo').split(',')
        Articulo = Articulo.filter(tipo__in=Tipos, activo=True)
    
    Articulo = Articulo[:24]

    data = {
        'Articulo': Articulo,
        'Marca': Marca,
        'Precios': PRECIOS,
        'Colores': COLOR_CHOICES,
        'Tipo': TIPO_CHOICES,
        'Genero': GENERO_CHOICES,
        'Talla': TALLAS_CHOICES
    }
    return render(request, 'catalogo.html', data)


def Login(request):
    data = {}
    form = LoginForm()

    if SesionIniciada(request):
        return redirect("/index")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    response = redirect("/dashboard")
                    return response
                else:
                    data['error'] = "Tu cuenta está deshabilitada. Contacta al administrador."
            else:
                data['error'] = "Usuario o contraseña incorrectos"
    
    data['form'] = form
    return render(request, 'login.html', data)




def shoe_list(request):
    # Manejo de los filtros
    precios = request.GET.getlist('precio')
    colores = request.GET.getlist('color')
    generos = request.GET.getlist('genero')
    marcas = request.GET.getlist('marca')
    tallas = request.GET.getlist('talla')
    tipos = request.GET.getlist('tipo')

    shoes = Articulos.objects.all()

    if precios:
        shoes = shoes.filter(precio__in=precios)
    if colores:
        shoes = shoes.filter(color__in=colores)
    if generos:
        shoes = shoes.filter(genero__in=generos)
    if marcas:
        shoes = shoes.filter(marca__in=marcas)
    if tallas:
        shoes = shoes.filter(talla__in=tallas)
    if tipos:
        shoes = shoes.filter(tipo__in=tipos)

    
    color_choices = COLOR_CHOICES
    genero_choices = GENERO_CHOICES
    talla_choices = TALLAS_CHOICES  
    tipo_choices = TIPO_CHOICES  

    return render(request, 'catalogo.html', {
        'shoes': shoes,
        'Precios': precios,  
        'Colores': color_choices,
        'Genero': genero_choices,
        'Marca': ArticuloMarca.objects.all(),
        'Talla': talla_choices,
        'Tipo': tipo_choices,

    })

def view_carrito(request):
    if request.method == 'POST':
        form_datos_compra = DatosCompraForm(request.POST)
        if form_datos_compra.is_valid():
            # Crear una nueva cuenta de usuario
            user = None
            if form_datos_compra.cleaned_data['crear_usuario']:
                user = User.objects.create_user(
                    username=form_datos_compra.cleaned_data['username'],
                    password=form_datos_compra.cleaned_data['password']
                )
                user.save()

                # Autenticar al usuario
                user = authenticate(username=form_datos_compra.cleaned_data['username'], password=form_datos_compra.cleaned_data['password'])

            # Crear un nuevo valor en el modelo DatosUsuario
            datos_usuario = DatosUsuario.objects.create(
                user=user,
                nombre=form_datos_compra.cleaned_data['nombre'],
                apellido_Paterno=form_datos_compra.cleaned_data['apellido_Paterno'],
                apellido_Materno=form_datos_compra.cleaned_data['apellido_Materno'],
                correo=form_datos_compra.cleaned_data['correo'],
                direccion=form_datos_compra.cleaned_data['direccion'],
                telefono=form_datos_compra.cleaned_data['telefono'],
                codigo_postal=form_datos_compra.cleaned_data['codigo_postal']
            )
            datos_usuario.save()

            return redirect('/carrito/pagar')
            

    carrito = request.session.get('carrito', {})
    Articulo = Articulos.objects.filter(id__in=carrito)
    total = sum(art.precio for art in Articulo)

    form_datos_compra = DatosCompraForm()
    mostrar_modal = not request.user.is_authenticated

    context = {
        'Articulo': Articulo,
        'total': total,
        'Carrito': carrito,
        'form_datos_compra' : form_datos_compra,
        'mostrar_modal': mostrar_modal
    }
    
    return render(request, 'carrito.html', context)

def agregar_al_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    if Articulo.stock <= 0:
        return render(request, 'catalogo.html', {'Mensaje': f"El artículo {Articulo.nombre} está agotado.", 'Redireccionar':'/catalogo'})

    id=str(id)
    carrito = request.session.get('carrito', {})

    if id in carrito:
        carrito[id] += 1
    else:
        carrito[id] = 1

    request.session['carrito'] = carrito

    return redirect('/carrito')

def limpiar_carrito(request):
    request.session['carrito'] = {}
    return redirect('/carrito')


def quitar_del_carrito(request, id):
    id=str(id)
    carrito = request.session.get('carrito', {})

    carrito.pop(id)
    request.session['carrito'] = carrito

    return redirect('/carrito')

def sumar_al_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    id=str(id)
    carrito = request.session.get('carrito', {})

    # Verificar que no sobrepase el stock
    if carrito.get(id, 0) > Articulo.stock:
        return HttpResponse(status=400)

    carrito.update({id: carrito[id] + 1})
    request.session['carrito'] = carrito
    
    # Devolver 200 OK
    return HttpResponse(status=200)

def restar_del_carrito(request, id):
    id=str(id)
    carrito = request.session.get('carrito', {})

    carrito.update({id: carrito[id] - 1})
    if carrito[id] <= 0:
        carrito.pop(id)
    request.session['carrito'] = carrito
    
    # Devolver 200 OK
    return HttpResponse(status=200)

def cambiar_cantidad_carrito(request, id):
    Articulo = get_object_or_404(Articulos, id=id)
    id=str(id)
    parametros_json = request.body.decode('utf-8')
    parametros = json.loads(parametros_json)
    cantidad = parametros["cantidad"]

    if cantidad > Articulo.stock:
        return HttpResponse(status=400)

    carrito = request.session.get('carrito', {})

    carrito.update({id: cantidad})
    request.session['carrito'] = carrito

    return redirect('/carrito')

def pagar_carrito(request):
    carrito = request.session.get('carrito', {})
    carrito_ids = list(carrito.keys())
    total = 0

    factura=[]
    for id in carrito_ids:
        # descontar stock
        SubArticulo = Articulos.objects.get(id=id)
        SubArticulo.stock -= carrito.get(id)
        SubArticulo.save()

        total += SubArticulo.precio * carrito.get(id)
    
        factura.append((SubArticulo, carrito.get(id)))
    
    # Obtener DatosUsuario si el usuario está autenticado
    datos_usuario = None
    if request.user.is_authenticated:
        datos_usuario = DatosUsuario.objects.get(user=request.user)

    # Inicio Procesar pago

    with transaction.atomic():
        Ventafinal = Ventas.objects.create(total=0)

        for articulo_id, cantidad in carrito.items():
            SubArticulo = Articulos.objects.get(id=articulo_id)
            VentaArticulo.objects.create(venta=Ventafinal, articulo=SubArticulo, cantidad=cantidad, datos=datos_usuario)
            
        Ventafinal.total = total
        Ventafinal.save()

    # Fin Procesar pago

    carrito.clear()
    request.session['carrito'] = carrito

    return render(request, 'Carrito.html', {'Mensaje': f"Compra realizada con éxito. Total: ${total}"})

@login_required(login_url='login')
def Dashboard(request):
    if not request.user.is_staff:
        raise PermissionDenied
    return render(request, 'index-admin-dashboard.html')

@login_required(login_url='login')
def DashboardVentas(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Calcular datos generales
    total_productos = Articulos.objects.count()
    total_marcas = ArticuloMarca.objects.count()
    total_categorias = CategoriaCard.objects.count()
    total_stock = sum(articulo.stock for articulo in Articulos.objects.all())

    # Calcular artículos por marca
    articulos_por_marca = Counter(articulo.marca for articulo in Articulos.objects.all())
    marcas = [marca.nombre for marca in ArticuloMarca.objects.all()]
    cantidades = [articulos_por_marca[marca] for marca in marcas]

        # Filtros de búsqueda
    ventas = Ventas.objects.prefetch_related(
        Prefetch(
            'ventaarticulo_set',
            queryset=VentaArticulo.objects.select_related('datos', 'articulo')
        ),
        'articulos'
    ).order_by('-id')

    # Aplicar filtros de rango de fecha y comprador
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    comprador = request.GET.get('comprador') or ""

    if fecha_inicio:
        
        try:
            fecha_inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        except ValueError:
            fecha_inicio = None
    if fecha_fin:
        try:
            fecha_fin = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
        except ValueError:
            fecha_fin = None

    if fecha_inicio and fecha_fin:

        ventas = ventas.filter(fecha__range=[fecha_inicio, fecha_fin])
    elif fecha_inicio:
        ventas = ventas.filter(fecha__gte=fecha_inicio)
    elif fecha_fin:
        ventas = ventas.filter(fecha__lte=fecha_fin)
    if comprador:
        ventas = ventas.filter(ventaarticulo__datos__nombre__icontains=comprador)

    # Optimizar carga de ventas y datos relacionados
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    ventas = ventas.filter(fecha__range=[hace_7_dias, hoy]).order_by('-id')

    """
    hoy = datetime.now()
    hace_7_dias = hoy - timedelta(days=7)
    ventas = ventas.filter(fecha__range=[hace_7_dias, hoy]).prefetch_related(
        Prefetch(
            'ventaarticulo_set',
            queryset=VentaArticulo.objects.select_related('datos', 'articulo')
        )
    ).order_by('-id')

    ventas = ventas.prefetch_related(
        'articulos', 'ventaarticulo_set__datos'
    ).order_by('-id')
    """

    context = {
        'total_productos': total_productos,
        'total_marcas': total_marcas,
        'total_categorias': total_categorias,
        'total_stock': total_stock,
        'marcas': marcas,
        'cantidades': cantidades,
        'ventas': ventas,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'comprador': comprador,
        
    }
    return render(request, 'index-admin-ventas.html', context)

@login_required(login_url='login')
def DashboardTickets(request):
    if not request.user.is_staff:
        raise PermissionDenied
    tickets = SoporteTicket.objects.all()
    return render(request, 'index-admin-soporte.html', {'tickets': tickets})

@login_required(login_url='login')
def DashboardCrud(request):
    if not request.user.is_staff:
        raise PermissionDenied
    articulos = Articulos.objects.all()
    marcas = ArticuloMarca.objects.all()
    cards = CategoriaCard.objects.all()
    return render(request, 'index-admin-crud.html', {'articulos': articulos, 'marcas': marcas, 'cards': cards})

@login_required(login_url='login')
def DashboardArticulos(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Obtener los filtros desde la solicitud
    nombre = request.GET.get('nombre', '').strip()
    precio = request.GET.get('precio', '').strip()
    talla = request.GET.get('talla', '').strip()
    color = request.GET.get('color', '').strip()
    genero = request.GET.get('genero', '').strip()
    tipo = request.GET.get('tipo', '').strip()
    estado = request.GET.get('estado', '').strip()
    pagina = int(request.GET.get('pagina', 1))

    # Filtrar artículos
    articulos = Articulos.objects.all()
    if nombre:
        articulos = articulos.filter(nombre__icontains=nombre)
    if precio:
        articulos = articulos.filter(precio__icontains=precio)
    if talla:
        articulos = articulos.filter(talla__icontains=talla)
    if color:
        articulos = articulos.filter(color__icontains=color)
    if genero:
        articulos = articulos.filter(genero__icontains=genero)
    if tipo:
        articulos = articulos.filter(tipo__icontains=tipo)
    if estado != '':
        articulos = articulos.filter(activo=bool(int(estado)))

    # Paginación
    articulos_por_pagina = 15
    inicio = (pagina - 1) * articulos_por_pagina
    fin = inicio + articulos_por_pagina
    articulos_paginados = articulos[inicio:fin]

    cantidad_articulos = articulos.count()
    cantidad_paginas = (cantidad_articulos + articulos_por_pagina - 1) // articulos_por_pagina
    paginas = list(range(1, cantidad_paginas + 1))

    return render(request, 'index-admin-articulos.html', {
        'Articulos': articulos_paginados,
        'Pagina': pagina,
        'CantidadPaginas': paginas,
        'request': request,
    })

@login_required(login_url='login')
def DashboardMarcas(request):
    if not request.user.is_staff:
        raise PermissionDenied
    pagina = 1
    if request.GET.get('pagina', 1):
        pagina = int(request.GET.get('pagina', 1))

    marca_por_pagina = 15
    inicio = (pagina - 1) * marca_por_pagina
    fin = inicio + marca_por_pagina
    marca = ArticuloMarca.objects.all()[inicio:fin]

    cantidad_marcas = ArticuloMarca.objects.count()
    cantidad_paginas = (cantidad_marcas + marca_por_pagina - 1) // marca_por_pagina
    
    nombre = request.GET.get('nombre', '').strip()
    marca = ArticuloMarca.objects.all()
    if nombre:
        marca = marca.filter(nombre__icontains=nombre)
    

    return render(request, 'index-admin-marcas.html', {'Marca': marca, 'Pagina': pagina, 'CantidadPaginas': cantidad_paginas})

@login_required(login_url='login')
def DashboardCards(request):
    if not request.user.is_staff:
        raise PermissionDenied
    
    pagina = int(request.GET.get('pagina', 1))
    card_por_pagina = 15
    titulo = request.GET.get('titulo', '').strip()
    
    CardQueryset = CategoriaCard.objects.all()
    if titulo:
        CardQueryset = CardQueryset.filter(titulo__icontains=titulo)
    
    cantidad_card = CardQueryset.count()
    cantidad_paginas = (cantidad_card + card_por_pagina - 1) // card_por_pagina
    
    inicio = (pagina - 1) * card_por_pagina
    fin = inicio + card_por_pagina
    Card = CardQueryset[inicio:fin]
    
    return render(
        request, 
        'index-admin-categorias.html', 
        {
            'cards': Card, 
            'Pagina': pagina, 
            'CantidadPaginas': cantidad_paginas,
            'titulo': titulo
        }
    )

@login_required(login_url='login')
def toggle_categoria(request, id):
    if not request.user.is_staff:
        raise PermissionDenied
    
    categoria = get_object_or_404(CategoriaCard, id=id)
    categoria.activo = not categoria.activo
    categoria.save()

    if request.is_ajax():  # Para solicitudes AJAX
        return JsonResponse({'status': 'success', 'activo': categoria.activo})
    return redirect(request.META.get('HTTP_REFERER', '/dashboard/categoria/'))


@login_required(login_url='login')
def DashboardUsuario(request):
    if not request.user.is_staff:
        raise PermissionDenied

    # Obtener filtros desde la solicitud
    nombre = request.GET.get('nombre', '').strip()
    rut = request.GET.get('rut', '').strip()
    estado = request.GET.get('estado', '').strip()
    pagina = int(request.GET.get('pagina', 1))

    # Filtrar usuarios
    usuarios = DatosUsuario.objects.all()
    if nombre:
        usuarios = usuarios.filter(nombre__icontains=nombre)
    if rut:
        usuarios = usuarios.filter(rut__icontains=rut)
    if estado != '':
        usuarios = usuarios.filter(activo=bool(int(estado)))

    # Paginación
    usuario_por_pagina = 15
    inicio = (pagina - 1) * usuario_por_pagina
    fin = inicio + usuario_por_pagina
    usuarios_paginados = usuarios[inicio:fin]

    cantidad_usuario = usuarios.count()
    cantidad_paginas = (cantidad_usuario + usuario_por_pagina - 1) // usuario_por_pagina

    return render(request, 'index-admin-usuarios.html', {
        'datos_usuario': usuarios_paginados,
        'Pagina': pagina,
        'CantidadPaginas': cantidad_paginas,
        'nombre': nombre,
        'rut': rut,
        'estado': estado,
    })
    
def buscar(request):
    query = request.GET.get('q')

    if query:
        # Filtrar en ambos modelos usando Q objects
        resultados_articulos = Articulos.objects.filter(
            Q(nombre__icontains=query) | Q(marca__nombre__icontains=query)
        )
        resultados_marcas = ArticuloMarca.objects.filter(
            Q(nombre__icontains=query) | Q(linea__icontains=query)
        )
    
        return render(request, 'resultados_busqueda.html', {
            'query': query,
            'resultados_articulos': resultados_articulos,
            'resultados_marcas': resultados_marcas
        })
    
    return render(request, 'resultados_busqueda.html', {
        'query': query,
        'resultados_articulos': None,
        'resultados_marcas': None
    })

def CrearTicketSoporte(request):
    if request.method == 'POST':
        form = SoporteTicketForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket creado con éxito.')
            return redirect('/soporte')
    else:
        form = SoporteTicketForm()
    return render(request, 'soporte-ticket.html', {'form': form})

def MarcarComoResueltoView(request, id):
    ticket = get_object_or_404(SoporteTicket, id=id)
    ticket.resuelto = True
    ticket.save()
    return redirect('/dashboard/soporte/')


def Index_perfil(request):
    # Obtener la sesion
    session = get_object_or_404(Session, session_key=request.COOKIES.get("sessionid"))
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')

    # Obtener el usuario
    user = get_object_or_404(User, id=uid)
    
    # Obtener datosusuario usando el usuario
    datos_usuario = get_object_or_404(DatosUsuario, user_id=user.id)

    """
    if request.method == 'POST':
        form = DatosCompraForm(request.POST, instance=datos_usuario)
        if form.is_valid():
            form.save()
            return redirect('perfil_usuario')
    else:
        form = DatosCompraForm(instance=datos_usuario)
    """

    context = {
        # 'form': form,
        'datos_usuario': datos_usuario,
    }
    return render(request, 'perfil.html', context)


def Update_Perfil(request):
    session = get_object_or_404(Session, session_key=request.COOKIES.get("sessionid"))
    session_data = session.get_decoded()
    uid = session_data.get('_auth_user_id')

    # Obtener el usuario
    user = get_object_or_404(User, id=uid)
    
    # Obtener datosusuario usando el usuario
    datos_usuario = get_object_or_404(DatosUsuario, user_id=user.id)

    form=EditarUsuarioForm(instance=datos_usuario)
    if request.method=='POST':
        form=EditarUsuarioForm(request.POST, request.FILES, instance=datos_usuario)
        if form.is_valid():
            form.save()
        return redirect("/profile")
    data={'form':form,'titulo':'Actualizar Usuario','prev':'/profile'}
    return render(request,'create-Articulos.html',data)



def Disable_Articulos(request, id):
    try:
        articulo = Articulos.objects.get(id=id)
        articulo.activo = False  # Marcamos como deshabilitado
        articulo.save()
        messages.success(request, f'El artículo "{articulo.nombre}" ha sido deshabilitado.')
    except Articulos.DoesNotExist:
        messages.error(request, 'El artículo no existe.')
    return redirect("/dashboard/articulos")

def Habilitar_Articulo(request, id):
    articulo = get_object_or_404(Articulos, id=id)
    
    articulo.activo = True
    articulo.save()
    return redirect('/dashboard/articulos')


@login_required
def deshabilitar_usuario(request, user_id):
    usuario = get_object_or_404(DatosUsuario, id=user_id)
    if usuario.activo:
        usuario.activo = False
        usuario.save()
    return redirect('/dashboard/usuarios')

@login_required
def habilitar_usuario(request, user_id):
    usuario = get_object_or_404(DatosUsuario, id=user_id)
    if not usuario.activo:
        usuario.activo = True
        usuario.save()
    return redirect('/dashboard/usuarios')

@login_required(login_url='login')
def AnularVenta(request, id):
    if not request.user.is_staff:
        raise PermissionDenied

    try:
        venta = Ventas.objects.get(id=id)
        venta.anulada = True
        venta.save()
        messages.success(request, f"La venta #{id} ha sido anulada correctamente.")
    except Ventas.DoesNotExist:
        messages.error(request, "La venta no existe.")
    
    return redirect('/dashboard/ventas/')