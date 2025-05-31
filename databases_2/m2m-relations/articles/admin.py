from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.text import slugify
from .models import Article, Section, ArticleSection


class ArticleSectionInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()

        if not any(form.cleaned_data and not form.cleaned_data.get('DELETE', False)
                   for form in self.forms):
            raise ValidationError('Статья должна иметь хотя бы один раздел')

        primary_count = sum(
            1 for form in self.forms
            if form.cleaned_data
            and not form.cleaned_data.get('DELETE', False)
            and form.cleaned_data.get('is_primary', False)
        )

        if primary_count == 0:
            raise ValidationError('Укажите основной раздел')
        elif primary_count > 1:
            raise ValidationError('Основным может быть только один раздел')


class ArticleSectionInline(admin.TabularInline):
    model = ArticleSection
    formset = ArticleSectionInlineFormSet
    extra = 1
    min_num = 1
    verbose_name = 'Раздел'
    verbose_name_plural = 'Разделы статьи'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ArticleSectionInline]
    list_display = ('title', 'slug', 'published_at', 'display_primary_section')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published_at',)
    search_fields = ('title', 'articlesection__section__name')
    prepopulated_fields = {'slug': ('title',)}

    def display_primary_section(self, obj):
        primary = obj.get_primary_section()
        return primary.name if primary else '—'

    display_primary_section.short_description = 'Основной раздел'

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('articlesection_set__section')

    def save_model(self, request, obj, form, change):
        if not obj.slug:
            obj.slug = slugify(obj.title, allow_unicode=True)
        super().save_model(request, obj, form, change)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}