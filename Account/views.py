from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .mixins import *
from django.urls import reverse_lazy
from django.contrib.auth import logout
from .models import User
from .forms import ProfileForm

class ArticleList(LoginRequiredMixin, ListView):
    template_name = "registration/home.html"

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=self.request.user)


class ArticleCreate(LoginRequiredMixin, FormValidMixin, FieldsMixin, CreateView):
    model = Article
    template_name = "registration/Article_Create_Update.html"


class ArticleUpdate(AuthorAccessMixin, FormValidMixin, FieldsMixin, UpdateView):
    model = Article
    template_name = "registration/Article_Create_Update.html"


class ArticleDelete(SuperUserAccessMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('account:home')
    template_name = "registration/article_confirm_delete.html"


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('Blog:Home')


class Profile(UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "registration/Profile.html"

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    success_url = reverse_lazy("account:profile")


    def get_form_kwargs(self):
        kwargs = super(Profile,self).get_form_kwargs()
        kwargs.update({
            "user":self.request.user
        })
        return kwargs