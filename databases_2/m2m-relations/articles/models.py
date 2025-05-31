from django.db import models
from django.core.exceptions import ValidationError


class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название раздела')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='URL-идентификатор')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=256, verbose_name='Название')
    slug = models.SlugField(max_length=256, unique=True, verbose_name='URL-идентификатор', blank=True)
    text = models.TextField(verbose_name='Текст')
    published_at = models.DateTimeField(verbose_name='Дата публикации')
    image = models.ImageField(null=True, blank=True, verbose_name='Изображение',)
    sections = models.ManyToManyField(
        Section,
        through='ArticleSection',
        through_fields=('article', 'section'),
        verbose_name='Разделы',
        default='temp-slug',
    )

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_primary_section(self):
        """Возвращает основной раздел статьи"""
        try:
            return self.articlesection_set.get(is_primary=True).section
        except ArticleSection.DoesNotExist:
            return None

    def get_secondary_sections(self):
        """Возвращает второстепенные разделы в алфавитном порядке"""
        primary_section = self.get_primary_section()
        if primary_section:
            return self.sections.exclude(id=primary_section.id).order_by('name')
        return self.sections.order_by('name')


class ArticleSection(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Статья')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, verbose_name='Раздел')
    is_primary = models.BooleanField(default=False, verbose_name='Основной раздел')

    class Meta:
        verbose_name = 'Раздел статьи'
        verbose_name_plural = 'Разделы статей'
        constraints = [
            models.UniqueConstraint(
                fields=['article', 'is_primary'],
                condition=models.Q(is_primary=True),
                name='unique_primary_section_per_article'
            )
        ]

    def __str__(self):
        return f"{self.article.title} - {self.section.name} ({'основной' if self.is_primary else 'второстепенный'})"

    def clean(self):
        if self.is_primary:
            existing_primary = ArticleSection.objects.filter(
                article=self.article,
                is_primary=True
            ).exclude(pk=self.pk).exists()

            if existing_primary:
                raise ValidationError('Основным может быть только один раздел')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
