from asyncio.windows_events import NULL
from tkinter import CURRENT
from urllib import request
from django.contrib.auth import authenticate,login,logout
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.contrib import messages
from sec_prog import settings
from django.core.mail import EmailMessage, send_mail
from . unq_str import generate_unq
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from sharefiles.models import Group, Message
from django.contrib import auth
from django.urls import reverse

# Create your views here.
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
    
        user = authenticate(request,username=username, password=password1)

        if user is not None and user.is_active:
                auth.login(request, user)
                fname = user.first_name
                # messages.success(request, "Logged In Sucessfully!!")
                return render(request, "home1.html",{"fname":fname})
        else:
                messages.info(request, "Bad Credentials!!")
                return redirect('badreq')
    else:

        return render(request, "login1.html")


def verifyInput(username,password1):
	error = []
	if len(username) < 4:
		error.append('Username Should At Least Be 4 Character Long')
	elif len(password1) < 8:
		error.append('Password Should At Least Be 8 Character Long')
	else:
		print('OK')

	return error




def home (request):
    fname = request.POST.get("fname")
    
    if fname == None:
        return HttpResponseRedirect(reverse("signin"))

    current_user = request.user
    user_id = current_user.id
    print(user_id)
    context = {'user_id': user_id}
    return render(request, "home1.html",context)

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        error = verifyInput(username,password1)

        if len(error) != 0:
            error = error[0]
            print(error)
            return render(request, 'bad_cred.html', {'error': error})
        else:
            print("good")
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try other username.")
            return redirect('badreq')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('badreq')
        
        if len(username)>20:
            messages.info(request, "Username must be under 20 charcters!!")
            return redirect('badreq')
        
        if password1 != password2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('badreq')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('badreq')
       


        myuser = User.objects.create_user(username, email, password1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address .")
        
        # Welcome Email
        subject = "Welcome to Django Login!"
        message = "Hello " + myuser.first_name + "! \n" + "Welcome!! \nThank you for visiting my website\n. We have also sent you an confirmation email, please confirm your email address. \n\nThanking You\nmanoj"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
         # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email!"
        message2 = render_to_string('authin.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_unq.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
   
        
        

    return render(request, "register1.html")

def signout(request):
    logout(request)
    messages.success(request, "logedout user")
    return redirect("badreq")

def post_msg(request):
    return render(request, "postmsg.html")

def view_my_posts(request):
    return render(request, "pst.html")

def view_badreq(request):
    return render(request,"bad_cred.html")
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_unq.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'failed.html')



def view_group(request):
    return render(request, "groups.html")

def room(request,room):
    username = request.GET.get('username')
    group_details = Group.objects.get(name=room)
    return render(request, 'messages.html', {
        'username': username,
        'room': room,
        'group_details': group_details
    })
    return render(request, "messages.html")
#after clicking enter group
def check_group_auth(request):
    group = request.POST['group_name']
    #username = request.POST['username']
    current_user = request.user
    user_id = current_user.id
    user_name=current_user.username
    print(user_id)
    context = {'user_id': user_id}
    context2={'user_name':user_name}

    if Group.objects.filter(name=group).exists():
        return redirect('/'+group+'/?username='+user_name)
    else:
        new_group = Group.objects.create(name=group)
        new_group.save()
        return redirect('/'+group+'/?username='+user_name)



def send(request):
    message = request.POST['message']
    username = request.POST['username']
    group_id = request.POST['group_id']

    new_message = Message.objects.create(value=message, user=username, group=group_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

#f(,var)
def messagebox(request, group):
    group_details = Group.objects.get(name=group)

    messages = Message.objects.filter(group=group_details.id)
    return JsonResponse({"messages":list(messages.values())})









