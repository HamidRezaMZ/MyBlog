from django.urls import path
from .views import ArticleList, ArticleDetail, CategoryList,AuthorList,ArticlePreview

app_name = "Blog"

urlpatterns = [
    path('', ArticleList.as_view(), name="Home"),
    path('page/<int:page>', ArticleList.as_view(), name="Home"),
    path('article/<slug:slug>', ArticleDetail.as_view(), name="Article"),
    path('preview/<int:pk>', ArticlePreview.as_view(), name="Preview"),
    path('category/<slug:slug>', CategoryList.as_view(), name="Category"),
    path('category/<slug:slug>/page/<int:page>', CategoryList.as_view(), name="Category"),
    path('author/<slug:username>', AuthorList.as_view(), name="Author"),
    path('author/<slug:username>/page/<int:page>', AuthorList.as_view(), name="Author"),
]
