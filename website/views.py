import ast
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from .process import *
from django.contrib import messages

# Create your views here.



def ajaxs(request):
    req_method = request.method

    def add_to_cart(user_cart, product, quantity, color):
        item = Cart_item.objects.filter(cart=user_cart, product=product, color=color)
        if item.exists():
            item = item[0]
            item.count = int(item.count) + int(quantity)
            item.save()
                
        else:
            new_cart_item = Cart_item()
            new_cart_item.cart = user_cart
            new_cart_item.product = product
            new_cart_item.count = quantity
            new_cart_item.color = color
            new_cart_item.save()

    if req_method == "GET" and request.GET['action'] == 'ajax_search':
        req = request.GET
        query = req.get('query')

        products = Product.objects.filter(title__contains=query).order_by('sell_count')[:6]


        json_response = {"suggestions": []}

        for product in products:

            json_response["suggestions"].append({
                "value": f"{product.title}",
                "permalink": f"/product/{product.id}",
                "price": f"{product.price} تومان",
                "thumbnail": f'<img width="300" height=300 src={product.main_image.url} class=attachment-dfscommerce_thumbnail size-dfscommerce_thumbnail alt= decoding=async srcset={product.main_image.url} 300w, {product.main_image.url} 150w, {product.main_image.url} 600w, {product.main_image.url} 1024w, {product.main_image.url} 768w, {product.main_image.url} 1200w sizes=(max-width: 300px) 100vw, 300px />',
            },)

        return JsonResponse(json_response)

    elif req_method == "POST":
        req = request.POST
        user_ = request.user
        try:
            action = req['action']
        except:
            data = ast.literal_eval(request.body.decode('utf-8'))
            action = data['action'] 
            comment_id = data['comment_id']
            comment = Comments.objects.get(id=comment_id)
            if user_.is_authenticated:
                try:
                    like = Comments_likes.objects.get(comment=comment, user=user_)  
                except:
                    like = Comments_likes.objects.create(comment=comment, user=user_)
                else:
                    like.delete()

                res = {"success":True}
        else:
        
            if action == 'Get_data':
                if user_.is_authenticated:
                    user_cart = Cart.objects.filter(user=user_, status='Not payed')
                    if not user_cart.exists():
                        user_cart = Cart.objects.create(user=user_, session_key=request.session.session_key, status='Not payed')
                    user_cart = user_cart[0]
                    user_cart.session_key = request.session.session_key
                    user_cart.save()
                    res = get_detials(user_cart, user=user_)
                else:
                    user_cart = Cart.objects.filter(status='Not payed', session_key=request.session.session_key)
                    if not user_cart.exists():
                        user_cart = Cart.objects.create(user=None, session_key=request.session.session_key)
                    else:
                        user_cart = user_cart[0]
                        
                    res = get_detials(user_cart, session_key=request.session.session_key)
                    
            
            elif action == 'login' or action == 'loginpage':
                phone_number = req['mobileNo']
                password = req['password']
                user = authenticate(request, phone_number=phone_number, password=password)
                if user is not None:
                    login(request, user)
                    res = {"code":1, 'message':"خوش آمدید"}

                else:
                    if action == 'login':
                        res = {"code":-11, 'message':"شماره تلفن یا رمز نامعتبر است",}
                    else:
                        messages.add_message(request, messages.ERROR, "شماره تلفن یا رمز نامعتبر است")

                
            
                
            elif action == 'ajax_add_to_cart':

                try:
                    product = Product.objects.get(id=req['add-to-cart'])
                except:
                    product = Product.objects.get(id=req['product_id'])
                    
                quantity = req['quantity']
                
                try:
                    color_id = req['color']
                except:
                    color = product.colors.all()[0]
                    color_id = color.id
                else:
                    color = Color.objects.get(id=color_id)
                
                

                if user_.is_authenticated:
                    user_cart = Cart.objects.get(user=user_, status='Not payed')
                    add_to_cart(user_cart, product, quantity, color)
                    res = get_detials(cart=user_cart, user=user_, add_=True) 


                else:
                    user_cart = Cart.objects.filter(
                        user=None, status='Not payed', session_key=request.session.session_key)
                    
                    if not user_cart.exists():
                        user_cart = Cart.objects.create(user=None, session_key=request.session.session_key)
                    
                    else:
                        user_cart = user_cart[0]
                        
                    add_to_cart(user_cart, product, quantity, color)
                
                    res = get_detials(cart=user_cart, session_key=request.session.session_key, add_=True) 

            elif action == 'new_wish_item':
                product_id = req['product_id']
                if user_.is_authenticated:
                    wishlist = Wishlists.objects.filter(user=user_)
                else:
                    wishlist = Wishlists.objects.filter(session_key=request.session.session_key)

                product_liked = get_object_or_404(Product, id=product_id)
                wish_item = Wishlists_items.objects.filter(wishlist=wishlist[0], product=product_liked)
                if wish_item.exists():
                    res = {'test':'alredy fucking exites'}

                else:
                    new_wish_item = Wishlists_items.objects.create(wishlist=wishlist[0], product=product_liked)
                    res = {'test':'Ok'}

        
            elif action == 'get_citys':
                state_id = request.POST['state_id']
                
                return HttpResponse(get_citys(state_id))

            elif action == 'update_order_review':
                res = {
                "result": "success",
                "messages": "",
                "reload": False,
                "fragments": {
                    '':''
                }}
                    
    
    return JsonResponse(res)


