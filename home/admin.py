from django.contrib import admin
from home.models import Contact, ScrappedProduct,recommend_product,sastodeal_product,recommend_product_sastodeal,socheko_product,recommend_product_socheko
from home.models import ReviewRatingDaraz, ReviewRatingSocheko, ReviewRatingSastodeal


# Register your models here.
admin.site.register(Contact)

admin.site.register(ScrappedProduct)
admin.site.register(recommend_product)
admin.site.register(sastodeal_product)
admin.site.register(recommend_product_sastodeal)
admin.site.register(socheko_product)
admin.site.register(recommend_product_socheko)


admin.site.register(ReviewRatingDaraz)
admin.site.register(ReviewRatingSocheko)
admin.site.register(ReviewRatingSastodeal)
