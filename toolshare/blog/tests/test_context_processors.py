from toolshare import settings, context_processors

# Create your tests here.
def test_context_processors(request):
   assert context_processors.get_GOOGLE_MAPS_API_KEY(request) == {'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,}