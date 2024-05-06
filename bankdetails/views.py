from bankdetails.encdec import generate,generate_random_xor_key,perform_xor,perform_xor_strings,encrypt_aes,encrypt_pass
from django.shortcuts import render
from bankdetails.models import Bankdetails,EncryptData
import base64


passw=''

def bankapplication(request):
    global user
    global passw
        
    try:
        if request.method=='POST':
            user=request.POST.get('name')
            gender=request.POST.get('gender')
            marriage=request.POST.get('marriage')
            Fname=request.POST.get('Fname')
            Mname=request.POST.get('Mname')
            pan=request.POST.get('pan')
            Wnet=request.POST.get('Wnet')
            number=request.POST.get('number')
            Dcc=request.POST.get('Dcc')
            city=request.POST.get('city')
            state=request.POST.get('state')
            pin=request.POST.get('pin')
            Email=request.POST.get('Email')
            passw=request.POST.get('passw')
            desg=request.POST.get('desg')
            Email1=encrypt_pass(Email)
            pan1=encrypt_pass(pan)
            number1=encrypt_pass(number)
            Fname1=encrypt_pass(Fname)
            Mname1=encrypt_pass(Mname)
            bank_details=Bankdetails(name=user,gender=gender,marriage=marriage,Fname=Fname1,Mname=Mname1,pan=pan1,Wnet=Wnet,
                             number=number1,Dcc=Dcc,city=city,state=state,pin=pin,Email=Email1,desg=desg)
            bank_details.save()



    except:
        pass


    return render(request,"applyform.html")


def carddetails(request):
    global user
    global passw
    
    
    credit_card_number = str(generate(16))
    cvv = str(generate(3))
    exp_date = "09/30"
    pin = str(generate(6))
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
    psc_salt_secrete_cvv = perform_xor(pin_salt_card, salt_secret_cvv)
    k = salt_card_number
    k2 = salt_secret_cvv


    combined = perform_xor_strings(k, passw)
    result_xor = perform_xor_strings(k2, passw)
    
    
    encrypted_data = encrypt_pass(passw)
    data={
        'cardnumber':credit_card_number,
        'exp_date':exp_date,
        'cvv':cvv,
        'secrete_pin':pin
    }
    try:
        
        encrypt_aes_data=EncryptData(user=user,cardnumber=encrypted_xor_credit_card,date_cvv=encrypted_xor_secret_cvv,
                                     key1=combined,key2=result_xor,pin=psc_salt_secrete_cvv,password=encrypted_data)
        encrypt_aes_data.save()
    except:
        pass


    return render(request,'carddetails.html',data)


