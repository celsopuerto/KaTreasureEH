from django.shortcuts import render, redirect
from django.contrib import messages
from ..firebase_config import config
import pyrebase
import firebase_admin


firebase = pyrebase.initialize_app(config)
db = firebase.database()
authn = firebase.auth()

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authn.sign_in_with_email_and_password(email, password)
            session_id = user['idToken']
            request.session['uid'] = str(session_id)
            
            uid = str(user['localId'])
            user_data = db.child("users").child(uid).child('details').child('full_name').get().val()
            print("Userdata:", user_data)
            messages.success(request, "Account Login Successfully")
            authenticated = True
            print("Login Success")
            return render(request, 'home.html', {'authenticated': authenticated, 'full_name': user_data})
        except Exception as e:
            error_message = str(e)
            if 'INVALID_EMAIL' in error_message:
                messages.error(request, "Invalid email, please try again.")
                return render(request, 'auth/login.html')
            elif 'INVALID_LOGIN_CREDENTIALS' in error_message:
                messages.error(request, "Invalid credentials, please try again.")
                return render(request, 'auth/login.html')
            else:
                messages.error(request, "Invalid input, please try again.")
                print("ERROR:", error_message)
                return render(request, 'auth/login.html')

    return render(request, 'auth/login.html')

def signup(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = authn.create_user_with_email_and_password(email, password)
            data = {"full_name": full_name, "email": email, "status":"1"}

            uid = user['localId']

            db.child('users').child(uid).child("details").set(data)
            
            messages.success(request, "Account Created Successfully")
            print("Signup Success")
            return redirect('KaTreasureApp:login')
        except Exception as e:
            error_message = str(e)
            if 'EMAIL_EXISTS' in error_message: 
                messages.error(request, "Email already exists. Please login or use a different email address.")
                return render(request, 'auth/signup.html')
            elif 'WEAK_PASSWORD' in error_message:
                messages.error(request, "Weak password.")
                return render(request, 'auth/signup.html')
            else:
                print(error_message)
                error_message = "Invalid Email Format."
                messages.error(request, error_message)
                return render(request, 'auth/signup.html')
    return render(request, 'auth/signup.html')