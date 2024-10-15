from django.conf import settings

def global_settings(request):
    return {
        "GA_ID": settings.GA_ID,
    }