from django.urls import path
from myapp import views  

app_name = 'myapp'

urlpatterns = [
    path(r'', views.index, name='index'),
    path('about/', views.about, name='about'),
    #path('<int:book_id>/', views.detail, name='detail'),
    path('<int:pk>/', views.BookDetailView.as_view(), name='detail'),
    path('findbooks/', views.findbooks, name='findbooks'),
    path('placeorder/', views.place_order, name='placeorder'),
    path('myorders/', views.my_orders, name='my_orders'),
    path('review/', views.review, name='review'),
    path('add_review/<int:book_id>/', views.add_review, name='add_review'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('register_user/', views.register_user, name='register_user'),
    path('chk_reviews/<int:book_id>/', views.chk_reviews, name='chk_reviews'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('forget_password/', views.forget_password, name='forget_password'),

    path('books/', views.BookListView.as_view(), name='books'),
    
    ]