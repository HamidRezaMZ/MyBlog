from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.models import User


# def home_page(request, page=1):
#     article_list = Article.objects.published()
#     paginator = Paginator(article_list, 2)
#     article = paginator.get_page(page)
#
#     context = {
#         "articles": article,
#         "category": Category.objects.filter(status=True)
#     }
#
#     return render(request, "article_list.html", context)

# def detail_article(request, slug):
#     context = {
#         "article": get_object_or_404(Article.objects.published(), slug=slug),
#     }
#
#     return render(request, "DetailArticle.html", context)
# def category_page(request, slug, page=1):
#     category = get_object_or_404(Category, slug=slug, status=True)
#     article_list = Article.objects.published()
#     paginator = Paginator(article_list, 2)
#     article = paginator.get_page(page)
#     context = {
#         "category": category,
#         "article": article,
#     }
#
#     return render(request, "Category.html", context)


class ArticleList(ListView):
    queryset = Article.objects.published()
    paginate_by = 2


class ArticleDetail(DetailView):
    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


class CategoryList(ListView):
    paginate_by = 5
    template_name = "Blog/category_list.html"

    def get_queryset(self):
        global category
        slug = self.kwargs.get('slug')
        category = get_object_or_404(Category.objects.active(), slug=slug)
        return category.article.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = category
        return context


class AuthorList(ListView):
    paginate_by = 5
    template_name = "Blog/author_list.html"

    def get_queryset(self):
        global author
        username = self.kwargs.get('username')
        author = get_object_or_404(User, username=username)
        return author.articles.published()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = author
        return context
