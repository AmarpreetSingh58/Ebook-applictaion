from django.shortcuts import render, redirect, reverse, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from myapp.models import Publisher, Book, Member, Order, Review
from django.shortcuts import get_object_or_404
from myapp.forms import SearchForm, OrderForm, ReviewForm, RegisterUserForm, AddReviewForm, MemberForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Avg
import random
from datetime import datetime, timedelta

from django.core.mail import send_mail


# Create your views here.

from django.views.generic import ListView, DetailView

class BookListView(ListView):
    model = Book
    context_object_name = 'booklist'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Add in the publisher
        can_add_review = False
        if self.request.user:
            if self.request.user.is_authenticated:
                # If user is Regular member or Premium Member
                if Member.objects.filter(status__in=[1,2]).filter(user_ptr=self.request.user).count() > 0:
                    can_add_review = True
        context['can_add_review'] = can_add_review
        return context


class BookDetailView(DetailView):
    model = Book


def index(request):
    booklist = Book.objects.all().order_by('id')[:10]
    return render(request, 'myapp/index.html', {'booklist': booklist})

def about(request):
    mynum = request.COOKIES.get('lucky_num')
    if not mynum:
        mynum = random.randint(1,100)
        
    response = render_to_response(template_name='myapp/about.html', context={'mynum':mynum})
    expire_date = datetime.now() + timedelta(minutes=5)
    #expire_date = datetime.now() + timedelta(seconds=5)
    response.set_cookie('lucky_num', mynum, expires=expire_date)

    return response
'''
def detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, template_name='myapp/detail.html', context={'book':book})
'''


