from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .forms import registroUsuariosForm, inicioSesionForm


# Variables
DOCLENGTHMIN = 6 #Minimo de carácteres para el documento
PASSLENGTHMIN = 8 #Minimo de carácteres para la contraseña
#Arrays - listas
adminIds = [0, 1]

#Notificaciones
EXITO_1 = "El usuario ha sido creado correctamente."
ERROR_1 = "El documento que intentó ingresar, ya existe."
ERROR_2 = "Formulario inválido."
ERROR_3 = "Error desconocido."
ERROR_4 = "Usuario o contraseña incorrecta."
ERROR_5 = "Este usuario no pudo ser redireccionado. Comunique este error."
ERROR_6 = "Usuario o documento demasiado corto(s)."
#-----------Functions----------#
def stripForm(form):
    for campo in form.fields:
        if isinstance(form.cleaned_data[campo], str):
            form.cleaned_data[campo] = form.cleaned_data[campo].strip()
    return form 


# Create your views here.
def Home(request):
    newForm = inicioSesionForm()
    if request.method == 'POST':
        form = inicioSesionForm(request.POST)
        if form.is_valid():
            form = stripForm(form)
            
            documento = form.cleaned_data['documento']
            password = form.cleaned_data['password']
            
            #Verificar el minimo de carácteres para cada campo
            if len(documento) < DOCLENGTHMIN or len(password) < PASSLENGTHMIN:
                recycledForm = inicioSesionForm(initial={'documento': documento})
                return render(request, "home.html", {'form': recycledForm,
                                                     'error': ERROR_6})
            
            logedUser = authenticate(request, username=documento, password=password)
            
            #Verificar que el usuario exista y su contraseña sea correcta
            if logedUser is None:
                recycledForm = inicioSesionForm(initial={'documento': documento})
                return render(request, "home.html", {'form': recycledForm,
                                                    'error':ERROR_4})
            else:
                login(request, logedUser)
                userType = logedUser.tipo_usuario_id
                print(f"-------------->usertype {userType}")
                if userType == 0:
                    return redirect(reverse('registro'))
                elif userType == 1:
                    return redirect(reverse('registro'))
                elif userType == 2:
                    return redirect(reverse('registro'))
                elif userType == 3:
                    return redirect(reverse('registro'))
                elif userType == 4:
                    return redirect(reverse('registro'))
                else:
                    logout(request)
                    return render(request, "home.html", {'form': newForm,
                                                         'error': ERROR_5})
        else:
            return render(request, "home.html",{'form':newForm,
                                                'error': ERROR_2})
    return render(request, "home.html", {'form': newForm})

def Registro(request):
    newForm = registroUsuariosForm()
    if request.method == "POST":
        form = registroUsuariosForm(request.POST)
        #Verificar que el documento no se haya registrado antes.
        if form.has_error("username", code="unique"):
            return render(request, "registro.html", {
                    "form": form,
                    "evento": ERROR_1,
                    "exito": False,
                })
        
        #Verificar la validez del formulario (campos en blanco, tipos de datos correctos)
        if form.is_valid():
            #Quitar espacios al principio y al final de los campos de texto
            form = stripForm(form)
            #Guardar el usuario nuevo
            try:
                documento = form.cleaned_data['username']
                password = form.cleaned_data['password']
                
                if len(documento) < DOCLENGTHMIN or len(password) < PASSLENGTHMIN:
                    return render(request, "registro.html", {
                      "form": form,
                      "evento": ERROR_6,
                      "exito": False  
                    })
                
                user = form.save(commit=False)
                user.username = documento
                user.set_password(password)
                user.email = form.cleaned_data['email']
                user.save()
                
                return render(request, "registro.html", {
                    "form": newForm,
                    "evento": EXITO_1,
                    "exito": True,
                    "documento": f"Usuario login: {documento}",
                    "password": f"Contraseña: {form.cleaned_data['password']}"
                })
            except Exception as e:
                return render(request, "registro.html", {
                    "form": form,
                    "evento": ERROR_3,
                    "exito": False,
                })
        else:
            return render(request, "registro.html", {
                    "form": form,
                    "evento": ERROR_2,
                    "exito": False,
                })
    #GET
    return render(request, "registro.html", {'form': newForm })

def Logout(request):
    logout(request)
    return redirect(reverse('home'))