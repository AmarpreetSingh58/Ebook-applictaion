from django import forms
from myapp.models import Order, Review, Member
from django.urls import reverse

# Use cripsy forms for final project
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('S', 'Scinece&Tech'),
        ('F', 'Fiction'),
        ('B', 'Biography'),
        ('T', 'Travel'),
        ('O', 'Other')
    ]
    name = forms.CharField(label='Your Name', max_length=100, required=False)
    category =   forms.ChoiceField(label='Select a category:', widget=forms.RadioSelect(),
                                        choices = CATEGORY_CHOICES, required=False)
    max_price = forms.IntegerField(label='Maximum Price', min_value=0, required=True)

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['books', 'member', 'order_type']
        widgets = {'books': forms.CheckboxSelectMultiple(), 'order_type':forms.RadioSelect()}
        labels = {'member': u'Member name', }

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['member'].empty_label = None
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'myapp:placeorder'

        self.helper.add_input(Submit('submit', 'Submit'))


class ReviewForm(forms.ModelForm):

    REVIEW_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Moderate'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]

    rating = forms.ChoiceField(choices=REVIEW_CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Review
        fields = [ 'reviewer', 'book', 'rating', 'comments']
        widgets = { 'book': forms.RadioSelect() }
        labels = {'reviewer': 'Please enter a valid email'}

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if int(rating) not in [1,2,3,4,5]:
            raise forms.ValidationError("You must enter a rating between 1 and 5!")

        return rating

class AddReviewForm(forms.ModelForm):

    REVIEW_CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Moderate'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]

    rating = forms.ChoiceField(choices=REVIEW_CHOICES, widget=forms.RadioSelect)
    #book = forms.HiddenInput()

    class Meta:
        model = Review
        fields = [ 'reviewer', 'rating', 'comments']
        labels = {'reviewer': 'Please enter a valid email'}

    def __init__(self, *args, **kwargs):
        self.book_id = kwargs.pop('book_id')
        super(AddReviewForm, self).__init__(*args, **kwargs)
        #self.fields['book'].widget.attrs['disabled'] = True                      
        #self.fields['book'].widget.attrs['required'] = False
        #Crispy forms options
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = reverse('myapp:add_review', args=[int(self.book_id)])
        self.helper.add_input(Submit('submit', 'Submit'))

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if int(rating) not in [1,2,3,4,5]:
            raise forms.ValidationError("You must enter a rating between 1 and 5!")

        return rating

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, help_text='Inform a valid email address.')

    class Meta:
        model = Member
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'myapp:register_user'

        self.helper.add_input(Submit('submit', 'Submit'))


class MemberForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [ 'id', 'first_name', 'last_name', 'photo']

    def __init__(self, *args, **kwargs):
        super(MemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form'
        self.helper.form_method = 'post'
        self.helper.form_action = 'myapp:user_profile'

        self.helper.add_input(Submit('submit', 'Submit'))