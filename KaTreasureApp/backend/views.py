from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages, auth as django_auth
from KaTreasureApp.firebase_config import config
import pyrebase
import firebase_admin
from django.core.mail import send_mail
from firebase_admin import credentials
from firebase_admin import auth

#pyrebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()
authn = firebase.auth()
usermain = db.child("users").get().val()
print("Signed in: ", usermain)

#admin firebase
cred = credentials.Certificate('firebase-sdk.json')
firebase_admin.initialize_app(cred)

# Create your views here.
@login_required
def base(request):
   
    return render(request, 'base/base.html')

def home(request):
    idToken = request.session.get('uid')
    authenticated = False
    full_name = None

    if idToken:
        full_name = get_user_info(idToken)
        if full_name:
            authenticated = True

    return render(request, 'home.html', {'full_name': full_name, 'authenticated': authenticated})

def get_user_info(id_token):
    if id_token:
        a = authn.get_account_info(id_token)
        a = a['users']
        a = a[0]
        a = a['localId']

        full_name = db.child("users").child(a).child('details').child('full_name').get().val()
        return full_name
    else:
        return None

def logout(request):
    django_auth.logout(request)
    messages.success(request, "Logged out.")
    return redirect('KaTreasureApp:login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        link = auth.generate_password_reset_link(email, action_code_settings=None)
        sender = 'isoygwapo84@gmail.com'
        subject = "KaTreasure: Password Reset"

        message = f'You requested to reset your password for your KaTreasure account. Use the link below to change it. \n\nReset Link: {link}'

        recipient_list = [email]

        send_mail(subject, message, sender, recipient_list)
        messages.success(request, f'Reset link has been sent to {email}')
        return redirect('KaTreasureApp:login')
        
    return render(request, 'auth/forgot_password.html')
