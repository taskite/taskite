from django.views import View
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.shortcuts import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, *args, **kwargs):
        file = request.data["file"]
        # Inititate a cache storage
        cache_storage = FileSystemStorage(
            location=settings.CACHE_MEDIA_ROOT, base_url=settings.MEDIA_URL
        )
        # Save the file using cache storage
        cache_storage.save(kwargs.get("file_key"), file)
        return Response(status=204)


class UpView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("<html>We are good!</html>")
