import time


def log_time(func):
    def wrapper(*args, **kwargs):
        print(f"Executing {func.__name__} method...")
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        print(f"{func.__name__} method execution time: {time_taken} seconds.")
        return result
    return wrapper