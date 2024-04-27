from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import JsonResponse

from .models import BlogPost

@method_decorator(login_required(login_url='accounts/login/'), name='dispatch')
class IndexView(generic.ListView):
    template_name = "cms/index.html"
    context_object_name = "all_posts"
    def get_queryset(self) -> QuerySet[Any]:
        return BlogPost.objects.filter(author=self.request.user).order_by("-pub_date")

class DetailView(generic.DetailView):
    model = BlogPost
    template_name = "cms/detail.html"

class CreateView(generic.CreateView):
    model = BlogPost
    fields = ["title", "body", "status"]
    template_name = "cms/create.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()  # Add the form to the context
        return context
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class UpdateView(generic.UpdateView):
    model = BlogPost
    fields = ["title", "body", "status"]
    template_name = "cms/update.html"
    success_url = "/"

    def get_object(self, queryset = None) -> Model:
        obj = BlogPost.objects.get(id = self.kwargs["pk"])
        return obj
    
class DeleteView(generic.DeleteView):
    model: BlogPost
    template_name = "cms/delete.html"
    success_url = "/"

    def get_object(self, queryset = None) -> Model:
        obj = BlogPost.objects.get(id = self.kwargs["pk"])
        return obj

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
       

def restful_api(request, username):
    if username:
        posts = list(BlogPost.objects.filter(author__username=username).filter(status="published").values())
    else:
        posts = []
    response = JsonResponse({"posts": posts})
    return response