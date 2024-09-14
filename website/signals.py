from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Cart


@receiver(post_save, sender=User)
def create_cart(sender, instance, created, **kwargs):
    print("IM HERE")
    if created:
        if not instance.last_session_key:
            print("IM DO THINGS NOW") 
            session_key = instance.last_session_key
            print(session_key)
            cart = Cart.objects.get(session_key=session_key, status='Not payed')
            print(cart)
            cart.session_key = None
            cart.user = instance
            cart.save()
        else:
            Cart.objects.create(user=instance)