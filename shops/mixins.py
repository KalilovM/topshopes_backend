from rest_framework import serializers


class CategoryRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return {"id": value.id, "name": value.name}
