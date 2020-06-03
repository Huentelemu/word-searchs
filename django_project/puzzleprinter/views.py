from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView

from .forms import BookForm, WordsListForm
from .models import Book, WordsList, Sopa

# Create your views here.
from django.template import loader

from .utils import read_words_file, WordSearch


def index(request):
    return render(request, 'puzzleprinter/index.html')


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES["document"]
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'puzzleprinter/upload.html', context)


def book_list(request):
    books = Book.objects.all()
    return render(request, 'puzzleprinter/book_list.html', {
        'books': books,
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'puzzleprinter/upload_book.html', {
        'form': form,
    })


def upload_list_words(request):
    if request.method == 'POST':
        form = WordsListForm(request.POST, request.FILES)
        if form.is_valid():
            word_list = form.save()
            list_of_lists = word_list.deliver_list_of_lists()
            for list_of_words in list_of_lists:
                ws = WordSearch(original_words=list_of_words, shape=(29, 17))
                soup = ws.string_representation
                soup = Sopa(list_of_words="\n".join(list_of_words),
                            words_list_object=word_list,
                            soup=soup)
                soup.save()

            return HttpResponseRedirect(reverse('results', args=(word_list.id,)))
    else:
        form = WordsListForm()
    return render(request, 'puzzleprinter/upload_list_words.html', {
        'form': form,
    })


def results(request, pk):
    words_list = WordsList.objects.get(pk=pk)
    return render(request, 'puzzleprinter/results.html', {
        'soups': words_list.sopa_set.all(),
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'


class UploadBookView(CreateView):
    model = Book
    fields = BookForm
    success_url = reverse_lazy('class_book_list')
    template_name = 'upload_book.html'
