import time 
import inspect
from functools import wraps

from PIL import Image
from io import BytesIO

from app.logging_config import logger


def resize_image_bytes(image_bytes: bytes, max_size: tuple = (1024, 1024)) -> bytes:
    img = Image.open(BytesIO(image_bytes))
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    buf = BytesIO()

    fmt = img.format if img.format else "PNG"
    if fmt.upper() in ["JPEG", "JPG"]:
        img.save(buf, format=fmt, quality=85)
    else:
        img.save(buf, format=fmt)
    
    res = buf.getvalue()
    logger.info("image_resized")
    return res



def log_func(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()

        logger.info("Function started", func_name=func.__qualname__)

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start
        logger.info("Function enede", func_name=func.__qualname__, time_needed=elapsed)
        return result
    return wrapper
