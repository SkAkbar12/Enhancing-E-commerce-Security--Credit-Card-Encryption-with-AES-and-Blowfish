from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from shoppingapp.otpgenerator import generate_pin
from shoppingapp.models import registerdetails,Image,Addtocart,savecarddetails
from shoppingapp.pinaunthenticator import Data,otpaunthtnticate
from shoppingapp.bankverify import verify
from bankdetails.encdec import encrypt_pass
from bankdetails.decdata import decrypt_pass
from bankdetails.decdata import bankdata
from django.core.mail import send_mail
from bankdetails.encdec import generate,generate_random_xor_key,perform_xor,perform_xor_strings,encrypt_aes
import time

# Create your views here.
def home(request):
    name = request.GET.get('data')
    email=request.GET.get('email')
  
    user_data={
        'name':name,
        'email_id':email
    }
    data=Image.objects.all()
    if request.method=='GET':
        str=request.GET.get('search')
        if str!=None:
            data=Image.objects.filter(name__icontains=str)

    img_data={
        'imgdata':data
    }
    context = {**user_data, **img_data}
    return render(request,'productlink.html',context)
def register(request):
    
    if request.method=='POST':
        username=request.POST.get('user')
        request.session['username']=username
        email=request.POST.get('email')
        password=request.POST.get('pass')
        encrypted_data=encrypt_pass(password)
        
        print("original data",password)
        try:
            # Attempt to retrieve a user with the provided email
            registerdetails.objects.get(email=email)
            return HttpResponse('User with this email already exists')
        except registerdetails.DoesNotExist:
            # No existing user found, proceed with registration
            data = registerdetails(username=username, email=email, password=encrypted_data)
            data.save()
            
    return render(request,'sregister.html')
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        password_input = request.POST.get('pass')
        print(password_input)

        try:
            # Retrieve a single user with the specified email
            user = registerdetails.objects.get(email=email)
            
            decrypted_db_password = decrypt_pass(user.password).decode('utf-8')
            print(decrypted_db_password)
            print("decrypt data",decrypted_db_password)
                # Compare decrypted password with user input
            encrypted_string = decrypted_db_password
            if encrypted_string == password_input:
                request.session['encrypted_string']= password_input
                url = reverse('home') + f'?data={user.username}&email={user.email}'
                    
                return redirect(url)
                    
            elif decrypted_db_password!=password_input:
                
                return HttpResponse("Incorrect password")
            else:
                return HttpResponse("User with this email does not exist")

            # If the loop completes without returning, no matching user was found
               

        except registerdetails.DoesNotExist:
            return HttpResponse("User with this email does not exist")

    return render(request, 'slogin.html')

def logout_user(request):
   
    return redirect('home')


def product_details(request,name,user,email):

    imgname=Image.objects.get(name=name)
    imgdata=imgname.newimg
    user_data={
        'name':user,
        'email_id':email,
        'imgname':name,
        'imgfile':imgdata
    }
   
    return render(request,'productdetails.html',user_data)

def cartitems(request,email,name,image):
    request.session['email'] = email
    
    
    savedata=Addtocart(email=email,productname=name,image=image)
    savedata.save()
    alldata=Addtocart.objects.filter(email=email)
    user=registerdetails.objects.get(email=email)
    data=user.username
    context={
        'alldata':alldata,
        'email':email,
        'user':data
    }
    
  

    return render(request,'cart.html',context)

def gateway(request,email,name,image):
    try:
        
        url = reverse('Scarddetails') + f'?email={email}&name={name}&image={image}'
        return redirect(url)
          
    except:
        pass
    return render(request,'payment.html')


def Scarddetails(request):
    email=request.GET.get('email')
    name=request.GET.get('name')
    image=request.GET.get('image')
    request.session['name'] = name
    request.session['image'] = image
    context={
        'email':email,
        'name':name,
        'image':image
    }
   
    if request.method=='POST':
        data=request.POST.get('paymentMethod')
        try:
            if data=='Credit or debit card':
                
                return redirect('fullcarddetails')
            else:
                return HttpResponse('Payment option currently not available')
        except:
            pass
    return render(request,'payment.html',context)

   
