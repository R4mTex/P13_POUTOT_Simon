from toolshare import settings


def get_GOOGLE_MAPS_API_KEY(request):
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
    }
