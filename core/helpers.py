import os
import uuid
from datetime import datetime
from django.utils.deconstruct import deconstructible
from rest_framework import serializers


@deconstructible
class PathAndRename:
    """
    Class to rename image to uuid4 and save it
    Returns path to image
    """

    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        ext = filename.split(".")[-1]
        filename = f"{uuid.uuid4().hex}.{ext}"

        def make_path(path):
            now = datetime.now()
            return os.path.join(path, f"{now.year}/{now.month}")

        date_path = make_path(self.sub_path)
        full_path = os.path.join(date_path, filename)

        return full_path


class ImageUrlField(serializers.RelatedField):
    """
    IDK
    """

    def to_representation(self, value):
        url = value.image.url
        request = self.context.get("request", None)
        if request is not None:
            return request.build_absolute_uri(url)
        return url
