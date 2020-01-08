from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def development_team(request):
    return render(request, 'development_team.html')