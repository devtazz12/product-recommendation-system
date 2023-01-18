from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from home.models import Contact
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
import requests
from bs4 import BeautifulSoup
import random
from .models import ScrappedProduct,Search
import numpy as np

import pickle
popular_df= pickle.load(open('home/result_daraz.pkl','rb'))
pt= pickle.load(open('home/pt_daraz.pkl','rb'))
similarity_score= pickle.load(open('home/similarity_score_daraz.pkl','rb'))
final_data= pickle.load(open('home/final_data_daraz.pkl','rb'))


avg_rating=[]
title=[]
img_url=[]
link=[]
price=[]
dprice=[]
perdis=[]
for i in popular_df['title--wFj93']:
  title.append(i)

for i in popular_df['rating']:
  avg_rating.append(i)
for i in popular_df['image--WOyuZ src']:
  img_url.append(i)
for i in popular_df['mainPic--ehOdr href']:
  link.append(i)
for i in popular_df['currency--GVKjl 2']:
  price.append(i)
for i in popular_df['currency--GVKjl']:
  dprice.append(i)
for i in popular_df['discount--HADrg']:
  perdis.append(i)


# ScrappedProduct.objects.all().delete()

products= ScrappedProduct.objects.all().count()


if products == 0:
   for n in range(0,3412):
        ScrappedProduct.objects.create(
          title = title[n],
          image = img_url[n],
          rating = round(avg_rating[n],1),
          link= link[n],
          price= price[n],
          dprice= dprice[n],
          perdis= perdis[n]
        )

    

  


# Create your views here.


def searchProductDetail(request,productId):
  if 'element' in request.GET:
    element = request.GET.get('element')
    html_content= get_html_content(element)
    soup= BeautifulSoup(html_content.text, 'html.parser')
    titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
    ratings = soup.findAll('span', {'class':'a-icon-alt'})
    img_urls=soup.find_all('img',{'class':'s-image'})
    title_list=[]
    rating_list=[]
    imgurl_list=[]


    # appending into list 
    for img_url in img_urls:
        if 'jpg' in img_url['src']:
            imgurl_list.append(img_url['src'])

    for title in titles:
        title_list.append(title.text)
    for rating in ratings:
        rating_list.append(rating.text.replace(' out of 5 stars',''))

    Search.objects.all().delete()

    scrap_amz = []
    for m in range(0,13):
        dict_scrap={}
        dict_scrap['title']=title_list[m]
        dict_scrap['image']=imgurl_list[m]
        dict_scrap['rating']=rating_list[m]
        scrap_amz.append(dict_scrap)

        Search.objects.create(
          title = title_list[m],
          image = imgurl_list[m],
          rating = rating_list[m]
        )

    
    products =Search.objects.all()
    


    return render(request, 'search.html', {'scrap_amz':products})

  productFromDB = Search.objects.get(pk=productId)


  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating
  }

  user_input=productFromDB.title
  
  index=np.where(pt.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1],reverse=True)[1:5]
  data=[]
  for i in similar_items:
    item={}
    temp_df=final_data[final_data['title']==pt.index[i[0]]]
    title= temp_df.drop_duplicates('title')['title'].values
    item['title']=title[0]
       
    img_url=temp_df.drop_duplicates('title')['img_url'].values
    rating=temp_df.drop_duplicates('title')['ratings'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
        
    data.append(item)

  return render(request,"productDetail.html",{'product':product, 'data':data})



def productDetail(request,productId):
  if 'element' in request.GET:
    element = request.GET.get('element')
    html_content= get_html_content(element)
    soup= BeautifulSoup(html_content.text, 'html.parser')
    titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
    ratings = soup.findAll('span', {'class':'a-icon-alt'})
    img_urls=soup.find_all('img',{'class':'s-image'})
    title_list=[]
    rating_list=[]
    imgurl_list=[]


    # appending into list 
    for img_url in img_urls:
        if 'jpg' in img_url['src']:
            imgurl_list.append(img_url['src'])

    for title in titles:
        title_list.append(title.text)
    for rating in ratings:
        rating_list.append(rating.text.replace(' out of 5 stars',''))

    Search.objects.all().delete()

    scrap_amz = []
    for m in range(0,13):
        dict_scrap={}
        dict_scrap['title']=title_list[m]
        dict_scrap['image']=imgurl_list[m]
        dict_scrap['rating']=rating_list[m]
        scrap_amz.append(dict_scrap)

        Search.objects.create(
          title = title_list[m],
          image = imgurl_list[m],
          rating = rating_list[m]
        )

    
    products =Search.objects.all()
    


    return render(request, 'search.html', {'scrap_amz':products})


  productFromDB = ScrappedProduct.objects.get(pk=productId)

  product = {
    'title':productFromDB.title,
    'image':productFromDB.image,
    'rating':productFromDB.rating
  }


  user_input=productFromDB.title
  print(user_input)
  
  index=np.where(pt.index==user_input)[0][0]
  similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x:x[1],reverse=True)[1:5]
  data=[]
  for i in similar_items:
    item={}
    temp_df=final_data[final_data['title--wFj93']==pt.index[i[0]]]
    title= temp_df.drop_duplicates('title--wFj93')['title--wFj93'].values
    item['title']=title[0]
       
    img_url=temp_df.drop_duplicates('title--wFj93')['image--WOyuZ src'].values
    rating=temp_df.drop_duplicates('title--wFj93')['rating'].values
    item['image']=img_url[0]
    item['rating']=rating[0]
        
    data.append(item)


  return render(request,"productDetail.html",{'product':product, 'data':data})



