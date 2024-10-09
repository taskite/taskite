from rest_framework.views import APIView
from django.views import View
from django.core.files.storage import default_storage
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from django.shortcuts import HttpResponse


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, *args, **kwargs):
        file = request.data["file"]
        # Save the file using default storage
        default_storage.save(kwargs.get("file_key"), file)
        # ...
        return Response(status=204)



class UpView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('<html>We are good!</html>')