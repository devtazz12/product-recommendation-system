from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import requests
from bs4 import BeautifulSoup
import random
from .models import ScrappedProduct,Search,recommend_product,sastodeal_product,recommend_product_sastodeal,socheko_product,recommend_product_socheko
import numpy as np
from django.core.paginator import Paginator

import pickle
# from daraz
# popular_df= pickle.load(open('home/result_daraz.pkl','rb'))
pt= pickle.load(open('home/pt_daraz.pkl','rb'))
similarity_score= pickle.load(open('home/similarity_score_daraz.pkl','rb'))
final_data= pickle.load(open('home/final_data_daraz.pkl','rb'))


# from sastodeal
# popular_df= pickle.load(open('home/result_sastodeal.pkl','rb'))
pt_sastodeal= pickle.load(open('home/pt_sastodeal.pkl','rb'))
similarity_score_sastodeal= pickle.load(open('home/similarity_score_sastodeal.pkl','rb'))
final_data_sastodeal= pickle.load(open('home/final_data_sastodeal.pkl','rb'))

# from socheko
popular_df= pickle.load(open('home/result_socheko.pkl','rb'))
pt_socheko= pickle.load(open('home/pt_socheko.pkl','rb'))
similarity_score_socheko= pickle.load(open('home/similarity_score_socheko.pkl','rb'))
final_data_socheko= pickle.load(open('home/final_data_socheko.pkl','rb'))

# to insert data into database

avg_rating=[]
title=[]
img_url=[]
link=[]
price=[]
dprice=[]
perdis=[]
for i in popular_df['title']:
  title.append(i)
for i in popular_df['rating']:
  avg_rating.append(i)
for i in popular_df['image']:
  img_url.append(i)
for i in popular_df['link']:
  link.append(i)
# for i in popular_df['currency--GVKjl 2']:
#   price.append(i)

for i in popular_df['dprice']: 
  dprice.append(i)

# for i in popular_df['discount--HADrg']:
#   perdis.append(i)


# socheko_product.objects.all().delete()

products= socheko_product.objects.all().count()
if products == 0:
   for n in range(0,814):
      socheko_product.objects.create(
        title = title[n],
        image = img_url[n],
        rating = avg_rating[n],
        link= link[n],
        dprice= dprice[n]      
      )

    
# end of insertion of data
  


# Create your views here.

#for daraz recommendation system


