from django.db import models


class UploadJobStatusChoices(models.IntegerChoices):
    PENDING = 1, "Pending"
    IN_PROGRESS = 2, "In Progress"
    SUCCESS = 3, "Success"
    FAILED = 4, "Failed"


class UploadJob(models.Model):
    """Модель для отслеживания задач по загрузке файлов."""

    file = models.FileField(upload_to="uploads/")
    ws_channel = models.CharField(max_length=255, null=True, blank=True)
    status = models.PositiveSmallIntegerField(choices=UploadJobStatusChoices, default=UploadJobStatusChoices.PENDING)
    uploaded_at = models.DateTimeField(auto_now_add=True)
