from functools import wraps


def synchronized(lock):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(*args, **kwargs):
            async with lock:
                return await fn(*args, **kwargs)

        return wrapper

    return decorator