def findbooks(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            max_price = form.cleaned_data['max_price']
            booklist = Book.objects.filter(price__lte=max_price)
            if category:
                booklist = booklist.filter(category=category)
            

            
            
            return render(request, 'myapp/results.html', 
                        context={'booklist':booklist, 'name':name, 'category': category})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findbooks.html', {'form':form})

@login_required
def place_order(request):

    #TODO: If the user is not the admin, the member will not be asked. 
    # The member will be the logged in user.

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            books = form.cleaned_data['books']
            order = form.save(commit=False)     
            member = order.member
            type = order.order_type
            order.save()
            total_purchase = 0
            if type == 1:       
                for b in books:  
                    member.borrowed_books.add(b)
                member.save()
            else:
                
                for b in books:  
                    order.books.add(b)
                    total_purchase += b.price 
                order.save()
            return render(request, 'myapp/order_response.html', {'books': books, 'order':order, 'total_purchase': total_purchase})
        else:
            return render(request, 'myapp/placeorder.html', {'form':form})

    else:
        form = OrderForm()
        if not request.user.is_superuser:
            form.fields['member'].queryset=Member.objects.filter(user_ptr=request.user)
        return render(request, 'myapp/placeorder.html', {'form':form})

def add_last_login(request):
    last_login = datetime.now()
    request.session['last_login'] = last_login.isoformat()
    # Session will expire in 1 hour
    request.session.set_expiry(3600)

# This is the old review code. The new one is add_review.
def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            book = form.cleaned_data['book']
            book.num_reviews += 1
            book.save()
            messages.success(request, 'Book reviewed successfully')
            return redirect('myapp:index')
        else:
            return render(request, 'myapp/review.html', {'form':form})
    else:
        form = ReviewForm()
        return render(request, 'myapp/review.html', {'form':form})

@login_required
def add_review(request, book_id):

    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        form = AddReviewForm(request.POST, book_id=book_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.save()
            book.num_reviews += 1
            book.save()
            messages.success(request, 'Book reviewed successfully')
            return redirect('myapp:books')
        else:
            return render(request, 'myapp/add_review.html', {'form':form})
            
    if request.user.email:
        form = AddReviewForm(initial={'book':book, 'reviewer': request.user.email}, book_id=book_id)
    else:
        form = AddReviewForm(initial={'book':book})
    return render(request, 'myapp/add_review.html', {'form':form, 'book_id':book.id, 'book':book})


# Create your views here.
def user_login(request):

    context={}

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        context['username'] = username
        context['password'] = password
        user = authenticate(username=username, password=password) 
        if user:
            if user.is_active:
                login(request, user)
                add_last_login(request)
                next_url = request.POST.get('next')
                if next_url:
                    return HttpResponseRedirect(next_url)
                return HttpResponseRedirect(reverse('myapp:books'))
                #return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'Your account is disabled.')
                return render(request, template_name='myapp/login.html', context=context)
                #return HttpResponse('Your account is disabled.')
        else:
            messages.error(request, 'Invalid login details.')
            return render(request, template_name='myapp/login.html', context=context)
            #return HttpResponse('Invalid login details.') 
    else:
        next_url = request.GET.get('next')
        if next_url:
            context['next']=next_url
        return render(request, 'myapp/login.html', context=context)

@login_required
def user_logout(request):
    logout(request)
    #return HttpResponseRedirect(reverse(('myapp:index')))
    return redirect('home')

@login_required
def chk_reviews(request, book_id):
    '''
        If the user is a Member, return all the average rating for the specified book 
        (i.e. book whose pk =  book_id). If there are no reviews submitted for the selected item, 
        display a suitable message.
    '''
    context = {}
    template_name = 'myapp/chk_reviews.html'

    if Member.objects.filter(username=request.user.username).count() == 0:
        messages.warning(request, 'You are not a registered member')
        return render(request, template_name=template_name, context=context)
    
    
    book = get_object_or_404(Book, id=book_id)
    context['book'] = book
    review_avg = Review.objects.filter(book_id=book_id).aggregate(Avg('rating'))
    context['review_avg'] = review_avg
    reviews = Review.objects.filter(book_id=book_id)
    context['reviews'] = reviews

    can_add_review = False
    if request.user:
        if request.user.is_authenticated:
            # If user is Regular member or Premium Member
            if Member.objects.filter(status__in=[1,2]).filter(user_ptr=request.user).count() > 0:
                can_add_review = True
    context['can_add_review'] = can_add_review

    return render(request, template_name=template_name, context=context)



def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            m = Member()
            m.user_prt = user
            m.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            add_last_login(request)
            return redirect('home')
    else:
        form = RegisterUserForm()
    return render(request, 'myapp/register.html', {'form': form})

@login_required
def user_profile(request):

    template_name='myapp/profile.html'
    member=None
    form=None
    context={}
    
    if Member.objects.filter(user_ptr=request.user).count() > 0:
        member = Member.objects.get(user_ptr=request.user)
        context['member'] = member
    else:
        messages.warning(request, 'Logged user is not a member and does not have a profile')

    print(member)

    if request.method == 'POST':
        form = MemberForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            member = form.save()
            messages.success(request, 'Information is updated')
            context['form']=form
            return render(request, template_name=template_name, context=context)
    else:
        form = MemberForm(instance=member)
    
    context['form'] = form
    return render(request, template_name=template_name, context=context)


@login_required
def my_orders(request):

    orders = None
    user_id = request.user.id

    if Member.objects.filter(id=user_id).count() == 0:
        messages.error(request, 'You are not a registered member!')
        return render(request, template_name='myapp/my_orders.html', context={'orders':orders})

    
    member = Member.objects.get(id=user_id)
    orders = Order.objects.filter(member=member)

    if orders.count() == 0:
        messages.warning(request, 'You do not have orders')


    return render(request, template_name='myapp/my_orders.html', context={'orders':orders})


def forget_password(request):

    if request.method == 'POST':
        email = request.POST['email']
        if Member.objects.filter(email=email).count() > 0:
            member = Member.objects.filter(email=email)[0]

            password = Member.objects.make_random_password()
            member.set_password(password)
            member.save()

            # send email

            send_mail(
                'Ebook app - New Password',
                'Your new password is ' + password,
                'noreply@ebookapp.com',
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Your new password was sent by email.')
            messages.warning(request, 'For demo purporse your password is ' + password)
            return redirect('myapp:user_login')
        else:
            messages.error(request, 'The email informed is not a valid user email.')

    return render(request, template_name='myapp/forget_password.html')
