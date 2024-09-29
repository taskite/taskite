from celery import shared_task
from datetime import datetime

from taskite.models import PurgedAsset, UnusedAsset


@shared_task
def purge_asset(key, timestamp_str):
    try:
        PurgedAsset.objects.create(
            key=key, purged_at=datetime.fromisoformat(timestamp_str)
        )
    except Exception as e:
        print(e)


@shared_task
def remove_unused_asset(key):
    asset = UnusedAsset.objects.filter(key=key).first()
    if not asset:
        print("Asset not found")
    else:
        asset.delete()