def account_view(request):
    if request.method == "POST":
        req = request.POST
        if req['action'] == 'register':
            name = req['name']
            phone_number = req['phone_number']
            password1 = req['password1']
            password2 = req['password2']
            
            if (password1 == password2) and chack_phone(phone_number) and name != ' ' and password_checker(password1):
                try:
                    user = User.objects.create_user(name=name, phone_number=phone_number, password=password1, last_session_key=request.session.session_key) 
                    login(request, user)
                except Exception as e:
                    print(e)
                    messages.add_message(request, messages.ERROR, "این شماره قبلا در سایت ثبت شده است")
                    return redirect('/my-account/')
                else:
                    return redirect('/')

            elif password1 != password2:
                messages.add_message(request, messages.ERROR, "رمز های عبور مطابقت ندارند !")
                return redirect('/my-account/')
       
            elif not password_checker(password1):
                messages.add_message(request, messages.ERROR, "رمز عبور ضعیف است")
                return redirect('/my-account/')
       
            else:
                messages.add_message(request, messages.ERROR, "خطا لطفا فیلد ها را با مقادیر معتبر پر کنید")
                return redirect('/my-account/')
        
    else:
        user = request.user
        if user.is_authenticated:
            carts = Cart.objects.filter(user=user).order_by('id')
            cart_items = Cart_item.objects.filter(cart=carts[0])
            total_price = 0
    
            for item in cart_items:
                e_price = item.product.price
                quantity = item.count
                total_price += e_price*quantity
                
            if total_price != 0:
                return render(request, 'account.html', {'carts':carts, 'total_price':total_price})
            else:
                return render(request, 'account.html', {'carts':[]})

                
        else:
            return render(request, 'account.html')
    


def index_view(request):

    return render(request, 'index.html')


def serach_view(request, serach_text=None):
    print(serach_text)
    return render(request, 'serach.html', {})


