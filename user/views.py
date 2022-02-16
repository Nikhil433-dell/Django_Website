from email import message

from django.http import HttpResponse
from user.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
# Create your views here.

def index(request):
    request.session['name'] = 'user_details'

    try:
        if request.method=="POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

        # check if user has entered correct credentials
            user_obj = User.objects.get(email=email.lower())
            user = authenticate(username=user_obj, password=password)

            profile = Profile.objects.get(user=user_obj)
            if user is not None:
                login(request, user)
                return redirect(f"/user_details/{profile.id}")
            else:
                messages.error(request, "Wrong Password!")
                print('failed')
                return redirect("/")
    except Exception as e:
        print(e)
    return render(request, "index.html")



def sign_up(request):
    request.session['name'] = 'user_details'

    try:
        if request.method == "POST":
            username = request.POST.get('username')
            last_name = "none"
            email = request.POST.get('email')
            password = request.POST.get('pass1')
            password2 = request.POST.get('pass2')
            address = request.POST.get('address')

            if password != password2:
                messages.error(request, "Error: Passwords not matching!")
                print("Passwords not matching!")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Error: Email Taken!")
                print("Email Taken!")
            elif User.objects.filter(username=username).exists():
                messages.error(request, "Error: Username Taken!")
                print("Username Taken!")
            elif password == username:
                messages.error(request, "Password is not Strong!")
                print("Error: Password is not Strong!")
            else:
                user = User.objects.create_user(first_name=username, last_name=last_name, username=username, email=email, password=password)
                user.save()

                profile = Profile(address=address, user=user)
                profile.save()

    #              'refresh': str(refresh),
    # 'access': str(refresh.access_token),
                print("user_created")
                return redirect(f"/user_details/{profile.id}")
    except Exception as e:
        print(e)
        message.error("Account not created")

    return render(request, "sign_up.html")




def user_details(request, id):
    if "name" in request.session:

        name = request.session['name']
        user = Profile.objects.get(id=id)

        context = {"user": user, "name": name}
        return render(request, "user_details.html", context)
    else:
        return HttpResponse("Session is expired !")




def logout(request):
    try:
        logout(request)
        print(f"{request.user}__logged out")
    except Exception as e:
        print(e)
    return redirect("/")



def edit(request, id):
    user_detail = Profile.objects.get(id=id)
    username = request.POST.get('username')
    email = request.POST.get('email')
    address = request.POST.get('address')
    if request.method == "POST":
        user_detail.address = address
        user_detail.save()
        print("edited")
        return redirect(f"/user_details/{id}")
    context = {"user": user_detail}
    return render(request, "edit.html", context)



def delete(request, id):
    user = Profile.objects.get(id=id)
    user.delete()
    messages.error(request, "Account deleted!")
    return redirect("/")