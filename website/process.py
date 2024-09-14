import json, re
from .models import Cart_item, Wishlists, Wishlists_items


def get_wishlist_items(user=None, session_key=None, get_products=False):
    if user:
        user_wishlist = Wishlists.objects.filter(user=user)
        if not user_wishlist.exists():
           user_wishlist = Wishlists.objects.create(user=user)
        else:
           user_wishlist = user_wishlist[0]
        
    else:
        user_wishlist = Wishlists.objects.filter(session_key=session_key)
        if not user_wishlist.exists():
            user_wishlist = Wishlists.objects.create(session_key=session_key)
        else:
            user_wishlist = user_wishlist[0]
        
    wishlist_items = Wishlists_items.objects.filter(wishlist=user_wishlist)  
    
    if get_products:
        wishlist_items = [obj.product for obj in wishlist_items]
    
    return wishlist_items


def get_detials(cart, user=None, session_key=None, add_=False):


    wishlist_count = len(get_wishlist_items(**({} if user else {'session_key': session_key})))
   
    items = Cart_item.objects.filter(cart=cart)

    lists = ""
    total_price = 0
    i = 0

    for item in items:

        lists = lists + f"""
                <li class="site_front-mini-cart-item mini_cart_item" >
                <a href="/product/{item.product.id}/" class="cart-item-link dj-fill">PLACE P</a>
                <a
                    href="/cart/?remove_item={item.id}"
                    class="remove remove_from_cart_button"
                    aria-label="{item.product.title}"
                    data-product_id="{item.product.id}"
                    data-cart_item_key="{item.product.id}"
                    data-product_sku=""
                >
                    &times;
                </a>
                <a href="/product/{item.product.id}/" class="cart-item-image">
                    <img
                        width="300"
                        height="300"
                        src="{item.product.main_image.url}"
                        class="attachment-site_front_thumbnail size-site_front_thumbnail"
                        alt=""
                        decoding="async"
                        srcset="{item.product.main_image.url} 300w, {item.product.main_image.url} 150w, {item.product.main_image.url} 600w, {item.product.main_image.url} 1024w, {item.product.main_image.url} 768w, {item.product.main_image.url} 1200w"
                        sizes="(max-width: 300px) 100vw, 300px"
                    />
                </a>
                <div class="cart-info">
                    <span class="dj-entities-title">{item.product.title}</span>
                    <span class="quantity d-flex justify-content-between">
                        <div>
                        {item.count} &times;
                        <span class="site_front-Price-amount amount">
                            <bdi data-price="{item.product.price}">{item.product.price}&nbsp;<span class="site_front-Price-currencySymbol">تومان</span></bdi>
                        </span>
                        </div>
                        <span class="color-item {item.color}" style="--clr:{item.color.hex_color}">
                        </span>
                    </span>
                </div>
            </li>

                """
        i += 1
        total_price += int(item.product.price) * int(item.count)

    print(total_price)

    # if not add_:
    #     res = {
    #             "fragments": {

    #                 "div.widget_shopping_cart_content": f'<div class="widget_shopping_cart_content"><div class="shopping-cart-widget-body dj-scroll"><div class="dj-scroll-content"><ul class="cart_list product_list_widget site_front-mini-cart ">{lists}</ul><!-- end product list --></div></div><div class="shopping-cart-widget-footer"><p class="site_front-mini-cart__total total"><strong>جمع جزء:</strong> <span class="site_front-Price-amount amount"><bdi data-price="{item.product.price}">{total_price}&nbsp;<span class="site_front-Price-currencySymbol">تومان</span></bdi></span></p><p class="site_front-mini-cart__buttons buttons"><a href="/cart/" class="button btn-cart fs-forward">مشاهده سبد خرید</a><a href="/checkout/" class="button checkout fs-forward">تسویه حساب</a></p></div></div>',
    #                 "span.dj-cart-number_dj": f'<span class="dj-cart-number dj-tools-count">3 <span>MSF</span></span>',
    #                 "span.dj-cart-subtotal_dj": f'<span class="dj-cart-subtotal"><span class="site_front-Price-amount amount"><bdi data-price="{item.product.price}">{total_price}&nbsp;<span class="site_front-Price-currencySymbol"> تومان</span></bdi></span></span>'
    #         },
    #     }

    # else:
    if i != 0:
        res = {
            "notices":f'<div class="site_front-message" role="alert">ntt<a href="/cart/" tabindex="1" class="button fs-forward">مشاهده سبد خرید</a> &ldquo;{item.product.title}&rdquo; به سبد خرید شما اضافه شد.</div>',
            "fragments": {
                "div.widget_shopping_cart_content": f'<div class="widget_shopping_cart_content"><div class="shopping-cart-widget-body dj-scroll"><div class="dj-scroll-content"><ul class="cart_list product_list_widget site_front-mini-cart ">{lists}</ul><!-- end product list --></div></div><div class="shopping-cart-widget-footer"><p class="site_front-mini-cart__total total"><strong>جمع جزء:</strong> <span class="site_front-Price-amount amount"><bdi data-price="{item.product.price}">{total_price}&nbsp;<span class="site_front-Price-currencySymbol">تومان</span></bdi></span></p><p class="site_front-mini-cart__buttons buttons"><a href="/cart/" class="button btn-cart fs-forward">مشاهده سبد خرید</a><a href="/checkout/" class="button checkout fs-forward">تسویه حساب</a></p></div></div>',
                "span.dj-cart-number_dj": f'<span class="dj-cart-number dj-tools-count">{i} <span>محصول</span></span>',
                "span.dj-cart-subtotal_dj": f'<span class="dj-cart-subtotal"><span class="site_front-Price-amount amount"><bdi data-price="{item.product.price}">{total_price}&nbsp;<span class="site_front-Price-currencySymbol"> تومان</span></bdi></span></span>'
            },
            "cart_items_count": i,
            "total_price":total_price,
        }
    else:
        res = {
            "notices":f'<div class="site_front-message" role="alert">ntt<a href="/cart/" tabindex="1" class="button fs-forward">مشاهده سبد خرید</a> &ldquo; . &rdquo; به سبد خرید شما اضافه شد.</div>',
            "fragments": {
                "div.widget_shopping_cart_content": f'<div class="widget_shopping_cart_content"><div class="shopping-cart-widget-body dj-scroll"><div class="dj-scroll-content"><ul class="cart_list product_list_widget site_front-mini-cart ">{lists}</ul><!-- end product list --></div></div><div class="shopping-cart-widget-footer"><p class="site_front-mini-cart__total total"><strong>جمع جزء:</strong> <span class="site_front-Price-amount amount"><bdi data-price="0">{total_price}&nbsp;<span class="site_front-Price-currencySymbol">تومان</span></bdi></span></p><p class="site_front-mini-cart__buttons buttons"><a href="/cart/" class="button btn-cart fs-forward">مشاهده سبد خرید</a><a href="/checkout/" class="button checkout fs-forward">تسویه حساب</a></p></div></div>',
                "span.dj-cart-number_dj": f'<span class="dj-cart-number dj-tools-count">{i} <span>محصول</span></span>',
                "span.dj-cart-subtotal_dj": f'<span class="dj-cart-subtotal"><span class="site_front-Price-amount amount"><bdi data-price="0">{total_price}&nbsp;<span class="site_front-Price-currencySymbol"> تومان</span></bdi></span></span>'
            },
            "cart_items_count": i,
            "total_price":total_price,
        }

    return res


def get_citys(state_id):
    with open('website/city.json', 'r', encoding='utf-8') as cityes:
        data = json.loads(cityes.read())
    
    return data[state_id]


def chack_phone(phone):
    if phone[0] == 0:
        phone = phone[0:]
    try:
        phone = int(phone)
    except:
        return False
    else:
        phone = str(phone)
        if len(phone) == 10:
            return True
        else:
            False
            

def password_checker(password):
    # Define the password strength criteria
    has_uppercase = False
    has_lowercase = False
    has_digit = False
    has_special_char = False
    has_length = False

    # Check length
    if len(password) >= 8:
        has_length = True
    else:
        return False
        

    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        has_uppercase = True

    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        has_lowercase = True

    # Check for digits
    if re.search(r"d", password):
        has_digit = True

    # Check for special characters
    if re.search(r"W", password):
        has_special_char = True

    # Evaluate the password strength
    strength = 0
    if has_length:
        strength += 1
    if has_uppercase:
        strength += 1
    if has_lowercase:
        strength += 1
    if has_digit:
        strength += 1
    if has_special_char:
        strength += 1
    
    if strength >= 1:
        return True
    else:
        return False
    