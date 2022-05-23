from django.shortcuts import render
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from testapp.models import Products

from django.core.mail import send_mail,send_mass_mail
#authorize razorPay  client with API Keys
razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))

def homepage(request):
    price = request.GET['price']
    number = request.GET['phone']
    email = request.user.email


    currency = "INR"
    amount = int(price)*100

    #create a razorpay order(order)
    razorpay_order = razorpay_client.order.create(dict(amount=amount,currency=currency,payment_capture='0'))
    
    #order id of newly created order(ex id= order_JYNeWn93UF8Ry2)
    razorpay_order_id = razorpay_order['id']
    callback_url = "paymenthandler/"

    #passing data to front end
    context = {}
    context["razorpay_order_id"] = razorpay_order_id
    context["razorpay_merchant_key"] = settings.RAZOR_KEY_ID
    context["razorpay_amount"] = amount
    context["callback_url"] = callback_url
    context["number"] = number
    context["currency"] = currency
    context["number"] = number
    context["email"] = email
    request.session[' razorpay_order_id'] = razorpay_order_id
    request.session['email'] = email
    request.session['amount'] = amount
    return render(request, 'payment/index.html',context=context)
    

@csrf_exempt
def paymenthandler(request):
    email = request.session.get('email')
    price = request.session.get('amount')
    order_id = request.session.get("razorpay_order_id")
    price_int = int(price)/100
    price = "Rs."+str(price_int)
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'payment/paymentsuccess.html')
                except:
                   subject = "Pasha Shopping Application"
                   message1 = '''Welcome to Pasha Shopping Application,\nWe value our customers more than anything,and your satisfaction is what we aim for! Welcome to you!\n\nunfortunately transaction failed.Please try after some time\n \nThank you for visiting us..........!\n
                                 \n\n\nThanks and Regards\n--------------------------\nPasha Shopping Application Team'''
                   message2 = "Order id is:{}\nPrice is:{}".format(order_id, price)
                   from_email = "pashasoftsol@gmail.com"
                   recipient_list = [email, ]
                   datatuple = ((subject, message1, from_email, recipient_list),(subject, message2, from_email, recipient_list))
                   #send_mail(subject, message, from_email, recipient_list)
                   send_mass_mail(datatuple)
                    # if there is an error while capturing payment.
                   return render(request, 'payment/paymentfail.html')
            else:
                subject = "Pasha Shopping Application"
                message1 = '''Welcome to Pasha Shopping Application,\nWe value our customers more than anything,and your satisfaction is what we aim for! Welcome to you!\n\nunfortunately transaction failed.Please try after some time\n \nThank you for visiting us..........!\n
                                 \n\n\nThanks and Regards\n--------------------------\nPasha Shopping Application Team'''
                message2 = "Order id is:{}\nPrice is:{}".format(order_id,price)
                from_email = "pashasoftsol@gmail.com"
                recipient_list = [email, ]
                datatuple = ((subject, message1, from_email, recipient_list),(subject, message2, from_email, recipient_list))
                #send_mail(subject, message, from_email, recipient_list)
                send_mass_mail(datatuple)
                # if signature verification fails.
                return render(request, 'payment/paymentfail.html')
        except:
            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
       # if other than POST request is made.
        return HttpResponseBadRequest()
