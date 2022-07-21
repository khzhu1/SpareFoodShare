from homePage.models import Product, ProductInfo
from userAuthentication.models import User, UserPersonal
from payment.models import OrderItem, Order
import datetime

CATEGORY_LIST = ["Fresh Fruit", "Fresh Vegetable", "Meat", "Frozen Food", "Food Cupboard",
                 "Beer, Wine & Spirits", "Bakery", "Milk & Eggs", "Drinks", "Others"]

def getProductList():
    product_list = Product.objects.all()
    # for p in product_list:
    #     print(p.product_info.product_name)

    return product_list


def getUserList():
    # user_list = User.objects.all()
    user_list = UserPersonal.objects.all()

    return user_list


def delUser(del_username):
    user = User.objects.get(username=del_username)

    products = Product.objects.all()
    for item in products:
        if item.product_info.user_id == str(user.id):
            item.delete()

    infos = ProductInfo.objects.all()

    for info in infos:
        if info.user_id == str(user.id):
            print('Delete item: ', info.product_name)
            info.delete()

    print('Delete user: ', user)
    user.delete()


def delProduct(item):
    p = Product.objects.get(pk=item)
    print('Deleting item: ', p.product_info.product_name)
    p.product_info.delete()

    p.delete()

def del_order(nid):
    print('Deleting order: ', nid)
    order = Order.objects.get(order_id=nid)
    orderItem = OrderItem.objects.get(order=order)
    order.delete()
    orderItem.delete()


def updateInfo(request, nid):
    user = User.objects.get(pk=nid)
    print('Updating user: ', user)
    user.first_name = request.POST.get('first_name')
    user.last_name = request.POST.get('last_name')
    user.email = request.POST.get('email')
    user.save()


def updateProduct(request, nid):
    item = Product.objects.get(product_id=nid)
    info = ProductInfo.objects.get(info_id=item.product_info.info_id)
    print("Updating product: ", info.product_name)

    info.product_name = request.POST.get('name')
    info.product_details = request.POST.get('details')
    info.product_expiryDate = request.POST.get('date')
    info.product_price = request.POST.get('price')
    info.product_location = request.POST.get('location')

    info.product_checkExpired = checkExpire(info.product_expiryDate)
    info.save()

    item.product_info = info
    item.save()

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

def getNoticeList():
    dest_list = []
    content_list = []

    # get today's date
    now = datetime.datetime.today()
    product_list = getProductList()
    for item in product_list:
        # for each item which is not expired, check the rest time
        if item.product_info.product_checkExpired:
            expire_date = datetime.datetime.strptime(item.product_info.product_expiryDate, "%Y-%m-%d")
            if (expire_date - now).days <= 3:
                print(item.product_info.product_name, " will be expired soon. ")
                dest_list.append(User.objects.get(id=item.product_info.user_id))
                content_list.append(item.product_info)

    return dest_list, content_list

def getOrderList():
    orders = OrderItem.objects.all()

    return orders

def getUserTypeChart():
    i_users = len(UserPersonal.objects.filter(user_type='Individual'))
    b_users = len(UserPersonal.objects.filter(user_type='Business'))

    return i_users, b_users

def getCategoryChart():
    result = []
    for c in CATEGORY_LIST:
        result.append(len(Product.objects.filter(product_category=c)))

    return result

def getCategoryChartWithOrder():
    result = []
    result_product = []
    for c in CATEGORY_LIST:
        count = 0
        count_pro = 0
        # get product list of category c
        pro_list = Product.objects.filter(product_category=c)
        for pro in pro_list:
            # count uploaded product of this category
            count_pro += 1
            # count completed order of this category
            if pro.product_info.product_sold:
                count += 1

        result.append(count)
        result_product.append(count_pro)

    print('uploaded product of this category', result)
    print('completed order of this category', result_product)

    return result, result_product

def getMonthChartWithOrder():
    result = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    amount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    order_list = OrderItem.objects.all()
    for order in order_list:
        month = int(order.order.created.month)
        price = float(order.product.product_info.product_price)
        result[month-1] += 1
        amount[month-1] += price

    return result, amount
