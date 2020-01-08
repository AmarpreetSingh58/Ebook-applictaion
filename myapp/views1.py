from django.http import HttpResponse
from .models import Publisher, Book, Member, Order

# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    heading1 = '<p>' + 'List of available books: ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    heading2 = '<p>' + 'List of publisher: ' + '</p>'
    response.write(heading2)
    plist = Publisher.objects.all().order_by('-city')
    for p in plist:
        para = '<p>'+ str(p.id) + ': ' + p.name + '-' + p.city + '</p>'
        response.write(para)

    return response

def about(request):
    return HttpResponse('This is an eBook APP')

def detail(request, book_id):
    book = Book.objects.get(id=book_id)
    return HttpResponse('<p>Title: {0}</p><p>Price: ${1}</p><p>Publisher:{2}</p>'.format(book.title.upper(), str(book.price), book.publisher))
    