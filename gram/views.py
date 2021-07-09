from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import request,HttpResponse
from django.contrib import messages
import pdb
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import datetime as dt
# Create your views here.

def register(request):
    return HttpResponse('Hello')


