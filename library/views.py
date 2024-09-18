from django.shortcuts import render
from book.models import  Book
from catagory.models import Catagory


def home(request,catagory_slug=None):
    data=Book.objects.all()
    if catagory_slug is not None:
      catagory=Catagory.objects.get(slug=catagory_slug)
      data=Book.objects.filter(catagory=catagory)

    catagory=Catagory.objects.all()
   
    return render(request,'home.html',{'data':data,'catagory':catagory,})