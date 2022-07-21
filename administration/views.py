from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .database import *
from django.core.mail import send_mail
from django.conf import settings
import json


def userManagement(request):
    context = {
        'userManagement': 'active'
    }

    users = getUserList()
    return render(request, 'userManagement.html', context={'content': context, 'users': users})


def user_delete(request):
    context = {
        'userManagement': 'active'
    }

    username = request.GET.get('del_username', None)
    if username:
        delUser(username)

    users = getUserList()
    return render(request, 'userManagement.html', context={'content': context, 'users': users})


def productManagement(request):
    context = {
        'productManagement': 'active'
    }

    # item_id = request.GET.get('del_item', None)

    products = getProductList()
    email_dest_list, product_list = getNoticeList()
    for p in products:
        p.product_category

    return render(request, 'productManagement.html', {'content': context, 'products': products,
                                                      'email_dest_list': email_dest_list,
                                                      'product_list': product_list})


def product_delete(request):
    context = {
        'userManagement': 'active'
    }

    item = request.GET.get('del_item', None)
    if item:
        delProduct(item)

    products = getProductList()
    return render(request, 'productManagement.html', context={'content': context, 'products': products})


def orderManagement(request):
    context = {
        'orderManagement': 'active'
    }
    order_list = getOrderList()
    return render(request, 'orderManagement.html', context={'content': context, 'order_list': order_list})

def order_delete(request):
    context = {
        'orderManagement': 'active'
    }
    nid = request.GET.get('del_order')
    print(nid)
    del_order(nid)
    order_list = getOrderList()
    return render(request, 'orderManagement.html', context={'content': context, 'order_list': order_list})


def dashboard(request):
    context = {
        'dashboard': 'active'
    }

    # chart 1
    iType, bType = getUserTypeChart()

    # chart 2
    monthList, amountList = getMonthChartWithOrder()

    # chart 3
    cList = getCategoryChart()

    # chart 4
    orderListWithCate, productListWithCate = getCategoryChartWithOrder()
    return render(request, 'dashboard.html', context={'content': context, 'iType': iType, 'bType': bType,
                                                      'cList': json.dumps(cList), 'cName': json.dumps(CATEGORY_LIST),
                                                      'orderListWithCate': json.dumps(orderListWithCate),
                                                      'productListWithCate': json.dumps(productListWithCate),
                                                      'monthList': json.dumps(monthList),
                                                      'amountList': json.dumps(amountList)})


def edit_profile(request, nid):
    if request.method == 'GET':
        user = User.objects.get(pk=nid)
        return render(request, 'profile.html', {'user': user})

    if request.method == 'POST':
        updateInfo(request, nid)

        users = getUserList()
        context = {
            'userManagement': 'active'
        }
        return render(request, 'userManagement.html', context={'content': context, 'users': users})


def edit_product(request, nid):
    if request.method == 'GET':
        item = Product.objects.get(product_id=nid)
        return render(request, 'editProduct.html', {'item': item})

    if request.method == 'POST':
        updateProduct(request, nid)

        context = {
            'userManagement': 'active'
        }

        products = getProductList()

        return render(request, 'productManagement.html', {'content': context, 'products': products})


def product_expiry_notice(request):
    email_dest_list, product_list = getNoticeList()
    print(email_dest_list)
    print(product_list)

    for i in range(len(email_dest_list)):
        title = "SpareFoodShare - " + " Your item \"" + product_list[i].product_name + "\" will be expired soon"
        msg = "Hi " + email_dest_list[i].username + ",\n\n        We kindly remind you that the item \"" + product_list[i].product_name + \
              "\" you posted on SpareFoodShare will be expired soon. \n\n\n" \
              "        The item is currently private. " \
              "Please make the item visible to everyone as soon as possible. " \
              "Once an item expires, it will be permanently removed. \n\n\n" \
              "        Check more information at http://localhost:8000/myList . \n\n\n\n\n" \
              "Wish you a happy life, \nSpareFoodShare"
        send_mail(title, msg, settings.EMAIL_HOST_USER, [email_dest_list[i].email])

    products = getProductList()
    context = {
        'userManagement': 'active'
    }

    return render(request, 'productManagement.html', {'content': context, 'products': products})