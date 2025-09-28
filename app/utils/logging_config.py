import logging
import sys

from structlog import wrap_logger, processors


logging.basicConfig(
    format="%(message)s",
    stream=sys.stdout,
    level=logging.DEBUG
)


file_handler = logging.FileHandler("app.log")
file_handler.setFormatter(logging.Formatter("%(message)s"))

base_logger = logging.getLogger("app")
base_logger.addHandler(file_handler)


logger = wrap_logger(
    base_logger,
    processors=[
        processors.TimeStamper(fmt="iso"),
        processors.add_log_level,
        processors.StackInfoRenderer(),
        processors.format_exc_info,
        processors.CallsiteParameterAdder([
                processors.CallsiteParameter.FILENAME,
                processors.CallsiteParameter.FUNC_NAME
            ]
        ),
        processors.JSONRenderer()
    ]
)