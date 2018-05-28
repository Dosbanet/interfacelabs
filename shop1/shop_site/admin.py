from django.contrib import admin

from .models import Merch, Cart, UserTokenStorage
# Register your models here.

class MerchAdmin(admin.ModelAdmin):
    """Simply bundles fields for ease of use.

    Really, it's all it does.
    """
    fieldsets = [
        ('Merch info', {
            'fields': ['name', 'desc', 'image']
        }),
        ('Shop info', {
            'fields': ['price', 'quantity']
        }),
    ]

admin.site.register(Merch, MerchAdmin)
admin.site.register(Cart)
admin.site.register(UserTokenStorage)
