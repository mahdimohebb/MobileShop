from django import template
from website.models import Blog, Category_blog, Category_Product, Product, Comments_likes, Cart_item


register = template.Library()


@register.simple_tag(name='get_best_products')
def get_best_products(cat=None, count=5):
    if cat:
        category_id = Category_Product.objects.filter(name=cat).values_list('id', flat=True).first()
        products = Product.objects.filter(category=category_id).order_by('sell_count')[:count]
    else:
        products = Product.objects.all().order_by('sell_count')[:count]
    
    return products


@register.simple_tag(name='get_product_categories')
def get_product_categories():
    categories = Category_Product.objects.all()
    return categories  


@register.simple_tag(name='recent_blogs')
def recent_blogs():
    blogs = Blog.objects.order_by('-date_publish')[:4]
    return blogs

@register.simple_tag(name='categories')
def categories():
    categories = Category_blog.objects.all()[:7]
    return categories


@register.simple_tag(name='description_cut')
def description_cut(text):
    if len(text) > 70:
        text = text[:70] + '...'
    
    return text


@register.simple_tag(name='date_shamsi')
def date_shamsi(date, m_d=False):
    
    date = date.split(' ')

    def gregorian_to_jalali(gy, gm, gd):
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if (gm > 2):
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        print(days)
        if (days > 365):
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if (days < 186):
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]


    def jalali_to_gregorian(jy, jm, jd):
        jy += 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
        if (jm < 7):
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186
            gy = 400 * (days // 146097)
            days %= 146097
        if (days > 36524):
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
        if (days >= 365):
            days += 1
            gy += 4 * (days // 1461)
            days %= 1461
        if (days > 365):
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
            gd = days + 1
        if ((gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0)):
            kab = 29
        else:
            kab = 28
            sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
            gm = 0
        while (gm < 13 and gd > sal_a[gm]):
            gd -= sal_a[gm]
            gm += 1
        return [gy, gm, gd]



    year = int(date[0])
    month = int(date[1])
    day = int(date[2])
    
    jalali_date = gregorian_to_jalali(year, month, day)
    
    if m_d:
        d = jalali_date[2]
        months = {1:'فروردین', 2:'اردیبهشت', 3:'خرداد', 4:'تیر', 5:'مرداد', 6:'شهریور', 7:'مهر', 8:'آبان', 9:'آذر', 10:'دی', 11:'بهمن', 12:'اسفند'}
        m = months[jalali_date[1]]
        
        return [d, m]
        
    else:
        jalali_date = f'{jalali_date[0]}/{jalali_date[1]}/{jalali_date[2]}'
        return jalali_date
    
@register.simple_tag(name='multiply')
def multiply(num1, num2):
    return (int(num1) * int(num2)) 

@register.simple_tag(name='get_prev_blog')
def get_prev_blog(blog):
    blogs = Blog.objects.all().order_by('-date_publish')
    index = [i for i, obj in enumerate(blogs) if obj == blog][0]
    print(index)
    return blogs[index + 1] if index + 1 < len(blogs) else None


@register.simple_tag(name='get_next_blog')
def get_next_blog(blog):
    blogs = Blog.objects.all().order_by('-date_publish')
    index = [i for i, obj in enumerate(blogs) if obj == blog][0]
    return blogs[index - 1] if index > 0 else None

@register.simple_tag(name='is_liked_comment')
def is_liked_comment(comment, user):
    try:
        if user.is_authenticated:
            like = Comments_likes.objects.get(comment=comment, user=user)
        else:
            return False
    except:
        return False
    else:
        return True

@register.simple_tag(name='comment_likes')
def comment_likes(comment):
    like = Comments_likes.objects.filter(comment=comment)
    return len(like)

@register.simple_tag(name='cart_items_count')
def cart_items_count(cart):
    items = Cart_item.objects.filter(cart=cart)
    return len(items)

@register.simple_tag(name='cart_items')
def cart_items(cart):
    items = Cart_item.objects.filter(cart=cart)
    return items
