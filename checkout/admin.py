from django.contrib import admin

from checkout.models import ItemOrder, Order

# Register your models here.


class ItemOrderInline(admin.TabularInline):
    model = ItemOrder
    extra = 0


class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ("product", "quantity", "order")


admin.site.register(ItemOrder, ItemOrderAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "address_customer", "items_order", "order_number")
    inlines = [ItemOrderInline]


admin.site.register(Order, OrderAdmin)
