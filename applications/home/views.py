from django.shortcuts import render
# Local models
from .models import Book
# External models
from applications.book.models import Unit

# Create your views here.
def home(request):
    book  = Book.objects.first()
    units = Unit.objects.prefetch_related('chapters__sections') 
    unit_section = []

    for unit in units:
        chapter = unit.chapters.first()
        if chapter is None:
            continue

        section = chapter.sections.first()
        if section is None:
            continue

        unit_section.append( (unit, section) )
    
    # Declarte the context dictionary to send data to our template
    context = {
        'book': book,
        'unit_section': unit_section,
    }

    return render(request, 'home/index.html', context) 
