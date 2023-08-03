from src.flask_files.redis_util import redis_client

client = redis_client.get_client()


def increment_view_count(recipe_id, recipe_name):
    client.zincrby('trending_pages', 1, recipe_id)

    if not client.exists(recipe_id):
        client.set(recipe_id, recipe_name)


def get_trending_recipes():
    trending_recipes_data = client.zrevrange('trending_pages', 0, 2, withscores=True)

    results = []

    for data in trending_recipes_data:

        results.append({
            'id': data[0].decode(),
            'views': data[1],
            'title': client.get(data[0]).decode()
        })

    return results


def clear_cache():
    client.flushdb()
