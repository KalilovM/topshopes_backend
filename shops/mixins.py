from rest_framework import serializers

from shops.models import Brand


class CustomRelatedField(serializers.RelatedField):
    """
    Relation with model
    Return {id: model_id, name: model_name}
    Takes only id
    """

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

    def to_internal_value(self, data):
        return data


class CustomRelatedFieldWithImage(CustomRelatedField):
    """
    Same as CustomRelatedField
    Return {id:model_id, name:model_name, image:model_image}
    """

    def to_representation(self, value):
        request = self.context.get("request", None)
        if request is not None:
            image = request.build_absolute_uri(value.image.url)
        else:
            raise ValueError
        return {"id": value.id, "name": value.name, "image": image}

    def to_internal_value(self, data: str):
        try:
            return Brand.objects.get(pk=data)
        except ValueError:
            raise ValueError
