import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from homePage.models import ProductInfo, Product
from django.views.decorators.csrf import csrf_exempt
from django.http.response import HttpResponse
import json
from django.http.response import JsonResponse
from .models import Order,OrderItem
from django.contrib.auth.decorators import login_required
import os

# Stripe secret key
stripe.api_key = settings.STRIPE_SECRET_KEY

# order page view
@login_required
def order(request):
    orders = Order.objects.filter(user_id= request.user.id)
    ids = orders.values('id')
    order_items = OrderItem.objects.filter(order_id__in=ids)
    
    return render(request, 'order.html', {'orders': order_items})

# only redirect to sucess page if payment is successful
@login_required
def success(request):
    return render(request, 'success.html')

# due to the minimum amount set in Stripe, we need to set a minimum amount
minimum_price = 3000
@login_required
def CreatePayment(request, id):
    product = Product.objects.get(product_id=id)
    # create a payment intent to stipe to get the client secret
    intent = stripe.PaymentIntent.create(
        amount=int(float(product.product_info.product_price) * 100) + minimum_price,
        currency='gbp',
        metadata={'userid': request.user.id},

    )

    return render(request, 'home.html', {'client_secret': intent.client_secret, 'product': product,
                                         'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY})

# Refund view
def Refund(request):
    if request.POST.get('action') == 'post':
        order_key = request.POST.get('order_key')
        str_i = order_key.find('_secret')
        # get the order id from the payment secret
        # (in the format of orderid_..._secret...)
        intent = order_key[:str_i]
        stripe.Refund.create(
            payment_intent= intent,
        )
        order = Order.objects.get(order_key=order_key)
        order_id = order.pk
        order_items = OrderItem.objects.filter(order_id=order_id)
        for item in order_items:
            product = Product.objects.get(product_id=item.product_id)
            info = product.product_info
            info.product_sold = False
            info.save()
        order.delete()
        response = JsonResponse({'success': 'Return something'})
        return response
    return HttpResponse(status=400)

# stripe webhook to check if payment is successful
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
            json.loads(payload), stripe.api_key
        )
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        # payment_confirmation(event.data.object.client_secret)
        print("success")

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def add(request):
    if request.POST.get('action') == 'post':

        order_key = request.POST.get('order_key')
        price = request.POST.get('price')
        # user_id = request.user.id
        user_id = request.POST.get('user_id')
        pid = request.POST.get('pid')

        product = Product.objects.get(product_id= pid)
        seller = product.product_info.user_id
        if (seller == request.user.id):
            print("You can't buy your own product")
            return redirect('/')
        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            # if order doesn't exist, create new order
            order = Order.objects.create(user_id=user_id, total_paid=price,  order_key=order_key)
            order_id = order.pk
            OrderItem.objects.create(order_id=order_id, price=price, product_id= pid)
            # update the product_sold field to True in the productinfo table 
            info = product.product_info
            info.product_sold = True
            info.save()

        response = JsonResponse({'success': 'Return something'})
        return response