def shop_view(request):

    filters = request.GET

    if len(filters) != 0:
        if filters.get('min_price') or filters.get('max_price'):
            if filters.get('min_price') and not filters.get('max_price'):
                products = Product.objects.filter(
                    price__gte=filters.get('min_price'))
            elif not filters.get('min_price') and filters.get('max_price'):
                products = Product.objects.filter(
                    price__lte=filters.get('max_price'))
            else:
                products = Product.objects.filter(price__gte=filters.get(
                    'min_price'), price__lte=filters.get('max_price'))

        elif filters.get('orderby'):
            filters_list = {'popularity': 'sell_count', 'rating': 'rate',
                            'date': 'date_added', 'price': 'price', 'price-desc': '-price'}

            products = Product.objects.all().order_by(
                f'{filters_list[filters["orderby"]]}')
        
        elif filters.get('s') and filters.get('post_type'):
            query = filters.get('s')
            products = Product.objects.filter(title__contains=query).order_by('sell_count')[:30]
        
        else:
            products = Product.objects.all().order_by('sell_count')

    else:
        products = Product.objects.all().order_by('sell_count')

    return render(request, 'shop.html', {'products': products, 'filters': filters})


def product_view(request, product_id=None):
    user = request.user    
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        if user.is_authenticated:
            req = request.POST
            form = MyFormCaptcha(req)
            if form.is_valid():
                title = req['title']
                rating = req['rating']
                content = req['comment']
                new_comment = Comments(user=user, product=product, title=title, rating=rating, content=content)
                new_comment.save()
                messages.add_message(request, messages.SUCCESS, "نظر شما با موفقیت ثبت شد")
                        
            else:
                messages.add_message(request, messages.ERROR, "کد امنیتی نامعتبر است")
        else:
            messages.add_message(request, messages.ERROR, "ابتدا وارد حساب کاربری خود شوید")
            
    
    
    is_in_wishlist = False    
    wishlist_items = get_wishlist_items(**({'user':user, 'get_products':True} if user.is_authenticated else {'session_key': request.session.session_key, 'get_products':True}))
    
    
    comments = Comments.objects.filter(product=product).order_by('-date_publish')
    
    commentform = MyFormCaptcha()
    
    print(comments)

    if product in wishlist_items:
        is_in_wishlist = True
    
    p_imgs = Product_images.objects.filter(product=product)
    
    return render(request, 'product.html', {'product': product,'imgs':p_imgs ,'is_in_wishlist':is_in_wishlist, 'commentform':commentform, 'comments':comments, 'range':range(1, 6)})


def blog_view(request, blog_title=None):
    if blog_title:
        blog = get_object_or_404(Blog, title=blog_title)
        blog.views = int(blog.views) + 1
        blog.save()
        return render(request, 'blog_content.html', {"blog": blog})
    else:
        blogs = Blog.objects.order_by('-date_publish')[:4]

        print(blogs)

        return render(request, 'blog.html', {"blogs": blogs})


def category_view(request, category_name):
    return render(request, 'category.html', {"name": category_name})


def about_us_view(request):
    return render(request, 'about-us.html', {})


def shop_rules(request):
    return render(request, 'shop-rules.html', {})


def category_product_view(request, cat):
    category = get_object_or_404(Category_Product, name=cat)
    filters = request.GET

    print(filters)

    category_id = Category_Product.objects.filter(
        name=category).values_list('id', flat=True).first()

    if len(filters) != 0:
        if filters.get('min_price') or filters.get('max_price'):
            if filters.get('min_price') and not filters.get('max_price'):
                products = Product.objects.filter(
                    category=category_id, price__gte=filters.get('min_price'))
            elif not filters.get('min_price') and filters.get('max_price'):
                products = Product.objects.filter(
                    category=category_id, price__lte=filters.get('max_price'))
            else:  
                products = Product.objects.filter(category=category_id, price__gte=filters.get(
                    'min_price'), price__lte=filters.get('max_price'))

        elif filters.get('orderby'):
            filters_list = {'popularity': 'sell_count', 'rating': 'rate',
                            'date': 'date_added', 'price': 'price', 'price-desc': '-price'}

            products = Product.objects.filter(category=category_id).order_by(
                f'{filters_list[filters["orderby"]]}')
        else:
            products = Product.objects.filter(category=category_id)

    else:
        products = Product.objects.filter(category=category_id,)

    return render(request, 'product-category.html', {'category': category, 'products': products[:30], 'filters': filters})


