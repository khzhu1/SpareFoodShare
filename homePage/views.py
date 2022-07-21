from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout as logoutUser
from .checkItem import *
from django.http import JsonResponse, HttpResponse
from homePage.models import ProductInfo, Product


def homePage(request):
    products = getAllItem()

    print("Current user id: ", request.user.id)

    now_user_form = None

    # get outer model of current login user
    users = UserPersonal.objects.all()
    for u in users:
        if u.user_form == request.user:
            now_user_form = u

    return render(request, "./HomePage.html", {'item_list': products, 'filter': 0, 'now_user': now_user_form})

def homePageWithFilter(request, nid):
    print("Filter by category id: ", nid)
    products = getItemList(nid)

    now_user_form = None

    # get outer model of current login user
    users = UserPersonal.objects.all()
    for u in users:
        if u.user_form == request.user:
            now_user_form = u

    return render(request, "./HomePage.html", {'item_list': products, 'filter': nid, 'now_user': now_user_form})


def logout(request):
    logoutUser(request)
    return redirect("/")


def addItem(request):
    if request.method == 'POST':

        # check every field
        result = checkInput(request)
        if isinstance(result, Product):
            # return instance means add product successfully
            print("Add item successful!!!")
            return redirect("/")

    return render(request, "AddItem.html")


# function of bulk upload
def maddItem(request):
    if request.POST.get('action'):
        users = request.POST.get('users')
        import json
        users = json.loads(users)

        # save data into database respectively
        for user in users:
            info = ProductInfo()
            info.user_id = request.user.id
            info.user_name = request.user.username
            info.product_name = user['title']
            info.product_details = user['description']
            info.product_expiryDate = user['date']
            info.product_price = user['price']
            info.product_location = user['postcode']

            if user['visibility'] == "0":
                info.product_visibility = True
            else:
                info.product_visibility = False

            info.product_sold = False
            info.product_checkExpired = checkExpire(info.product_expiryDate)

            info.save()
            product = Product()
            product.product_info = info
            product.product_image = "product_images/"+user["product_img"]

            if user['category'] == "1":
                product.product_category = "Fresh Fruit"
            elif user['category'] == "2":
                product.product_category = "Fresh Vegetable"
            elif user['category'] == "3":
                product.product_category = "Meat"
            elif user['category'] == "4":
                product.product_category = "Frozen Food"
            elif user['category'] == "5":
                product.product_category = "Food Cupboard"
            elif user['category'] == "6":
                product.product_category = "Beer, Wine & Spirits"
            elif user['category'] == "7":
                product.product_category = "Bakery"
            elif user['category'] == "8":
                product.product_category = "Milk & Eggs"
            elif user['category'] == "9":
                product.product_category = "Drinks"
            elif user['category'] == "10":
                product.product_category = "Others"

            print("save")
            product.save()

    products = getItemList(0)
    print(products)

    print("render")
    messages.success(request, "Upload successful")
    return redirect("/")


def viewItem(request):
    # get item which is clicked by user
    product = Product.objects.get(pk=request.GET.get('product_id', None))
    user_id = request.user.id

    return render(request, "./ViewItem.html", {'product': product, 'user_id': user_id})

def myList(request):
    products = getMyList(request)
    return render(request, "./MyList.html", {'item_list': products})

def map(request):
    return render(request, "./Map.html")

def searchHomePage(request, keyword):
    # get product list by searching keyword in title and description
    products = searchProduct(keyword)
    return render(request, "./HomePage.html", {'item_list': products, 'filter': 0})

def viewMyItem(request):
    # get item which is clicked by user
    product = Product.objects.get(pk=request.GET.get('product_id', None))

    return render(request, "./ViewMyItem.html", {'product': product})

def changeVisibility(request):
    if request.POST.get('action') == 'post':
        visibility = request.POST.get('visibility', None)
        product_id = request.POST.get('product_id', None)
        product = Product.objects.get(pk=product_id)
        print(visibility)

        if visibility == 'true':
            productinfo = product.product_info
            productinfo.product_visibility = True
            productinfo.save()
            
        else:
            productinfo = product.product_info
            productinfo.product_visibility = False
            productinfo.save()
        
        response = JsonResponse({'success': 'Return something'})
        return response
