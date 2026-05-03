from django.shortcuts import get_object_or_404, render
# Local models
from .models import Section

# Create your views here.

# Retrieve the section by the given id that was sent in the URL
def viewSection(request, section_slug):
    section = get_object_or_404(
        Section.objects.select_related('chapter__unit'),
        slug=section_slug,
        chapter__isnull=False,
        chapter__unit__isnull=False,
    )
    unit = section.chapter.unit
    color = unit.color
    exam = unit.exam

    options = {
        '1': 'I',
        '2': 'II',
        '3': 'III',
        '4': 'IV',
    } 

    chapters = unit.chapters.all()

    context = {
        'chapters': chapters,
        'section': section,
        'color': color,
        'id': options.get(str(unit.id), str(unit.id)),
        'exam': exam,   
    }

    return render(request, 'book/section.html', context=context)
