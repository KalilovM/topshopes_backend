from rest_framework import serializers


# TODO: rename it
class ProductImageRelationField(serializers.RelatedField):
    """
    Relation in product's image field with Images model
    On create gets list of images
    Return {id, image}
    """

    def to_representation(self, value):
        try:
            return {
                "id": value.id,
                "image": value.image.url,
            }
        except AttributeError:
            self.fail("invalid data")

    def to_internal_value(self, data):
        return data
