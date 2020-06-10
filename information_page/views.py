from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.shortcuts import (
    get_object_or_404,
    redirect,
)
from django.views.generic.base import TemplateView
from django.views.generic import (
    DetailView,
    ListView,
    CreateView,
    UpdateView,
    DeleteView
)

from guardian.mixins import PermissionRequiredMixin, LoginRequiredMixin
from guardian.decorators import permission_required

from information_page.models import (
    Article,
    ArticleGenre,
    ArticleComment,
    ArticleNote
)
from information_page.forms import (
    CommentForm,
    NoteForm
)


ITEMS_PER_PAGE = 2
ARTICLE_TEMPLATES_BASE_DIR = 'information_page/articles'
GENRE_TEMPLATES_BASE_DIR = 'information_page/genres'
COMMENT_TEMPLATES_BASE_DIR = 'information_page/comments'
NOTE_TEMPLATES_BASE_DIR = 'information_page/notes'


# Create your views here.
#########################################################################
#########################################################################
# Home
class HomePageView(TemplateView):
    template_name = 'information_page/home_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        categories = ArticleGenre.objects.filter(
            parent__isnull=True)
        categories_articles = {}
        for category in categories:
            category_articles = category.article_set.filter(
                published=True).order_by('-publication_date')[:6]
            if category_articles:
                categories_articles[category] = category_articles

        context['categories'] = categories_articles
        published = Article.objects.filter(
            published=True).order_by(
            '-publication_date')[:categories.count() * 2]
        context['newest_posts'] = published

        return context


class AboutPageView(TemplateView):
    template_name = 'information_page/about.html'


#########################################################################
#########################################################################
# Articles
class ArticleDetails(DetailView):
    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/article_details.html'
    model = Article
    context_object_name = 'article'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        context['note_form'] = NoteForm()
        return context


class AllArticles(ListView):
    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/articles.html'
    model = Article
    paginate_by = ITEMS_PER_PAGE
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(published=True)


class ArticlesByCategory(ListView):
    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/articles_by_category_list.html'
    model = Article
    paginate_by = ITEMS_PER_PAGE
    context_object_name = 'articles'

    def get_queryset(self):
        return Article.objects.filter(
            genre__name__iexact=self.kwargs['category'],
            published=True).order_by(
            '-publication_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = ArticleGenre.objects.filter(
            name__iexact=self.kwargs['category']).first()
        return context


class ArticlesInDraft(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'information_page.view_article'

    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/articles_in_draft.html'
    model = Article
    paginate_by = ITEMS_PER_PAGE
    context_object_name = 'drafts'

    def get_queryset(self):
        return Article.objects.filter(
            published=False).order_by(
            '-publication_date')


class AuthorArticles(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'information_page.view_article'

    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/author_articles.html'
    model = Article
    paginate_by = ITEMS_PER_PAGE
    context_object_name = 'myarticles'

    def get_queryset(self):
        return Article.objects.filter(
            author__username__iexact=self.kwargs['username']).filter(
            published=True).order_by(
            '-publication_date')


class CreateArticle(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'information_page.add_article'
    # A lot of threads about it on github, just look in google for:
    # django guardian PermissionRequiredMixin return AttributeError
    permission_object = None

    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/create_article.html'
    model = Article
    fields = ['title', 'text', 'genre']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateArticle(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'information_page.change_article'

    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/update_article.html'
    model = Article
    fields = ['text']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.last_modification_date = datetime.now()
        self.object.save()
        return super(UpdateView, self).form_valid(form)


class DeleteArticle(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'information_page.delete_article'
    accept_global_perms = True

    template_name = f'{ARTICLE_TEMPLATES_BASE_DIR}/confirm_article_delete.html'
    model = Article
    success_url = reverse_lazy('my-list')


@login_required()
@permission_required('information_page.can_publish',
                     (Article, 'slug', 'slug'))
def publish(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article.publish()
    return redirect('informations:article-details', slug=slug)


#########################################################################
#########################################################################
# Genre
class CreateGenre(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'information_page.add_articlegenre'
    permission_object = None

    template_name = f'{GENRE_TEMPLATES_BASE_DIR}/create_genre.html'
    model = ArticleGenre
    fields = ['name', 'parent', 'description']


class GenresList(ListView):
    template_name = f'{GENRE_TEMPLATES_BASE_DIR}/genres_list.html'
    model = ArticleGenre
    paginate_by = ITEMS_PER_PAGE


class GenreDetails(DetailView):
    template_name = f'{GENRE_TEMPLATES_BASE_DIR}/genre_details.html'
    model = ArticleGenre


class DeleteGenre(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'information_page.delete_articlegenre'
    accept_global_perms = True

    template_name = f'{GENRE_TEMPLATES_BASE_DIR}/delete_genre.html'
    model = ArticleGenre
    success_url = reverse_lazy('genre-list')


#########################################################################
#########################################################################
# Comments
class Comments(ListView):
    template_name = f'{COMMENT_TEMPLATES_BASE_DIR}/comments.html'
    model = ArticleComment
    paginate_by = ITEMS_PER_PAGE
    context_object_name = 'comments'

    def get_queryset(self):
        return ArticleComment.objects.filter(
            author__username__iexact=self.kwargs['username'])


class DeleteComment(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'information_page.delete_articlecomment'
    accept_global_perms = True

    template_name = f'{COMMENT_TEMPLATES_BASE_DIR}/delete_comment.html'
    model = ArticleComment

    def get_success_url(self, **kwargs):
        return reverse_lazy(
            'informations:article-details',
            kwargs={'slug': self.object.article.slug})


class UpdateComment(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'information_page.change_articlecomment'

    template_name = f'{COMMENT_TEMPLATES_BASE_DIR}/update_comment.html'
    model = ArticleComment
    fields = ['text']


@login_required()
@permission_required('information_page.add_articlecomment')
def create_comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.article = article
            comment.save()
            return redirect('informations:article-details', slug=article.slug)


#########################################################################
#########################################################################
# Notes
class DeleteNote(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'information_page.delete_articlenote'
    accept_global_perms = True

    template_name = f'{NOTE_TEMPLATES_BASE_DIR}/delete_note.html'
    model = ArticleNote
    success_url = reverse_lazy('informations:home')


class UpdateNote(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'information_page.change_articlenote'

    template_name = f'{NOTE_TEMPLATES_BASE_DIR}/update_note.html'
    model = ArticleNote
    fields = ['text']


class Notes(LoginRequiredMixin, ListView):
    template_name = f'{NOTE_TEMPLATES_BASE_DIR}/notes.html'
    model = ArticleNote
    paginate_by = ITEMS_PER_PAGE

    def get_queryset(self):
        return ArticleNote.objects.filter(
            author__username__iexact=self.kwargs['username']).order_by(
            '-creation_date')


@login_required()
@permission_required('information_page.add_articlenote', accept_global_perms=True)
def create_note(request, slug):
    article = get_object_or_404(Article, slug=slug)
    if request.POST:
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.article = article
            note.author = request.user
            note.save()
            return redirect('informations:article-details', slug=article.slug)
