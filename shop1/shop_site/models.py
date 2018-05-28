from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Merch(models.Model):
    """Class to describe merchandise.

    Fields are self-explanatory. Image points at default image by default.
    """
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)
    desc = models.TextField(default="No description.")
    image = models.CharField(default="shop_site/images/no_image.png", max_length=100)

    def __str__(self):
        """Magic method.

        Magic is all it really does.
        """
        return self.name

class Cart(models.Model):
    """Main class to describe users shopping cart.

    Uses helper class CartHolder to handle M2M relationships. Perishes after purchase is
    finalised.
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Merch, through="CartHolder", through_fields=('who', 'what'))

    def __str__(self):
        """Magic method.

        Magic is all it really does.
        """
        return self.owner.username + "'s cart"

    def total_summ(self):
        """Counts total price of all stuff in cart.

        Pretty obvious one.
        """
        summ = 0
        temp_set = CartHolder.objects.filter(who=self)
        for item in temp_set:
            summ += int(item.what.price) * item.how_much
        return summ

    def contents(self):
        """Outputs contents for views to handle.

        Output is list of 2-tuples (Merch, integer).
        """
        cont = []
        temp_set = CartHolder.objects.filter(who=self)
        for item in temp_set:
            cont.append((item.what, item.how_much))
        return cont

    def add_merch(self, merch, num):
        """Adds merch in cart.

        Handles making record in helper table if needed.
        """
        try:
            cart_h = CartHolder.objects.get(who=self, what=merch)
        except CartHolder.DoesNotExist:
            cart_h = CartHolder(who=self, what=merch)
            cart_h.save()
        current = cart_h.how_much
        cart_h.how_much = current + int(num)
        cart_h.save()

    def sub_merch(self, merch, num):
        """Substracts merch from cart.

        Substracting merch which wasn't in cart is an error.
        """
        try:
            cart_h = CartHolder.objects.get(who=self, what=merch)
        except CartHolder.DoesNotExist:
            print("This really shouldn't have happened.")
            print(str(self), str(merch), num)
            return
        current = cart_h.how_much
        cart_h.how_much = current - abs(int(num))
        if cart_h.how_much == 0:
            cart_h.delete()
        else:
            cart_h.save()

class CartHolder(models.Model):
    """Helper class to handle M2M relationship for Cart class.

    Stores what cart it belongs to, what is stored in it, and how much.
    """
    who = models.ForeignKey(Cart, on_delete=models.CASCADE)
    what = models.ForeignKey(Merch, on_delete=models.CASCADE)
    how_much = models.IntegerField(default=0)

class UserTokenStorage(models.Model):
    token = models.CharField(max_length=200)
    expires = models.DateTimeField('date when token expires')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
