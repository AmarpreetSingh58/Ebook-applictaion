from django.db import models
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Avg

class Publisher(models.Model):
    name = models.CharField(max_length=200)
    website = models.URLField()
    city = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=50, default='USA')

    def __str__(self):
        if self.name:
            return self.name
        return super().__str__()

class Book(models.Model):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=1, choices=CATEGORY_CHOICES, default='S')
    num_pages = models.PositiveIntegerField(default=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(1000)])
    publisher = models.ForeignKey(Publisher, related_name='books', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    num_reviews = models.PositiveIntegerField(default=0)

    def __str__(self):
        if self.title:
            return self.title
        return super().__str__()

    def review_avg(self):
        if self.review_set.all().count() > 0:
            return self.review_set.all().aggregate(Avg('rating'))['rating__avg']

        return 'Without reviews'


class Member(User):
    STATUS_CHOICES = [
        (1, 'Regular member'),
        (2, 'Premium Member'),
        (3, 'Guest Member'),
    ]

    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    address = models.CharField(max_length=300, blank='True', null='True')
    city = models.CharField(max_length=20, default='Windsor')
    province=models.CharField(max_length=2, default='ON')
    last_renewal = models.DateField(default=timezone.now)
    auto_renew = models.BooleanField(default=True)
    borrowed_books = models.ManyToManyField(Book, blank=True)
    photo = models.ImageField(blank=True, null=True)

    # Property to check if the data was right entered
    @property
    def bb_str(self):
        bb_list = list(self.borrowed_books.values_list('id', flat=True))
        return str(bb_list)

    class Meta:
        verbose_name = "member"

class Order(models.Model):

    ORDER_TYPE_CHOICES = [(0,'Purchase'),(1, 'Borrow')]

    books = models.ManyToManyField(Book)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    order_type = models.IntegerField(choices=ORDER_TYPE_CHOICES, blank=False, null=False, default=0)
    order_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.member and self.order_date:
            return ' - '.join((self.member.__str__(), self.order_date.isoformat()))
        return super().__str__()

    # Property to check if the data was right entered
    @property
    def books_str(self):
        b_list = list(self.books.values_list('id', flat=True))
        return str(b_list)

    @property
    def order_date_str(self):
        if self.order_date:
            return self.order_date.isoformat()[0:10]
        return ''

    def total_items(self):
        if self.books:
            return self.books.count()
        return 0
        
class Review(models.Model):
    reviewer = models.EmailField()
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comments = models.TextField(null=False, blank=False)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        if self.comments:
            return self.comments
        return ''

    @property
    def date_iso(self):
        if self.date:
            return self.date.isoformat()
        return ''
    
