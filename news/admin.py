from django.contrib import admin
from django.urls import path
from .models import Article, ArticleImage, ArticleVideo, Category, Reporter, Comment
from .views import generate_article_llm
from .llm_news import generate_news

# --- Inlines ---
class ArticleImageInline(admin.TabularInline):
    model = ArticleImage
    extra = 1

class ArticleVideoInline(admin.TabularInline):
    model = ArticleVideo
    extra = 1

# --- Admin action ---
@admin.action(description="Generate crime news in india")
def generate_news_content(modeladmin, request, queryset):
    for article in queryset:
        if not article.content:
            article.content = generate_news(
                article.title,
                article.category.name,
                article.reporter.user.username if article.reporter else None
            )
            article.save()

# --- Article Admin ---
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'reporter', 'category', 'rank', 'published_date')
    inlines = [ArticleImageInline, ArticleVideoInline]
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'content')
    actions = [generate_news_content]
    change_list_template = "admin/news/article/change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "generate-article/",
                self.admin_site.admin_view(generate_article_llm),
                name="generate-article"
            ),
        ]
        return custom_urls + urls

    change_list_template = "admin/news/article/change_list.html"

# --- Register other models ---
admin.site.register(Reporter)
admin.site.register(Category)
admin.site.register(Comment)
