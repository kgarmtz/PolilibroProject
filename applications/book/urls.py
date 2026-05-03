from django.urls import path
from . import views

app_name = 'book_app'

urlpatterns = [
    path('seccion/<slug:section_slug>/', views.viewSection, name='chapter_section')
]