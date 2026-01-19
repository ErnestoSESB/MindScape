from .forms import UserRegistrationForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django import forms
from .models import Task
from .forms import TaskForm


@login_required(login_url='/login/')
def tasks(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/tasks/')
    else:
        form = TaskForm()
    tasks = Task.objects.order_by('-created_at')
    return render(request, 'pages/task.html', {'form': form, 'tasks': tasks})

@login_required(login_url='/login/')
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/tasks/')
    else:
        form = TaskForm(instance=task)
    tasks = Task.objects.order_by('-created_at')
    return render(request, 'pages/task.html', {'form': form, 'tasks': tasks, 'edit_task': task})

@login_required(login_url='/login/')
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/tasks/')
    return redirect('/tasks/')


class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'seu@email.com'}))
    password = forms.CharField(label='Senha', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': '••••••••'}))

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            raise forms.ValidationError('Email ou senha inválidos.')
        if not user.check_password(password):
            raise forms.ValidationError('Email ou senha inválidos.')
        cleaned_data['user'] = user
        return cleaned_data
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def menu(request):
    user = request.user
    return render(request, 'pages/index.html', {'user': {'name': user.name}})

def login(request):
    if request.method == 'POST':
        form = EmailAuthenticationForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            auth_login(request, user)
            return redirect('/menu/')
        else:
            return render(request, 'pages/login.html', {'form': form})
    else:
        form = EmailAuthenticationForm()
    return render(request, 'pages/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/login')

from django.http import JsonResponse

@login_required(login_url='/login/')
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            return redirect('/tasks/')
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
    else:
        form = TaskForm()
    return render(request, 'pages/create_task.html', {'form': form})


def create_account(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('/login/')
    else:
        form = UserRegistrationForm()
    return render(request, 'pages/create_account.html', {'form': form})

