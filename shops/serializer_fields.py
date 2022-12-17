from rest_framework import serializers


class ProductImageRelationField(serializers.RelatedField):
    """
    Relation in product's image field with Images model
    On create gets list of images
    Return {id, image}
    """

    def to_representation(self, value):
        print(value)
        return True

    def to_internal_value(self, data):
        print(data)
        return data
