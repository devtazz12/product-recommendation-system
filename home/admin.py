from django.contrib import admin
from home.models import Contact, ScrappedProduct,Search,recommend_product


# Register your models here.
admin.site.register(Contact)

admin.site.register(ScrappedProduct)
admin.site.register(recommend_product)
admin.site.register(Search)