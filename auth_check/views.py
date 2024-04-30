from django.http import HttpResponseRedirect
from django.shortcuts import render
from .hash import hashing, verifying
from expense_crud.models import User

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()
        if (not user) or (not verifying(user.password, password)):
            return render(request, 'login.html', {'message': 'Sai tên đăng nhập hoặc mật khẩu', 'username': username})
        response = HttpResponseRedirect('/')
        response.set_cookie('cookie', user.cookie)
        return response
    elif request.method == 'GET':
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        # check if username exists
        if User.objects.filter(username=username):
            return render(request, 'register.html', {
                'message': 'Tài khoản đã tồn tại', 
                'username': username, 
                'full_name': full_name
            })
        if len(password) < 6:
            return render(request, 'register.html', {
                'message': 'Mật khẩu phải lớn hơn 6 ký tự', 
                'username': username, 
                'full_name': full_name
            })
        cookie = hashing(username)
        user = User(username=username, password=hashing(password), full_name=full_name, cookie = cookie)
        user.save()
        response = HttpResponseRedirect('/')
        response.set_cookie('cookie', cookie)
        return response

    elif request.method == 'GET':
        return render(request, 'register.html')

def logout(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('cookie')
    return response
