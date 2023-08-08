from django.core.cache import cache

def increment_like_count(request, post_id):
    # Check if the like count is already cached
    cache_key = f'post_{post_id}_like_count'
    like_count = cache.get(cache_key)

    if like_count is None:
        # If not cached, retrieve the like count from the database
        post = Post.objects.get(id=post_id)
        like_count = post.like_count

        # Cache the like count
        cache.set(cache_key, like_count)

    # Increment the like count
    like_count += 1

    # Update the like count in the database
    post.like_count = like_count
    post.save()

    # Update the cached like count
    cache.set(cache_key, like_count)

    # Return a response
    return HttpResponse(f'Like count: {like_count}')
