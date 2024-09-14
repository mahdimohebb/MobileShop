from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

# Register your models here.

admin.site.register(User)
admin.site.register(Category_Product)
admin.site.register(Category_blog)
admin.site.register(Cart)
admin.site.register(Cart_item)
admin.site.register(Color)
admin.site.register(Wishlists)
admin.site.register(Wishlists_items)
admin.site.register(Special_offer)
admin.site.register(Comments)
admin.site.register(Comments_likes)
admin.site.register(Product_images)


class ProductAdmin(SummernoteModelAdmin):
    summernote_fields = ('details')
    
class BlogAdmin(SummernoteModelAdmin):
    summernote_fields = ('content')


admin.site.register(Product, ProductAdmin)
admin.site.register(Blog, BlogAdmin)
    