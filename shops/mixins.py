from rest_framework import serializers


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
