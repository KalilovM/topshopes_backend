from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers


class CommonRelatedField(serializers.RelatedField):
    model = None
    serializer = None

    def __init__(self, **kwargs):
        self.pk_field = kwargs.pop('pk_field', None)
        super().__init__(**kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if queryset is None and self.model is not None:
            queryset = self.model.objects.all()

        if queryset is None:
            raise Exception('CommonRelated field must provide a `queryset` or `model` argument')

        return queryset

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        if self.serializer is not None:
            return self.serializer(context=self.context).to_representation(value)
