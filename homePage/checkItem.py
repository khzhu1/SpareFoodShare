from userAuthentication.models import UserPersonal, User
from .models import ProductInfo, Product
import datetime

CATEGORY_LIST = ["Fresh Fruit", "Fresh Vegetable", "Meat", "Frozen Food", "Food Cupboard",
                 "Beer, Wine & Spirits", "Bakery", "Milk & Eggs", "Drinks", "Others"]

# return all the product which can shown in public
def getItemList(category):
    result = []
    products = Product.objects.all()
    # print(type(category))

    # get a list contains items which are not expired and set 'visible' and in stock
    for item in products:
        ex_boolean = checkExpire(item.product_info.product_expiryDate)
        # product expired, change status
        if item.product_info.product_checkExpired != ex_boolean:
            # print('Check!!! Update before ', item.product_info.product_checkExpired)
            info = ProductInfo.objects.get(info_id=item.product_info.info_id)
            info.product_checkExpired = ex_boolean
            info.save()
            item.product_info = info
            # print('Check !!! Update after ', item.product_info.product_checkExpired)
            item.save()

        if item.product_info.product_checkExpired and item.product_info.product_visibility and not item.product_info.product_sold:
            if item.product_category == CATEGORY_LIST[int(category or 0)-1]:
                print("item: ", item)
                print("list: ", CATEGORY_LIST[int(category or 0)-1])
                result.append(item)
    return result

def getAllItem():
    result = []
    products = Product.objects.all()

    # get a list contains items which are not expired and set 'visible' and in stock
    for item in products:
        ex_boolean = checkExpire(item.product_info.product_expiryDate)
        # product expired, change status
        if item.product_info.product_checkExpired != ex_boolean:
            # print('Check!!! Update before ', item.product_info.product_checkExpired)
            info = ProductInfo.objects.get(info_id=item.product_info.info_id)
            info.product_checkExpired = ex_boolean
            info.save()
            item.product_info = info
            # print('Check !!! Update after ', item.product_info.product_checkExpired)
            item.save()

        if item.product_info.product_checkExpired and item.product_info.product_visibility and not item.product_info.product_sold:
            result.append(item)
    return result

# return all the product which are uploaded by current user
def getMyList(request):
    result = []
    products = Product.objects.all()

    # get a list contains items which are not expired and set 'visible' and in stock
    for item in products:
        if item.product_info.user_id == str(request.user.id):
            result.append(item)
    return result


def checkInput(request):
    info = ProductInfo()
    info.user_id = request.user.id
    info.user_name = request.user.username
    info.product_name = request.POST.get('title')
    info.product_details = request.POST.get('description')
    info.product_expiryDate = request.POST.get('expire_date')
    info.product_price = request.POST.get('price')
    info.product_location = request.POST.get('postcode')

    # 0: public; 1: private.
    if request.POST.get('visibility') == "0":
        info.product_visibility = True
    else:
        info.product_visibility = False

    info.product_sold = False
    info.product_checkExpired = checkExpire(info.product_expiryDate)

    info.save()
    product = Product()
    product.product_info = info
    product.product_image = request.FILES.get("product_img")

    if request.POST.get('category') == "1":
        product.product_category = "Fresh Fruit"
    elif request.POST.get('category') == "2":
        product.product_category = "Fresh Vegetable"
    elif request.POST.get('category') == "3":
        product.product_category = "Meat"
    elif request.POST.get('category') == "4":
        product.product_category = "Frozen Food"
    elif request.POST.get('category') == "5":
        product.product_category = "Food Cupboard"
    elif request.POST.get('category') == "6":
        product.product_category = "Beer, Wine & Spirits"
    elif request.POST.get('category') == "7":
        product.product_category = "Bakery"
    elif request.POST.get('category') == "8":
        product.product_category = "Milk & Eggs"
    elif request.POST.get('category') == "9":
        product.product_category = "Drinks"
    elif request.POST.get('category') == "10":
        product.product_category = "Others"

    product.save()

    return product


def checkExpire(date_str):
    # get today's date
    now = datetime.datetime.today()
    expire_date = datetime.datetime.strptime(date_str, "%Y-%m-%d")
    # check if today is before expire date
    if expire_date >= now:
        return True
    # if not, it can't be shown to public
    else:
        return False


def showItem(product):
    item = product.product_info
    print(product.product_image)
    print(item.user_id, item.product_name, item.product_details, item.product_expiryDate,
          item.product_price, item.product_location, item.product_visibility, item.product_sold,
          item.product_checkExpired)

def searchProduct(keyword):
    result = []
    products = Product.objects.all()

    # get a list contains items which are not expired and set 'visible' and in stock
    for item in products:
        if keyword in item.product_info.product_name or keyword in item.product_info.product_details:
            result.append(item)
    return result
