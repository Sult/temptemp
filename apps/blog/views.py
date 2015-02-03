from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from apps.users.forms import LoginForm
from apps.users.decorators import group_required
from apps.blog.forms import ArticleForm
from apps.blog.models import Article


def blog(request):
    login_form = LoginForm()
    if request.user.is_authenticated():
        articles = Article.objects.filter(published=True).order_by("-created")
    else:
        articles = Article.objects.filter(published=True, public=True).order_by("-created")
    
    #pagination
    paginator = Paginator(articles, 2, request=request)
    page = request.GET.get('page', 1)
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    
    return render(request, "blog/blog.html", {"articles": articles, "login_form": login_form})
    



@group_required("deno")
def blog_admin(request):
    articles = Article.objects.order_by("-modified")
    return render(request, "admin/blog_admin.html", {"articles": articles})



#create new article 
@group_required("deno")
def blog_create(request):
    form = ArticleForm(request.POST or None)
    if request.POST and form.is_valid():
        form.save_new(request.user, False)
        return HttpResponseRedirect(reverse("blog_admin"))
    
    return render(request, "admin/blog_edit.html", {"form": form})
    
    
    
@group_required("deno")
def blog_edit(request, slug):
    article = get_object_or_404(Article, slug=slug)
    form = ArticleForm(request.POST or None, instance=article)
    if request.POST and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse("blog_admin"))
    return render(request, "admin/blog_edit.html", {"form": form})



@group_required("deno")
def blog_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return HttpResponseRedirect(reverse("blog_admin"))
    



