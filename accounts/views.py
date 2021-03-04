from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from verify_email.email_handler import send_verification_email
from django.core.mail import EmailMessage
from realtors.models import Realtor
from django.views import View
from django.urls import reverse
from .utils import token_generator

from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site


def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        user_type = request.POST['user_type']
    
        # Check if password match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks Good
                    user = User.objects.create_user(username=username, password=password, email=email, 
                    first_name=first_name, last_name=last_name) 
                    # Login after register
                    #auth.login(request, user)
                    #messages.success('You are now loged in')
                    #return redirect('index')
                    user.is_active = False
                    user.save()
                    if user_type=='realtor':
                       realtor = Realtor.objects.create(user_id=user) 
                    # path_to_view
                    # getting domain we are on
                    # relative urlto verification
                    # encode uid
                    # token
                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs={
                        'uidb64': uidb64, 'token': token_generator.make_token(user)
                    })

                    email_subject = 'Activate your account'

                    activate_url = 'http://'+domain+link                    
                    email_body = 'Hi '+user.username + ',' + \
                        '\n Please use this link to verify your account\n' + activate_url 
                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'mnjayswal10@gmail.com',
                        [email],
                    )
                    email.send(fail_silently=False)
                    messages.success(request, 'Activate your account from mail') #messages.success(request, 'You are now registered and log in') changed this line
                    return redirect('login')

        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')

    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user_type=='realtor':
                auth.login(request, user)
                try:
                    request.user.profile
                    messages.success(request, 'You are now logged in')
                    return redirect('index')
                except:
                    messages.error(request, "You can't loin as Realtor")
                    return redirect('login')
            else:
                auth.login(request, user)
                try:
                    request.user.profile
                    messages.error(request, "You can't loin as Buyer")
                    return redirect('login')
                except:
                    messages.success(request, "You are now logged in")
                    return redirect('index')
                
                messages.success(request, 'You are now logged in')
                return redirect('dashboard')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, "You are now logged out")
        return redirect('index')

def dashboard(request):
#    if request.method == 'POST':
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('login'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('login')
        
        except Exception as ex:
            pass

        return redirect('login')
'''
class LoginView(View):
    def get(self, request):
        return render(request, 'login')'''