def productDetail(request,productId):
  productFromDB = ScrappedProduct.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'price': productFromDB.price,
    'dprice':productFromDB.dprice,
    'perdis':productFromDB.perdis
  }


  user_input=productFromDB.title
  
  index=np.where(pt.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data[final_data['title--wFj93']==pt.index[i[0]]]
    title= temp_df.drop_duplicates('title--wFj93')['title--wFj93'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('title--wFj93')['mainPic--ehOdr href'].values
    img_url=temp_df.drop_duplicates('title--wFj93')['image--WOyuZ src'].values
    rating=temp_df.drop_duplicates('title--wFj93')['rating'].values
    price=temp_df.drop_duplicates('title--wFj93')['currency--GVKjl 2'].values
    dprice=temp_df.drop_duplicates('title--wFj93')['currency--GVKjl'].values
    perdis=temp_df.drop_duplicates('title--wFj93')['discount--HADrg'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['price']=price[0]
    item['dprice']=dprice[0]
    item['perdis']=perdis[0]
    
    recommend_product.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        price= price[0],
        dprice= dprice[0],
        perdis= perdis[0]
      )
        
   
  recommendproductfromDB = recommend_product.objects.all()

  return render(request,"productDetail.html",{'product':product, 'data':recommendproductfromDB})


def recommendDetail(request,productId):
  productFromDB = recommend_product.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'price': productFromDB.price,
    'dprice':productFromDB.dprice,
    'perdis':productFromDB.perdis
  }


  user_input=productFromDB.title
  
  index=np.where(pt.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data[final_data['title--wFj93']==pt.index[i[0]]]
    title= temp_df.drop_duplicates('title--wFj93')['title--wFj93'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('title--wFj93')['mainPic--ehOdr href'].values
    img_url=temp_df.drop_duplicates('title--wFj93')['image--WOyuZ src'].values
    rating=temp_df.drop_duplicates('title--wFj93')['rating'].values
    price=temp_df.drop_duplicates('title--wFj93')['currency--GVKjl 2'].values
    dprice=temp_df.drop_duplicates('title--wFj93')['currency--GVKjl'].values
    perdis=temp_df.drop_duplicates('title--wFj93')['discount--HADrg'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['price']=price[0]
    item['dprice']=dprice[0]
    item['perdis']=perdis[0]
    
    recommend_product.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        price= price[0],
        dprice= dprice[0],
        perdis= perdis[0]
      )
        
   
  recommendproductfromDB = recommend_product.objects.all()

  return render(request,"productDetail.html",{'product':product, 'data':recommendproductfromDB})

# end of daraz recommendation system
#start of sastodeal recommendation system
def product_detail_sastodeal(request, productId):
  productFromDB = sastodeal_product.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'dprice':productFromDB.dprice,
  }


  user_input=productFromDB.title
  
  index=np.where(pt_sastodeal.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score_sastodeal[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product_sastodeal.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data_sastodeal[final_data_sastodeal['product-item-link']==pt_sastodeal.index[i[0]]]
    title= temp_df.drop_duplicates('product-item-link')['product-item-link'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('product-item-link')['product href'].values
    img_url=temp_df.drop_duplicates('product-item-link')['product-image-wrapper src'].values
    rating=temp_df.drop_duplicates('product-item-link')['rating'].values
    dprice=temp_df.drop_duplicates('product-item-link')['price'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['dprice']=dprice[0]
    
    recommend_product_sastodeal.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        dprice= dprice[0],
      )
        
   
  recommendproductfromDB = recommend_product_sastodeal.objects.all()

  return render(request,"productDetailsastodeal.html",{'product':product, 'data':recommendproductfromDB})


def recommend_detail_sastodeal(request, productId):
  productFromDB = recommend_product_sastodeal.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'dprice':productFromDB.dprice,
  }


  user_input=productFromDB.title
  
  index=np.where(pt_sastodeal.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score_sastodeal[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product_sastodeal.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data_sastodeal[final_data_sastodeal['product-item-link']==pt_sastodeal.index[i[0]]]
    title= temp_df.drop_duplicates('product-item-link')['product-item-link'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('product-item-link')['product href'].values
    img_url=temp_df.drop_duplicates('product-item-link')['product-image-wrapper src'].values
    rating=temp_df.drop_duplicates('product-item-link')['rating'].values
    dprice=temp_df.drop_duplicates('product-item-link')['price'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['dprice']=dprice[0]
    
    recommend_product_sastodeal.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        dprice= dprice[0],
      )
        
   
  recommendproductfromDB = recommend_product_sastodeal.objects.all()

  return render(request,"productDetailsastodeal.html",{'product':product, 'data':recommendproductfromDB})


  # end of sastodeal system

  #start of socheko system
def product_detail_socheko(request, productId):
  productFromDB = socheko_product.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'dprice':productFromDB.dprice,
  }


  user_input=productFromDB.title
  
  index=np.where(pt_socheko.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score_socheko[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product_socheko.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data_socheko[final_data_socheko['title']==pt_socheko.index[i[0]]]
    title= temp_df.drop_duplicates('title')['title'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('title')['link'].values
    img_url=temp_df.drop_duplicates('title')['image'].values
    rating=temp_df.drop_duplicates('title')['rating'].values
    dprice=temp_df.drop_duplicates('title')['dprice'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['dprice']=dprice[0]
    
    recommend_product_socheko.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        dprice= dprice[0],
      )
        
   
  recommendproductfromDB = recommend_product_socheko.objects.all()
  return render(request, 'productDetailsocheko.html',{'product':product, 'data':recommendproductfromDB})

def recommend_detail_socheko(request, productId):
  productFromDB = recommend_product_socheko.objects.get(pk=productId)
  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating,
    'link': productFromDB.link,
    'dprice':productFromDB.dprice,
  }


  user_input=productFromDB.title
  
  index=np.where(pt_socheko.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score_socheko[index])), key=lambda x:x[1],reverse=True)[1:5]
  recommend_product_socheko.objects.all().delete()
  for i in similar_items:
    item={}
    temp_df=final_data_socheko[final_data_socheko['title']==pt_socheko.index[i[0]]]
    title= temp_df.drop_duplicates('title')['title'].values
    item['title']=title[0]
    link=temp_df.drop_duplicates('title')['link'].values
    img_url=temp_df.drop_duplicates('title')['image'].values
    rating=temp_df.drop_duplicates('title')['rating'].values
    dprice=temp_df.drop_duplicates('title')['dprice'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
    item['link']=link[0]
    item['dprice']=dprice[0]
    
    recommend_product_socheko.objects.create(
        title = title[0],
        image = img_url[0],
        rating = rating[0],
        link= link[0],
        dprice= dprice[0],
      )
        
   
  recommendproductfromDB = recommend_product_socheko.objects.all()
  return render(request, 'productDetailsocheko.html',{'product':product, 'data':recommendproductfromDB})



  #end of socheko system




def index(request):

  productsFromDB = ScrappedProduct.objects.all()[98:102]
  sastodealproduct = sastodeal_product.objects.all()[0:4]
  sochekoproduct = socheko_product.objects.all()[0:4]
  dict={
    'popularlist':productsFromDB,
    'sastodealproduct':sastodealproduct,
    'sochekoproduct':sochekoproduct
  }

  return render(request, 'index.html', dict)
   # return HttpResponse("this is about page")

def about(request):
   
   return render(request, "about.html")
   # return HttpResponse("this is about page")

def contact(request):
  #this is process of sending information of user in the database.

  if request.method == "POST":
     name = request.POST.get('name')
     email = request.POST.get('email')
     desc = request.POST.get('desc')
     contact = Contact(name=name,email=email,desc=desc,date=datetime.today())
     contact.save()
     messages.success(request, 'Your message has been sent!')
  return render(request, "contact.html")


def loginUser(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # check if user has entered corect credentials or not
        user = authenticate(username=username, password=password)
        if user is not None:
          # A backend authenticated the credentials
          login(request, user)
          return redirect("/")
        else:
          # No backend authenticated the credentials
          return render(request, 'login.html')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    return redirect("/login")


def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        error_message = None
        if pass1!=pass2:
          error_message ='your confirm password donot match with password'    

   

   # check for errorneous inputs
        if not error_message:
   #create the user
          myuser = User.objects.create_user(username, email, pass1)
          myuser.first_name = fname
          myuser.last_name =lname
          myuser.save()
          messages.success(request, "your account has been successfully created")
          login(request, myuser)
          return redirect('/login')
        else:
          return render(request, 'login.html', {'error':error_message})  

    else: 
        return HttpResponse('404 Error - Not Found') 


def daraz(request):

  productsFromDB = ScrappedProduct.objects.get_queryset().order_by('id')
  paginator=Paginator(productsFromDB, 50)
  page_number=request.GET.get('page')
  if page_number==None:
    page_number=1
  product=paginator.get_page(page_number)
  
  return render(request, "daraz.html",{'popularlist':product ,'page_number':page_number})



def sastodeal(request):

  sastodealproduct = sastodeal_product.objects.get_queryset().order_by('id')
  paginator=Paginator(sastodealproduct, 50)
  page_number=request.GET.get('page')
  if page_number==None:
    page_number=1
  product=paginator.get_page(page_number)
  
  return render(request, "sastodeal.html",{ 'page_number':page_number, 'sastodealproduct':product})


def socheko(request):
  sochekoproduct = socheko_product.objects.get_queryset().order_by('id')
  paginator=Paginator(sochekoproduct, 50)
  page_number=request.GET.get('page')
  if page_number==None:
    page_number=1
  product=paginator.get_page(page_number)
  return render(request, "socheko.html",{ 'page_number':page_number, 'sochekoproduct':product})