def wishlist_view(request):
    user = request.user
    if user.is_authenticated:
        wishlist = Wishlists.objects.filter(user=user)
        user_cart = Cart.objects.get(user=user, status='Not payed')
    else:
        wishlist = Wishlists.objects.filter(session_key=request.session.session_key)
        user_cart = Cart.objects.filter(user=None, status='Not payed', session_key=request.session.session_key)
        if not user_cart.exists():
            user_cart = Cart.objects.create(user=None, session_key=request.session.session_key)
        else:
            user_cart = user_cart[0]
    
    try:
        item_id = request.GET['remove_item']
    except:
        pass
    else:
        item = get_object_or_404(Wishlists_items, wishlist=wishlist[0],  id=item_id)
        item.delete()
    
    user_cart_items = Cart_item.objects.filter(cart=user_cart)
    in_cart_items = [obj['product_id'] for obj in user_cart_items.values()]
    
    print(in_cart_items)
    
    wish_items = Wishlists_items.objects.filter(wishlist=wishlist[0])

    
    return render(request, 'wishlist.html', {'wish_items':wish_items, 'in_cart_items':in_cart_items})
    
    
def cart_view(request):
    user = request.user
    
    if user.is_authenticated:
        user_cart = Cart.objects.get(user=user, status='Not payed')
    else:
        user_cart = Cart.objects.filter(user=None, status='Not payed', session_key=request.session.session_key)
        if not user_cart.exists():
            user_cart = Cart.objects.create(user=None, session_key=request.session.session_key)
        else:
            user_cart = user_cart[0]
            
    
    if request.method == 'POST':
        print('rigth here ! ')        
        data = request.POST

        if data['action'] == 'update-cart':
            for key, value in data.items():
                if 'qty' in key:
                    item_id = key.split('-')[1]
                    item = Cart_item.objects.get(id=item_id)
                    if value == '0':
                        item.delete()
                    else:
                        item.count = value            
                        item.save()
                        
    elif request.method == 'GET':
        data = request.GET
        try:
            item_id = data['remove_item']
        except:
            pass
        else:
            item = get_object_or_404(Cart_item, cart=user_cart, id=item_id)
            item.delete()
            
    cart_items = Cart_item.objects.filter(cart=user_cart)
    total_price = 0
    
    for item in cart_items:
        e_price = item.product.price
        quantity = item.count
        total_price += e_price*quantity
                
    return render(request, 'cart.html', {'cart_items':cart_items, 'total_price':total_price})


def checkout_view(request):
    user = request.user
    
    if user.is_authenticated:
        user_cart = Cart.objects.get(user=user, status='Not payed')
    else:
        user_cart = Cart.objects.filter(user=None, status='Not payed', session_key=request.session.session_key)
        if not user_cart.exists():
            user_cart = Cart.objects.create(user=None, session_key=request.session.session_key)
        else:
            user_cart = user_cart[0]
    
    cart_items = Cart_item.objects.filter(cart=user_cart)
    if len(cart_items) == 0:
        return redirect('/cart/')

    total_price = 0
    
    for item in cart_items:
        e_price = item.product.price
        quantity = item.count
        total_price += e_price*quantity
        
        
    return render(request, 'checkout.html', {'cart_items':cart_items, 'total_price':total_price})


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    
    return redirect('/')

def contact_us(request):
    return render(request, 'contact-us.html')

def category_blog_view(request, cat):

    category = get_object_or_404(Category_blog, name=cat)
    
    blogs = Blog.objects.filter(category=category).order_by('-date_publish')

    return render(request, 'category-blog.html', {"blogs": blogs, 'category':category})

def page_not_found(request, exception=None):
    return render(request, '404.html', status=404)
