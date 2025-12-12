# newsportal_backEnd/news/views.py

from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters # <-- IMPORTANT: Import the filters module
from .models import Article, Category, Comment
from .serializers import ArticleSerializer, CategorySerializer, CommentSerializer
from django.shortcuts import render, redirect
from .models import Article, Category, Reporter
from .llm_news import generate_news
from django.http import JsonResponse
from openai import OpenAI
import os

def test_llm(request):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Generate a short tech headline"}
        ]
    )

    output = response.choices[0].message.content

    # Remove leading/trailing quotes (if any)
    output = output.strip('"')

    return JsonResponse({"llm_output": output})

# news/views.py
from django.shortcuts import render, redirect
from .models import Article, Category, Reporter
from .llm_news import generate_news
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def generate_article_llm(request):
    categories = Category.objects.all()
    reporters = Reporter.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        category_id = request.POST.get("category")
        reporter_id = request.POST.get("reporter")

        category = Category.objects.get(id=category_id) if category_id else None
        reporter = Reporter.objects.get(id=reporter_id) if reporter_id else None

        content = generate_news(title, category.name if category else None,
                                reporter.user.username if reporter else None)

        article = Article.objects.create(
            title=title,
            content=content,
            category=category,
            reporter=reporter
        )

        return redirect(f"/admin/news/article/{article.id}/change/")  # redirect to article admin page

    return render(request, "admin/news/generate_article_form.html", {
        "categories": categories,
        "reporters": reporters
    })



class ArticleViewSet(viewsets.ModelViewSet):
    """
    Handles listing, retrieving, and (via Admin/Authentication) creating/updating articles.
    Implements search functionality.
    """
    queryset = Article.objects.all().order_by('-published_date')
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # --- SEARCH IMPLEMENTATION (User Requirement: Search Articles) ---
    filter_backends = [filters.SearchFilter]
    # The frontend ArticleList.js sends the search query to the 'search' parameter.
    # We tell DRF which fields to search within.
    search_fields = ['title', 'content', 'category__name'] 
    # -----------------------------------------------------------------


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Handles listing categories.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    """
    Handles listing and creating comments for a specific article.
    (User Requirement: View and Comment on articles)
    """
    serializer_class = CommentSerializer
    permission_classes = [AllowAny] # Allow any user (even anonymous) to post comments

    def get_queryset(self):
        # Retrieve the article_id from the URL (defined in news/urls.py)
        article_id = self.kwargs['article_id']
        # Filter comments to show only those belonging to the current article
        return Comment.objects.filter(article__id=article_id).order_by('created_on')

    def perform_create(self, serializer):
        # Automatically link the new comment to the correct Article instance
        article = Article.objects.get(pk=self.kwargs['article_id'])
        serializer.save(article=article)