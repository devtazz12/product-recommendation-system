from django.contrib import admin
from home.models import Contact, ScrappedProduct,Search


# Register your models here.
admin.site.register(Contact)

admin.site.register(ScrappedProduct)
admin.site.register(Search)