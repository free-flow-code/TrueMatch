import math
from fastapi_cache import FastAPICache


def great_circle_distance(lat1, lon1, lat2, lon2) -> float:
    earth_radius = 6371  # Радиус Земли в километрах
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c


async def filter_by_distance(clients, user_id, user_lat, user_lon, max_distance) -> list:
    filtered_clients = []
    redis = FastAPICache.get_backend().redis

    for client in clients:
        if not client.lat or not client.lon:
            continue

        cache_key1 = f"{user_id}-{client.id}"
        cache_key2 = f"{client.id}-{user_id}"

        if await redis.exists(cache_key1):
            distance = await redis.get(cache_key1)
        elif await redis.exists(cache_key2):
            distance = await redis.get(cache_key2)
        else:
            distance = great_circle_distance(user_lat, user_lon, client.lat, client.lon)
            await redis.set(cache_key1, distance, ex=3600)  # Кэшируем на 1 час

        if float(distance) <= max_distance:
            filtered_clients.append(client)
    return filtered_clients
