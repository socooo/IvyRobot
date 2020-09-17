# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from account.forms import LoginForm
from account.forms import RegistrationForm, UserProfileForm

from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserInfo,UserInfo1
from django.contrib.auth.models import User

from django.http import HttpResponseRedirect
from .forms import UserProfileForm, UserInfoForm, UserForm, UserInfo1Form


# Create your views here.


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            
            if user:
                login(request, user)
                return HttpResponse("Welcome. you have been authorized")
            else:
                return HttpResponse("Sorry, user or password is incorrect")
        else:
            return HttpResponse("Invalid login")
        
    if request.method == "GET":
        login_form = LoginForm()
        return render(request, "account/login.html", {"form":login_form})

def user_logout(request):
    if request.method == "GET" or request.method == "POST":
        from django.contrib.auth import views as auth_views
        request.session['gs_is_gs_menu_set'] = 'False'
        request.session['gs_auth_role_mas_dict_list'] = None
        request.session['gs_auth_role_mas_dict_list_lvl3'] = None

        auth_views.logout(request)
        return render(request, "account/logout.html")

    
def reigster(request):  #init password= qwertasdfg
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        userprofile_form = UserProfileForm(request.POST)
        
        if user_form.is_valid():
            # print(user_form.cleaned_data['username'])
            # print(user_form.cleaned_data['email'])
            print(user_form.cleaned_data['password'])
            print(user_form.cleaned_data['password2'])
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            new_profile = userprofile_form.save(commit=False)
            new_profile.user = new_user
            new_profile.save()
            
            UserInfo.objects.create(user=new_user)
            return HttpResponse("successfully")
        else:
            return HttpResponse("<h1>Sorry, you cannot register</h1>")

    if request.method == "GET":
        user_form = RegistrationForm()
        userprofile_form = UserProfileForm()
        return render(request, "account/register.html", {"form":user_form, "profile":userprofile_form})
        # return HttpResponse("111")

        
@login_required(login_url='/account/login/')
def myself(request):
    user1 = User.objects.get(username=request.user.username)
    userprofile = UserProfile.objects.get(user=request.user)
    userinfo=UserInfo.objects.get(user=request.user)
    
    print(user1.username)
    print(userinfo.school)
    print(userinfo.photo)
    
    return render(request, "account/myself.html", {"user":user1,"userprofile":userprofile,"userinfo":userinfo})

@login_required(login_url='/account/login/')
def myself_edit(request):
    
    print("--1")
    user=User.objects.get(username=request.user.username)
    userprofile=UserProfile.objects.get(user=request.user)
    userinfo=UserInfo.objects.get(user=request.user)
    
    print("--2")
    
    if request.method=="POST":
        print("--3")
        user_form=UserForm(request.POST)
        userprofile_form=UserProfileForm(request.POST)
        userinfo_form=UserInfoForm(request.POST)

        if user_form.is_valid() * userprofile_form.is_valid() * userinfo_form.is_valid():
            user_cd=user_form.cleaned_data
            userprofile_cd=userprofile_form.cleaned_data
            userinfo_cd=userinfo_form.cleaned_data
            
            print("email", user_cd["email"])
            user.email=user_cd["email"]
            
            print("birth", userprofile_cd["birth"])
            userprofile.birth=userprofile_cd['birth']
            userprofile.phone=userprofile_cd['phone']

            userinfo.school=userinfo_cd['school']
            userinfo.company=userinfo_cd['company']
            userinfo.profession=userinfo_cd['profession']
            userinfo.address=userinfo_cd['address']
            userinfo.aboutme=userinfo_cd['aboutme']

                 
            user.save()
            userprofile.save()
            userinfo.save()
            
        return HttpResponseRedirect('/account/my-information/')
    else:
        user_form=UserForm(instance=request.user)
        userprofile_form=UserProfileForm(initial=
            {
                "birth":userprofile.birth,
                "phone":userprofile.phone
            })
        userinfo_form=UserInfoForm(initial=
            {
                "school":userinfo.school,
                "profession":userinfo.profession,
                "company":userinfo.company,
                "address":userinfo.address,
                "aboutme":userinfo.aboutme,
                "school":userinfo.school
            })
        return render(request,"account/myself_edit.html",
            {
                "user_form":user_form,
                "userprofile_form":userprofile_form,
                "userinfo_form":userinfo_form
            })
        
@login_required(login_url='/account/login/')       
def my_image(request):
    if request.method =='POST':
        img=request.POST['img']
        userinfo=UserInfo.objects.get(user=request.user.id)
        userinfo.photo=img
        userinfo.save()
        return HttpResponse("1")
    else:
        return render(request,"account/imagecrop.html")