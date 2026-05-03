# Python standard libraries
from datetime import timedelta, datetime
# Django libraries
from django.db import models
from django.urls import reverse, reverse_lazy
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify
from django.core.validators import FileExtensionValidator
from ckeditor_uploader.fields import RichTextUploadingField

# External models
from applications.home.models import Book

class Unit(models.Model):

    COLOR_CHOICES = (
        ('red', 'red'),
        ('blue', 'blue'),
        ('yellow', 'yellow'),
        ('green', 'green'),
    )

    name  = models.CharField('Name', max_length=80)
    description  = models.TextField('Description', max_length=200)
    image = models.FileField('Cover', upload_to='book', validators=[FileExtensionValidator(['svg'])])
    color = models.CharField('Color', max_length=20, choices=COLOR_CHOICES)
    exam  = models.FileField('File', upload_to='exams', blank=True)
    book  = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)

    def __str__(self):
       return self.name

class Chapter(models.Model):
    name = models.CharField('Chapter', max_length=50)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, related_name='chapters')

    def __str__(self):
        return self.name

class Section(models.Model):
    title   = models.CharField('Title', max_length=80)
    name    = models.CharField('Name', max_length=50)
    seo_name = models.CharField('Seo Name', max_length=80, blank=True)
    content = RichTextUploadingField('Content')
    slug    = models.SlugField(editable=False, max_length=300, blank=True)
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, related_name='sections')

    def __str__(self): 
        return self.name
    
    # self - instance of our model 
    def get_url(self):
        return reverse('book_app:chapter_section', args=[self.slug])

    def get_absolute_url(self):
        return reverse('book_app:chapter_section', args=[self.slug])

    # Generate the unique url for each section
    def save(self, *args, **kwargs ):
        # current time 
        now = datetime.now()
        total_time = timedelta(
            hours   = now.hour,
            minutes = now.minute,
            seconds = now.second,
        )

        seconds = int(total_time.total_seconds())
        slug_unique = f'{self.seo_name} {str(seconds)}'
        self.slug = slugify(slug_unique)

        super(Section, self).save(*args, **kwargs)

class Resource(models.Model):
    
    TYPE_CHOICES = (
        ('list', 'list'),
        ('slide', 'slide'),
        ('activity', 'activity'),
    )

    name = models.CharField("Name", max_length=60)
    file = models.FileField('File', upload_to='files')
    file_type = models.CharField("File Type", max_length=15, choices=TYPE_CHOICES)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='resources', null=True)
