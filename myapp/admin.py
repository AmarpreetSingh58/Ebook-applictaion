from django.contrib import admin
from .models import Publisher, Book, Member, Order, Review

# Register your models here.

class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password', 'first_name', 'last_name', 'status', 'address', 'city', 'province', 'auto_renew', 'last_renewal', 'bb_str']
    #list_display_links = None
    #list_editable = ['username', 'password', 'first_name', 'last_name', 'status', 'address', 'city', 'province', 'auto_renew', 'last_renewal']

class OrderAdmin(admin.ModelAdmin):
    fields = [('books'), ('member', 'order_type','order_date')]
    list_display = ['id', 'member', 'order_type', 'order_date_str', 'books_str', 'total_items']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'book', 'rating', 'comments', 'date']

class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name', 'website', 'city']


def add_ten_dollars(modeladmin, request, queryset):
    for book in queryset:
        book.price = book.price + 10
        book.save()
add_ten_dollars.short_description = "Add $10"

def update_reviews(modeladmin, request, queryset):
    for book in queryset:
        n = book.review_set.count()
        book.num_reviews = n
        book.save()
update_reviews.short_description = "Update number of reviews"        

class BookAdmin(admin.ModelAdmin):
    fields = [('title', 'category', 'publisher'), ('num_pages', 'price', 'num_reviews')]
    list_display = ['title', 'category', 'num_pages', 'price', 'publisher','description', 'num_reviews']
    actions = [add_ten_dollars, update_reviews]

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review, ReviewAdmin)
