from .models import Property
from django.core.cache import cache
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def get_all_properties():
    properties = cache.get('all_properties')
    if properties is None:
        properties = list(Property.objects.all().values(
            'id', 'title', 'description', 'price', 'location', 'created_at'
        ))
        cache.set('all_properties', properties, timeout=3600)
    return properties


def get_redis_cache_metrics():
    redis_con = get_redis_connection('defualt')
    info = redis_con.info

    hits = info.get('keyspace_hits', 0)
    misses = info.get('keyspace_misses', 0)
    total = hits + misses
    hit_ratio = (hits / total)

    metrics = {
        "keyspace_hits": hits,
        "keyspace_misses": misses,
        "hit_ratio": round(hit_ratio, 4) if hit_ratio is not None else "N/A"
    }

    logger.info(f"Redis Cache Metrics: {metrics}")
    return metrics
