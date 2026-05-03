from django.db import models
from django.core.validators import FileExtensionValidator
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Book(models.Model):
    title        = models.CharField('Title', max_length=50)
    image        = models.FileField('Cover', upload_to='book', validators=[FileExtensionValidator(['svg'])])
    description  = models.TextField('Description', max_length=200)
    about          = RichTextField('About')
    organization   = RichTextField('Organization')
    about_sections = RichTextField('About Section', blank=True)
     
    def __str__(self):
        return self.title