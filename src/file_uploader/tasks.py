import logging
import time

from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from file_uploader.models import UploadJob, UploadJobStatusChoices


@shared_task
def process_file_task(job_id: int) -> None:
    job: UploadJob = UploadJob.objects.get(pk=job_id)
    job.status = UploadJobStatusChoices.IN_PROGRESS
    job.save()

    try:
        logging.info(f"Processing file `{job.file}`")
        time.sleep(5)  # какая-то обработка файла
        job.status = UploadJobStatusChoices.SUCCESS

        # WebSocket уведомление
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            job.ws_channel,
            {
                "type": "upload_job_status",
                "job_id": job.id,
                "status": job.status,
            },
        )

    except Exception as err:
        job.status = UploadJobStatusChoices.FAILED
        logging.error(str(err))

    finally:
        job.save()
