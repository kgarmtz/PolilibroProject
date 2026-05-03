# Declaring the global variables that we want to display in the whole application
from .models import Unit, Chapter, Section

# Context processor function 
def units_list(request):
    # Fetching all the units from our database 
    units = Unit.objects.all()

    # Return a context dictionary
    return {
        'units': units,
    }