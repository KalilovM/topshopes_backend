from rest_framework import serializers


class CategoryRelatedField(serializers.RelatedField):
    """
    Relation with category
    Return {id: cat_id, name: cat_name}
    Takes only id
    """

    def to_representation(self, value):
        return {"id": value.id, "name": value.name}

    def to_internal_value(self, data):
        return data
