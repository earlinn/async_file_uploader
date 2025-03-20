from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    files = serializers.ListField(child=serializers.FileField(), allow_empty=False)
    ws_channel = serializers.CharField(required=False)
