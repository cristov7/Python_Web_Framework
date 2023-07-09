from django.http import HttpRequest
from .models import *
from django.shortcuts import render
from django.views.generic import View, TemplateView, RedirectView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import classonlymethod
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django import forms


# A view is a callable which takes a request and returns a response
# Class-based views provide an alternative way to implement views as Python objects instead of functions


# Function-Based Views:
def list_articles_func(request: HttpRequest):
    template_name = 'articles/baseviews.html'
    context = {'all_article_objects': ArticleModel.objects.all()}
    return render(request, template_name, context)


# class AdminsOnlyView:
#     def is_admin(self):
#         pass


# Class-Based Views:
class ListArticlesView(View):   # class ListArticlesView(AdminsOnlyView, View):
    template_name = 'articles/baseviews.html'

    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):   # def get_context_data(...):
        context = {'all_article_objects': ArticleModel.objects.all()}
        return render(self.request, self.template_name, context)   # def render_to_response(...):


# CustomBaseView -> Base Views
class CustomBaseView:
    def post(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):
        pass

    @classonlymethod
    def as_view(cls):
        self = cls()

        def view(request: HttpRequest):
            if request.method == 'POST':
                return self.post(request)
            else:   # request.method == 'GET':
                return self.get(request)
        return view


# Class-Based Views -> Base Views:
class CustomListArticlesView(CustomBaseView):
    template_name = 'articles/baseviews.html'

    def get(self, request, *args, **kwargs):   # def get_context_data(...):
        context = {'all_article_objects': ArticleModel.objects.all()}
        return render(request, self.template_name, context)   # def render_to_response(...):


# Class-Based Views -> TemplateView:
class TemplateListArticles(TemplateView):
    template_name = 'articles/templateview.html'

    # static data:
    extra_context = {'all_article_objects': ArticleModel.objects.all()}

    # dynamic data:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_article_objects'] = ArticleModel.objects.all()
        return context


# Class-Based Views -> RedirectView:
class RedirectToFunc(RedirectView):
    url = reverse_lazy('func')


# => Generic Views:
# C -> Create (POST: 'CreateView')
# R -> Read (GET: 'ListView' = Model.objects.all(); 'DetailView' = Model.objects.get())
# U -> Update (PUT / PATCH: 'UpdateView')
# D -> Delete (DELETE: 'DeleteView')


# Generic Views -> ListView:
class ListViewListArticlesView(ListView):   # 'ListView' representing a list of objects
    template_name = 'articles/listview.html'
    model = ArticleModel
    # if not 'context_object_name':
    # - default: 'object_list' = ArticleModel.objects.all()
    # - 'model name' + 'list' -> 'articlemodel_list' = ArticleModel.objects.all()
    context_object_name = 'all_article_objects'   # 'all_article_objects' = ArticleModel.objects.all()
    paginate_by = 3   # limit of 3 objects (in page)

    def get_queryset(self):
        queryset = super().get_queryset()

        search = self.request.GET.get('search', '')
        queryset = queryset.filter(title__icontains=search)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


# Generic Views -> DetailView:
class DetailViewListArticlesView(DetailView):   # while 'DetailView' is executing, self.object will contain the object
    template_name = 'articles/detailview.html'
    model = ArticleModel
    # if not 'context_object_name':
    # - default: 'object' = ArticleModel.objects.get()
    # - 'model name' -> 'articlemodel' = ArticleModel.objects.get()
    context_object_name = 'article_object'   # 'article_object' = ArticleModel.objects.get()
    # pk_url_kwarg = 'number'   # http://localhost:8000/generic/detail-view/<int:number>/   (default: 'pk' or / and 'slug')


class DisabledFormFieldsMixin:
    disabled_fields = []

    def get_form(self, *args, **kwargs):   # return instance
        form = super().get_form(*args, **kwargs)
        for field in self.disabled_fields:
            form.fields[field].widget.attrs['disabled'] = 'disabled'
            form.fields[field].widget.attrs['readonly'] = 'readonly'
        return form


# Generic Views -> CreateView:
class CreateViewListArticlesView(CreateView):   # class CreateViewListArticlesView(DisabledFormFieldsMixin, CreateView):
    template_name = 'articles/createview.html'
    model = ArticleModel
    # fields = '__all__'   # Forms: 1
    success_url = reverse_lazy('list view')   # Redirect after valid POST request

    # def form_valid(self, form):
    #     pass

    # def form_invalid(self, form):
    #     pass

    form_class = modelform_factory(   # Forms: 2
        ArticleModel,
        fields='__all__',
        widgets={'title': forms.TextInput(attrs={'placeholder': 'title'}),
                 'content': forms.Textarea(attrs={'placeholder': 'content'})})

    # disabled_fields = ['title']   # NOT built-in

    # def get_form(self, *args, **kwargs):   # Forms: 3
    #     form = super().get_form(*args, **kwargs)
    #     for field in self.disabled_fields:
    #         form.fields[field].widget.attrs['disabled'] = 'disabled'
    #         form.fields[field].widget.attrs['readonly'] = 'readonly'
    #     return form

    # def get_form_class(self):   # Forms: 4
    #     pass


# Generic Views -> UpdateView:
class UpdateViewListArticlesView(UpdateView):
    pass


# Generic Views -> DeleteView:
class DeleteViewListArticlesView(DisabledFormFieldsMixin, DeleteView):
    template_name = 'articles/deleteview.html'
    model = ArticleModel
    # if not 'context_object_name':
    # - default: 'object' = ArticleModel.objects.get()
    # - 'model name' -> 'articlemodel' = ArticleModel.objects.get()
    context_object_name = 'article_object'   # 'article_object' = ArticleModel.objects.get()

    form_class = modelform_factory(ArticleModel, fields='__all__')

    disabled_fields = ['title', 'content']  # NOT built-in

    def get_form_kwargs(self):
        instance = self.get_object()
        form_kwargs = super().get_form_kwargs()
        form_kwargs.update(instance=instance)
        return form_kwargs

    success_url = reverse_lazy('list view')  # Redirect after valid POST request