def fullcarddetails(request):
  
    if request.method == 'POST':
        cardnumber = request.POST.get('cardnumbers')
        date = request.POST.get('expdates')
        cvv = request.POST.get('cvvs')
       
        # Store card details in session
        request.session['cardnumber'] = cardnumber
        request.session['date'] = date
        request.session['cvv'] = cvv
    
        # Call bankdata function to check details
        bankdetails = bankdata(cardnumber, date, cvv)
        if bankdetails:
            return redirect('paymentForm')
        else:
            return HttpResponse('Data not found')

    return render(request, 'gateway.html')
import time

def paymentForm(request):
    pin = generate_pin()
    print(pin)
    request.session['pin'] = pin
    request.session['pin_timestamp'] = time.time()  # Update pin_timestamp
    email = request.session.get('email', '')  # Get email from session or provide a default value

    subject = "One-Factor Authentication"
    message = f"One-time password: {pin}. Don't share this passcode with anyone"
    from_email = "ashwalshaik20@gmail.com"  # Replace with your Gmail email

    try:
        send_mail(subject, message, from_email, [email], fail_silently=False)
        return render(request, 'otp.html')
    except Exception as e:
        # Handle any exceptions or log the error
        print(f"Error sending email: {e}")

    return render(request, 'otp.html')


def verifypin(request):
    if request.method=='POST':
        p1=request.POST.get('p1')
        p2=request.POST.get('p2')
        p3=request.POST.get('p3')
        p4=request.POST.get('p4')
        p5=request.POST.get('p5')
        p6=request.POST.get('p6')
        pin = request.session.get('pin', '')
        pin_timestamp = request.session.get('pin_timestamp', 0)  # Get stored timestamp
        
        # Check if more than 90 seconds (1.5 minutes) have passed since the pin was generated
        if time.time() - pin_timestamp > 90:
            return HttpResponse('OTP Verification time limit exceeded. Please try again.')

        else:
            authenticate=otpaunthtnticate(p1,p2,p3,p4,p5,p6,pin)
            print(authenticate)
            if authenticate==True:
                return redirect('authotp')
            else:
                return HttpResponse('You have entered wrong otp,try again')

    return render(request,'otp.html')
def autheotp(request):
    
    if request.method=='POST':
        p1=request.POST.get('p1')
        p2=request.POST.get('p2')
        p3=request.POST.get('p3')
        p4=request.POST.get('p4')
        p5=request.POST.get('p5')
        p6=request.POST.get('p6')
        l=[p1,p2,p3,p4,p5,p6]
        print(f"list:{l}")
        
        data=Data()
      
        status=data.pinaunthenticate(l)
        email=request.session.get('email','')
        status1=savecarddetails.objects.filter(email=email).exists()

        if status:
            ll = list("".join([p1, p2, p3, p4, p5, p6]))

            credit_card_number = request.session.get('cardnumber','')
            cvv = request.session.get('cvv','')
            exp_date = request.session.get('date','')  # Corrected 'data' to 'date'
            pin = "".join(ll)

            salt_card_number = generate_random_xor_key(len(credit_card_number))
            salt_secret_cvv = generate_random_xor_key(len(exp_date + cvv))
    
    # XOR-based Tokenization with random keys
            tokenized_xor_credit_card = perform_xor(credit_card_number, salt_card_number)
            tokenized_xor_secret_cvv = perform_xor(exp_date + ',' + cvv, salt_secret_cvv)

    # AES Encryption for XOR tokenized data
            encrypted_xor_credit_card = encrypt_aes(pin, tokenized_xor_credit_card, salt_card_number)
            encrypted_xor_secret_cvv = encrypt_aes(pin, tokenized_xor_secret_cvv, salt_secret_cvv)

    # Perform XOR encryption
            pin_salt_card = perform_xor(pin, salt_card_number)
            psc_salt_secret_cvv = perform_xor(pin_salt_card, salt_secret_cvv)
            k = salt_card_number
            k2 = salt_secret_cvv
            passw=request.session.get('encrypted_string','')

            combined = perform_xor_strings(k, passw)
            result_xor = perform_xor_strings(k2, passw)

            encrypted_data = encrypt_pass(passw)
            email=request.session.get('email','')
            if status1==False:
                data=savecarddetails(email=email,cardnumber=encrypted_xor_credit_card,date_cvv=encrypted_xor_secret_cvv,
                                     key1=combined,key2=result_xor,pin=psc_salt_secret_cvv)
          
                data.save()
        

            return redirect('success')
        else:
            return redirect('fullcarddetails')
      
    return render(request,'verifypin.html')

def success(request):
    
 
    return render(request,'ordersucces.html')
