# Python packages
from datetime import timedelta, datetime
# Django packages
from django.contrib.sitemaps import Sitemap
from django.urls import reverse_lazy
# External models 
from applications.book.models import Section

# Creating a sitemap for the model 
class SectionSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Section.objects.all()

    # Sorting the url by chronological creation order
    
class Sitemap(Sitemap):
    protocol = 'https'

    def __init__(self, names):
        self.names = names
    
    def items(self):
        return self.names
    
    def changefreq(self, obj):
        return 'monthly'

    def lastmod(self, obj):
        return datetime.now()
    
    def location(self, obj):
        return reverse_lazy(obj)
