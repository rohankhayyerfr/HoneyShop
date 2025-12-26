from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductImage,
    ProductVariant,
    ProductSpecification,
    ProductPolicy
)

# ======================
# Category Admin
# ======================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ======================
# Inline Models for Product
# ======================

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'is_main', 'order')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = (
        'label',
        'weight',
        'price', 'old_price',
        'inventory',
        'is_available', 'is_best_seller',
    )

class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = (
        'title',
        'value',
        'order'
    )

class ProductPolicyInline(admin.StackedInline):
    model = ProductPolicy
    extra = 0
    max_num = 1
    fields = (
        'shipping_text',
        'return_text',
        'packaging_text',
    )


# ======================
# Product Admin
# ======================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'name', 'name', 'category', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('name', 'slug')

    readonly_fields = ('created_at',)

    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': (
                'category',
                'name',
                'slug',
                'short_description',
                'description',
                'is_active',
            )
        }),
        ('سیستمی', {
            'fields': ('created_at',)
        }),
    )

    inlines = [
        ProductVariantInline,
        ProductImageInline,
        ProductSpecificationInline,
        ProductPolicyInline,
    ]


# ======================
# ProductVariant Admin
# ======================
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = (
        'product', 'label',
        'price', 'inventory', 'is_available', 'is_best_seller'
    )
    list_filter = ('is_available', 'is_best_seller')
    list_editable = ('price', 'inventory', 'is_available', 'is_best_seller')


# ======================
# ProductSpecification Admin
# ======================
@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'title',
        'value',
        'order'
    )
    list_editable = ('value', 'order')
    list_filter = ('product',)


# ======================
# ProductPolicy Admin
# ======================
@admin.register(ProductPolicy)
class ProductPolicyAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'shipping_text',
        'return_text',
        'packaging_text',
    )
