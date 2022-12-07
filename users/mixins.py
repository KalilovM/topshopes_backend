from core.mixins import CommonRelatedField
from users.models import Customer
from users.serializers import CustomerSerializer


class CustomerRelatedField(CommonRelatedField):
    model = Customer
    serializer = CustomerSerializer
