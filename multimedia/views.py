from django.shortcuts import redirect
from django.views.generic import ListView, DetailView,CreateView
from django.views.generic import TemplateView
from .models import BooksLibrary, Gallery, SpiritualPoemSong, UserManual, PraiseGlory, TestimonyOfSalvation, ArchiveLink
from .forms import BooksLibraryForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import BooksLibrary
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST



class MultimediaView(TemplateView):
    template_name = 'multimedia/multimediaView.html'

class BooksLibraryListView(ListView):
    model = BooksLibrary
    template_name = 'multimedia/books_library_list.html'
    context_object_name = 'books'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = BooksLibraryForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = BooksLibraryForm(request.POST, request.FILES)
        
        if form.is_valid():
            form.instance.user = self.request.user
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            published_date = form.cleaned_data.get('published_date')
            
            # Check if a book with the same title, author, and published date already exists
            if BooksLibrary.objects.filter(title=title, author=author, published_date=published_date).exists():
                form.add_error(None, "A book with the same title, author, and published date already exists.")
                # Render the same page with the invalid form
                return self.form_invalid(form)
            else:
                form.save()
                return redirect('multimedia:books_library_list')
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        # Ensure the object_list is set for rendering the context
        self.object_list = self.get_queryset()
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

        
class BooksLibraryDetailView(DetailView):
    model = BooksLibrary
    template_name = 'multimedia/books_library_detail.html'
    context_object_name = 'book'

class GalleryListView(ListView):
    model = Gallery
    template_name = 'multimedia/gallery_list.html'
    context_object_name = 'media'
    paginate_by = 10

class GalleryDetailView(DetailView):
    model = Gallery
    template_name = 'multimedia/gallery_detail.html'
    context_object_name = 'media_item'

class UserManualListView(ListView):
    model = UserManual
    template_name = 'multimedia/user_manual_list.html'
    context_object_name = 'user_manuals'
    paginate_by = 10

class UserManualDetailView(DetailView):
    model = UserManual
    template_name = 'multimedia/user_manual_detail.html'
    context_object_name = 'user_manual'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manual = self.get_object()

        # Example: finding related manuals based on the same category or other criteria
        related_manuals = UserManual.objects.all().exclude(id=manual.id)[:6]  # Excluding the current manual and limiting to 4
        
        context['related_manuals'] = related_manuals
        return context

class PraiseGloryListView(ListView):
    model = PraiseGlory
    template_name = 'multimedia/praise_glory_list.html'
    context_object_name = 'praises'
    paginate_by = 10
    
class PraiseGloryDetailView(DetailView):
    model = PraiseGlory
    template_name = 'multimedia/praise_glory_detail.html'
    context_object_name = 'praise_glory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        praise_glory = self.get_object()

        # Example: finding related praises based on some criteria
        related_praises = PraiseGlory.objects.exclude(id=praise_glory.id)[:4]  # Excluding the current praise and limiting to 4

        context['related_praises'] = related_praises
        return context


class TestimonyOfSalvationListView(ListView):
    model = TestimonyOfSalvation
    template_name = 'multimedia/testimony_of_salvation_list.html'
    context_object_name = 'testimonies'
    paginate_by = 10

class TestimonyOfSalvationDetailView(DetailView):
    model = TestimonyOfSalvation
    template_name = 'multimedia/testimony_of_salvation_detail.html'
    context_object_name = 'testimony'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        testimony = self.get_object()
        if testimony :
            # Example: finding related testimonies based on some criteria
            related_testimonies = TestimonyOfSalvation.objects.exclude(id=testimony.id)[:4]  # Excluding the current testimony and limiting to 4
            context['related_testimonies'] = related_testimonies
        return context

class ArchiveLinkListView(ListView):
    model = ArchiveLink
    template_name = 'multimedia/archive_link_list.html'
    context_object_name = 'archives'
    paginate_by = 10

class ArchiveLinkDetailView(DetailView):
    model = ArchiveLink
    template_name = 'multimedia/archive_link_detail.html'
    context_object_name = 'archive'

class BooksLibraryCreateView(CreateView, LoginRequiredMixin):
    model = BooksLibrary
    form_class = BooksLibraryForm
    template_name = 'multimedia/books_library_form.html'
    success_url = reverse_lazy('multimedia:books_library_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        title = form.cleaned_data.get('title')
        author = form.cleaned_data.get('author')
        published_date = form.cleaned_data.get('published_date')
        
        # Check if a book with the same title, author, and published date already exists
        if BooksLibrary.objects.filter(title=title, author=author, published_date=published_date).exists():
            form.add_error(None, "A book with the same title, author, and published date already exists.")
            return self.form_invalid(form)
        
        return super().form_valid(form)


@login_required
@require_POST
def vote_book(request):
    book_id = request.POST.get('book_id')
    action = request.POST.get('action')
    user = request.user

    try:
        book = BooksLibrary.objects.get(id=book_id)
        
        if action == 'vote':
            if not book.voters.filter(id=user.id).exists():
                book.voters.add(user)
                book.voteCount += 1
                book.save()
                return JsonResponse({'status': 'ok', 'voteCount': book.voteCount})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have already voted.'})
        elif action == 'unvote':
            if book.voters.filter(id=user.id).exists():
                book.voters.remove(user)
                book.voteCount -= 1
                book.save()
                return JsonResponse({'status': 'ok', 'voteCount': book.voteCount})
            else:
                return JsonResponse({'status': 'error', 'message': 'You have not voted yet.'})
    except BooksLibrary.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Book not found.'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid action.'})

class SpiritualPoemSongListView(ListView):
    model = SpiritualPoemSong
    template_name = 'multimedia/spiritual_poem_song_list.html'
    context_object_name = 'poems_songs'
    paginate_by = 10

class SpiritualPoemSongDetailView(DetailView):
    model = SpiritualPoemSong
    template_name = 'multimedia/spiritual_poem_song_detail.html'
    context_object_name = 'poem_song'
    
    
# multimedia/
# books_library_list.html
# books_library_form.html
# books_library_detail.html
# gallery_list.html
# gallery_detail.html
# user_manual_list.html
# user_manual_detail.html
# praise_glory_list.html
# praise_glory_detail.html
# testimony_of_salvation_list.html
# testimony_of_salvation_detail.html
# archive_link_list.html
# archive_link_detail.html
# spiritual_poem_song_list.html
# spiritual_poem_song_detail.html