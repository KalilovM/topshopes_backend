from core.mixins import CommonRelatedField
from users.models import Customer
from users.serializers import CustomerSerializer

# think about common related fields
class CustomerRelatedField(CommonRelatedField):
    model = Customer
    serializer = CustomerSerializer
