from django.db.models import Prefetch
from django.views.generic import ListView
from django.shortcuts import render

from articles.models import Article, ArticleSection


def articles_list(request):
    articles = Article.objects.order_by('-published_at').prefetch_related(
        Prefetch(
            'articlesection_set',
            queryset=ArticleSection.objects.select_related('section'),
            to_attr='scopes'
        )
    )

    return render(request, 'articles/news.html', {'object_list': articles})


class ArticlesListView(ListView):
    model = Article
    template_name = 'articles/news.html'
    context_object_name = 'object_list'
    ordering = '-published_at'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.prefetch_related(
            Prefetch(
                'articlesection_set',
                queryset=ArticleSection.objects.select_related('section'),
                to_attr='scopes'
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
