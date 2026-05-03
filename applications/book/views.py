from django.shortcuts import render
# Local models
from .models import Section, Unit

# Create your views here.

# Retrieve the section by the given id that was sent in the URL
def viewSection(request, section_slug):
    section = Section.objects.get(slug=section_slug)
    color = section.chapter.unit.color
    unit = Unit.objects.filter(color=color)[0]
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
        'id': options[str(unit.id)],
        'exam': exam,   
    }

    return render(request, 'book/section.html', context=context)