def get_html_content(element): 
    headers = {
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Mobile Safari/537.36',
        'Accept-Language': 'en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    response = requests.get(f'https://www.amazon.com/s?k={element}', headers=headers)
    return response

def search(request):
  if request.user.is_anonymous:
    return redirect("/login")
  if 'element' in request.GET:
    element = request.GET.get('element')
    html_content= get_html_content(element)
    soup= BeautifulSoup(html_content.text, 'html.parser')
    titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
    ratings = soup.findAll('span', {'class':'a-icon-alt'})
    img_urls=soup.find_all('img',{'class':'s-image'})
    title_list=[]
    rating_list=[]
    imgurl_list=[]


    # appending into list 
    for img_url in img_urls:
        if 'jpg' in img_url['src']:
            imgurl_list.append(img_url['src'])

    for title in titles:
        title_list.append(title.text)
    for rating in ratings:
        rating_list.append(rating.text.replace(' out of 5 stars',''))

    Search.objects.all().delete()

    scrap_amz = []
    for m in range(0,13):
        dict_scrap={}
        dict_scrap['title']=title_list[m]
        dict_scrap['image']=imgurl_list[m]
        dict_scrap['rating']=rating_list[m]
        scrap_amz.append(dict_scrap)

        Search.objects.create(
          title = title_list[m],
          image = imgurl_list[m],
          rating = rating_list[m]
        )

    
    products =Search.objects.all()
    


    return render(request, 'search.html', {'scrap_amz':products})
  
  return render(request, 'search.html')    



def index(request):

  productsFromDB = ScrappedProduct.objects.all()[98:102]

  return render(request, 'index.html', {'popularlist':productsFromDB})
   # return HttpResponse("this is about page")

def about(request):
   if 'element' in request.GET:
     element = request.GET.get('element')
     html_content= get_html_content(element)
     soup= BeautifulSoup(html_content.text, 'html.parser')
     titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
     ratings = soup.findAll('span', {'class':'a-icon-alt'})
     img_urls=soup.find_all('img',{'class':'s-image'})
     title_list=[]
     rating_list=[]
     imgurl_list=[]
 
 
     # appending into list 
     for img_url in img_urls:
         if 'jpg' in img_url['src']:
             imgurl_list.append(img_url['src'])
 
     for title in titles:
         title_list.append(title.text)
     for rating in ratings:
         rating_list.append(rating.text.replace(' out of 5 stars',''))
 
     Search.objects.all().delete()
 
     scrap_amz = []
     for m in range(0,13):
         dict_scrap={}
         dict_scrap['title']=title_list[m]
         dict_scrap['image']=imgurl_list[m]
         dict_scrap['rating']=rating_list[m]
         scrap_amz.append(dict_scrap)
 
         Search.objects.create(
           title = title_list[m],
           image = imgurl_list[m],
           rating = rating_list[m]
         )
 
     
     products =Search.objects.all()
     
 
 
     return render(request, 'search.html', {'scrap_amz':products})
   return render(request, "about.html")
   # return HttpResponse("this is about page")

def contact(request):
  #this is process of sending information of user in the database.
  if 'element' in request.GET:
    element = request.GET.get('element')
    html_content= get_html_content(element)
    soup= BeautifulSoup(html_content.text, 'html.parser')
    titles = soup.findAll('span', {'class':'a-size-small a-color-base a-text-normal'})
    ratings = soup.findAll('span', {'class':'a-icon-alt'})
    img_urls=soup.find_all('img',{'class':'s-image'})
    title_list=[]
    rating_list=[]
    imgurl_list=[]


    # appending into list 
    for img_url in img_urls:
        if 'jpg' in img_url['src']:
            imgurl_list.append(img_url['src'])

    for title in titles:
        title_list.append(title.text)
    for rating in ratings:
        rating_list.append(rating.text.replace(' out of 5 stars',''))

    Search.objects.all().delete()

    scrap_amz = []
    for m in range(0,13):
        dict_scrap={}
        dict_scrap['title']=title_list[m]
        dict_scrap['image']=imgurl_list[m]
        dict_scrap['rating']=rating_list[m]
        scrap_amz.append(dict_scrap)

        Search.objects.create(
          title = title_list[m],
          image = imgurl_list[m],
          rating = rating_list[m]
        )

    
    products =Search.objects.all()
    


    return render(request, 'search.html', {'scrap_amz':products})

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
  productsFromDB = ScrappedProduct.objects.all()
  return render(request, "daraz.html",{'popularlist':productsFromDB})