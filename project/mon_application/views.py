from itertools import chain
import random
from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import profile,post,like,followers


# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_following=followers.objects.filter(follower=request.user.username)
    user_object=User.objects.get(username=request.user.username)
    image=profile.objects.get(user=user_object)
    posts=post.objects.all()
    all_users=User.objects.all()
    user_following_all=[]
    for user in user_following:
        user_list=User.objects.get(username=user.user)
        user_following_all.append(user_list)
    
    new_suggestions_list=[x for x in list(all_users) if (x not in list(user_following_all))]
    current_user=User.objects.filter(username=request.user.username)
    final=[x for x in list(new_suggestions_list) if (x not in list(current_user))]
    random.shuffle(final)
    username_profile=[]
    username_profile_list=[]
    for users in final:
        username_profile.append(users.id)
    for ids in username_profile:
        profile_list=profile.objects.filter(id_user=ids)
        username_profile_list.append(profile_list)
    final_list=list(chain(*username_profile_list))
    return  render(request,'index.html',{'user_profile':image,'posts':posts,'final_list':final_list[:4]})

@login_required(login_url='signin')
def settings(request):
    user_profile=profile.objects.get(user=request.user)
    if request.method=="POST":
        
        
        if request.FILES.get('image')==None:
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        else:
            image=request.FILES.get('image')
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
        return redirect('settings')
            
    return render(request,'setting.html',{'user_profile':user_profile})
    

def signin(request):
    if request.method=="POST":
        username=request.POST["username"]
        password=request.POST["password"]
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,'Credentials Invalid') 
            return redirect('signin')
    else:
      return render(request,'signin.html')

def signup(request):
    
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username taken')
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                
                #cree un neveau profile
                user_model=User.objects.get(username=username)
                new_profile=profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect("settings")
        else:
             messages.info(request,'Password not matching')
             return redirect('signup')   
    else:
        return render(request,'signup.html')
    

def upload(request):
    if request.method=="POST":
       user=request.user.username
       image=request.FILES.get('image_upload')
       caption=request.POST["caption"] 
       post_create=post.objects.create(user=user,image=image,caption=caption)
       post_create.save()
       return redirect('/')
    else:
        return redirect('/')
    
@login_required(login_url='signin')  
def logout(request):
    return redirect('signin')

 
def search(request):
    user_object=User.objects.get(username=request.user.username)
    user_profile=profile.objects.get(user=user_object)
    if request.method == "POST":
        username=request.POST['username']
        username_object=User.objects.filter(username__icontains=username)
        username_profile=[]
        username_profile_list=[]
        for users in username_object:
            username_profile.append(users.id)
        for ids in username_profile:
            profile_lists=profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
            
        username_profile_list=list(chain(*username_profile_list))
    return render(request,"search.html",{'user_profile':user_profile, 'username_profile_list':username_profile_list})

def profi(request,pk):
    user_object=User.objects.get(username=pk)
    user_profile=profile.objects.get(user=user_object)
    user_post=post.objects.filter(user=pk)
    combien=len(user_post)
    follower=request.user.username
    user=pk
    if followers.objects.filter(follower=follower,user=user).first():
       text='Unfollow'
    else:
        text="Follow"
        
    user_followers=followers.objects.filter(user=pk)
    nombre=len(user_followers)
    user_foll=followers.objects.filter(follower=pk)
    nombre2=len(user_foll)
    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_post':user_post,
        'combien':combien,
        'text':text,
        'nombre':nombre,
        'nombre2':nombre2,
    }
    return render(request,"profile.html",context)


def follow(request):
    if request.method == "POST":
       follower=request.POST["follower"]
       user=request.POST["user"]
       
       if followers.objects.filter(follower=follower,user=user):
           delete_follower=followers.objects.get(follower=follower,user=user)
           delete_follower.delete()
           return redirect('/profi/'+user)
       else:
           new=followers.objects.create(follower=follower,user=user)
           new.save()
           return redirect('/profi/'+user)
    else:
        return redirect("/")
    


def likes_post(request):
    username=request.user.username
    post_id=request.GET.get('post_id')
    posts=post.objects.get(id=post_id)
    like_filter=like.objects.filter(post_id=post_id,username=username).first()
    if like_filter==None:
        new_like=like.objects.create(post_id=post_id,username=username)
        new_like.save()
        posts.no_of_likes=posts.no_of_likes+1
        posts.save()
        return redirect('/')
    else:
        like_filter.delete()
        posts.no_of_likes=posts.no_of_likes-1
        posts.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'no_of_likes': post.no_of_likes})

    return redirect('/')