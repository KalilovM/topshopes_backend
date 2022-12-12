from core.mixins import CommonRelatedField
from shops.models import Link, Shop
from shops.serializers import LinkSerializer, ShopSerializer


class ShopRelatedField(CommonRelatedField):
    model = Shop
    serializer = ShopSerializer


class LinkRelatedField(CommonRelatedField):
    model = Link
    serializer = LinkSerializer
