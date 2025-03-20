from django.contrib import admin

from file_uploader.models import UploadJob


@admin.register(UploadJob)
class UploadJobAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "status", "uploaded_at")
    list_filter = ("status",)
    search_fields = ("file",)
    readonly_fields = ("uploaded_at",)
