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