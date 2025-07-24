from django.shortcuts import render

# Create your views here.
def menu(request):
    return render(request, 'pages/index.html', context={  
    })

def login(request):
    return render(request, 'pages/login.html', context={})
    