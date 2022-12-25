from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Code, Blog, CustomUser
from .utility import send_email

from auditlog.models import LogEntry

from django.db import connection
import hashlib
from django.contrib.auth.hashers import make_password, check_password

# Create your views here.

def home(request):
    all_blogs = Blog.objects.all()
    blogs = all_blogs.exclude(is_private = True).order_by('-created_date')
    if request.user.is_authenticated:
        user = request.user
        context = {
            'user' : user,
            'blogs' : blogs
        }
        return render(request, 'home.html',context)
    else:
        context = {
            'blogs' : blogs,
        }
        return render(request, 'home.html',context)
    

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                user = None

            if user is not None:
                print("username already exits")
                return redirect(signup)
            else:
                new_user = User(username=username, email = email)
                new_user.set_password(password)
                new_user.save()
                
                customuser = CustomUser(username=username, password = password)
                customuser.save()
                login(request, new_user)
                return redirect('home')
        else:
            return render(request, 'signup.html')

def signin(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active == True:
                    request.session['pk'] = user.pk
                    return redirect('verify')
                else:
                    return redirect('home')

            else:
                print("Wrong Username or password")
                return redirect('login')
        else:
            return render(request, 'login.html')

def verify(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        try:
            pk = request.session.get('pk')
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            user = None
        if user is not None:
            code = Code.objects.get(user=user)
            user_code_number = code.number
            sent_user_code = f"{user.username}: {user_code_number}"

            if not request.POST:
                print(sent_user_code)
                send_email(user.email,sent_user_code)
                return render(request, 'verify.html')
            else:
                user_given_code = request.POST.get('code')
                if str(user_code_number) == user_given_code:
                    code.save()
                    login(request, user)
                    return redirect('home')
                else:
                    print("code didn't match")
                    code.save()
                    del request.session['pk']
                    request.session.modified = True
                    return redirect('login')
        else:
            print("not allowed")
            return redirect('login')
def user_logout(request):
    logout(request)
    return redirect('login')

def profile(request,pk):
    user = User.objects.get(pk=pk)
    if user == request.user:
        blogs = Blog.objects.filter(user = user).order_by('-created_date')
        context = {
            'user' : user,
            'blogs' : blogs,
        }
        return render(request, 'profile.html',context)
    else:
        blogs = Blog.objects.filter(user = user).order_by('-created_date').exclude(is_private = True)
        context = {
            'user' : user,
            'blogs' : blogs,
        }
        return render(request, 'profile.html',context)


def post_blog(request):
    if request.user.is_authenticated:
        user = request.user

        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            private = request.POST.get("private")

            if private is None:
                blog = Blog.objects.create(user = user, title=title,content=content,is_private = False)
                blog.save()
                return redirect('home')
            else:
                blog = Blog.objects.create(user = user, title=title,content=content,is_private = True)
                blog.save()
                return redirect('home')
            
        else:
            context = {
                'user' : user
            }
            return render(request, 'create_blog.html',context)
    else:
        return redirect('home')

def blog_detail(request,pk):
    blog = Blog.objects.get(pk=pk)
    if blog.is_private:
        if blog.user == request.user:
            context = {
                'blog' : blog,
            }
            return render(request, 'blog_detail.html',context)
        else:
            return redirect('home')
    else:
        context = {
            'blog' : blog,
        }
        return render(request, 'blog_detail.html',context)
        
    

def edit_blog(request,pk):
    if request.user.is_authenticated:
        user = request.user
        blog = Blog.objects.get(pk=pk)
        if(user == blog.user):
            if request.method == "POST":
                title = request.POST.get("title")
                content = request.POST.get("content")
                private = request.POST.get("private")
                if private is None:
                    blog.title = title
                    blog.content = content
                    blog.is_private = False
                    blog.save()
                    return redirect('home')
                else:
                    blog.title = title
                    blog.content = content
                    blog.is_private = True
                    blog.save()
                    return redirect('home')
            else:
                context = {
                    'blog' : blog,
                }
                return render(request, 'edit_blog.html',context)
        else:
            return redirect('home')
    else:
        return redirect('home')

def delete_blog(request,pk):
    if request.user.is_authenticated:
        user = request.user
        blog = Blog.objects.get(pk=pk)
        if(user == blog.user):
            if request.method == "POST":
                blog.delete()
                return redirect('home')
            else:
                context = {
                    'blog' : blog,
                }
                return render(request, 'delete_blog.html',context)
        else:
            return redirect('home')
    else:
        return redirect('home')



def admin(request):
    pass


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def unsecure_login(request):
    cursor = connection.cursor()
    username = request.GET.get('username')
    password = request.GET.get('password')
    # cursor.execute(" SELECT * FROM auth_user WHERE username='%s' " %(username))
    # record = cursor.fetchall()
    # if len(record) > 0:
    #     for row in record:
    #         is_matched = check_password(password,row[1])
    #         if(is_matched  == True):
    #             user = User.objects.get(username = username)
    #             login(request, user)
    #             return redirect('home')

    query = "SELECT * FROM blog_customuser WHERE username='%s' AND password='%s';" %(username,password)
    user = CustomUser.objects.raw(query)

    if user is not None:
        for u in user:
            # is_matched = check_password(password,u.password)
            # if(is_matched  == True):
            user = User.objects.get(username = u.username)
            login(request, user)
            return redirect('home')
    
    return render(request, 'unsecure_login.html')


