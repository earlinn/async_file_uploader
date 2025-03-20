import uuid

from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from file_uploader.models import UploadJob
from file_uploader.serializers import FileUploadSerializer
from file_uploader.tasks import process_file_task


class FileUploadAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = FileUploadSerializer(data=request.data, context={"request": request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        files = serializer.validated_data["files"]
        ws_channel = serializer.validated_data.get("ws_channel") or str(uuid.uuid4())

        jobs = []
        for f in files:
            job = UploadJob.objects.create(file=f, ws_channel=ws_channel)
            jobs.append(job.pk)
            process_file_task.delay(job.pk)
        return Response({"jobs": jobs, "ws_channel": ws_channel, "status": "queued"}, status=status.HTTP_202_ACCEPTED)
