from django.urls import path
from .views import *
from django.views.generic import RedirectView

urlpatterns = [
    path('func/', list_articles_func, name='func'),
    # http://localhost:8000/func/

    path('cbv/', ListArticlesView.as_view(), name='cbv'),
    # http://localhost:8000/cbv/

    path('base-views/', CustomListArticlesView.as_view(), name='base views'),
    # http://localhost:8000/base-views/

    path('template/', TemplateListArticles.as_view(), name='template'),
    # http://localhost:8000/template/

    path('redirect-to-func/', RedirectToFunc.as_view(), name='redirect to func'),
    # http://localhost:8000/redirect-to-func/

    path('redirect-to-cbv/', RedirectView.as_view(url='http://localhost:8000/cbv/'), name='redirect to cbv'),
    # http://localhost:8000/redirect-to-cbv/

    path('generic/list-view/', ListViewListArticlesView.as_view(), name='list view'),
    # http://localhost:8000/generic/list-view/

    path('generic/detail-view/<int:pk>/', DetailViewListArticlesView.as_view(), name='detail view'),
    # http://localhost:8000/generic/detail-view/<int:pk>/

    path('generic/create-view/', CreateViewListArticlesView.as_view(), name='create view'),
    # http://localhost:8000/generic/create-view/

    path('generic/delete-view/<int:pk>/', DeleteViewListArticlesView.as_view(), name='delete view')
    # http://localhost:8000/generic/delete-view/<int:pk>/
]
