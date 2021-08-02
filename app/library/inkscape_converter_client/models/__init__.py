# flake8: noqa

# import all models into this package
# if you have many models here with many references from one model to another this may
# raise a RecursionError
# to avoid this, import only the models that you directly need like:
# from from app.library.inkscape_converter_client.model.pet import Pet
# or import this package, but before doing it, use:
# import sys
# sys.setrecursionlimit(n)

from app.library.inkscape_converter_client.model.conversion_request import (
    ConversionRequest,
)
from app.library.inkscape_converter_client.model.conversion_response import (
    ConversionResponse,
)
from app.library.inkscape_converter_client.model.http_validation_error import (
    HTTPValidationError,
)
from app.library.inkscape_converter_client.model.validation_error import ValidationError
