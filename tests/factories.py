import factory
from django.core.files.base import ContentFile
from faker import Factory

from shops.models import Product, Shop, Color, Size, Category, Brand, BrandType, Image
from users.models import Customer, Address

faker = Factory.create()


class CustomerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Customer


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    user = factory.SubFactory(CustomerFactory)


class BrandTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BrandType


class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    type = factory.SubFactory(BrandTypeFactory)


class ColorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Color


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    parent = factory.SubFactory('tests.factories.CategoryFactory', parent=None)



class SizeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Size


class ShopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Shop

    user = factory.SubFactory(CustomerFactory)
    cover_picture = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
    profile_picture = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    shop = factory.SubFactory(ShopFactory)
    brand = factory.SubFactory(BrandFactory)
    thumbnail = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # simple build do nothing
            return
        if extracted:
            # A list of groups were passed in, use them
            print(extracted)
            for category in extracted:
                self.categories.add(category)

    @factory.post_generation
    def sizes(self, create, extracted, **kwargs):
        if not create:
            # simple build do nothing
            return
        if extracted:
            # A list of groups were passed in, use them
            for size in extracted:
                self.sizes.add(size)

    @factory.post_generation
    def colors(self, create, extracted, **kwargs):
        if not create:
            # simple build do nothing
            return
        if extracted:
            # A list of groups were passed in, use them
            for color in extracted:
                self.colors.add(color)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    image = factory.django.ImageField(color="blue")
    product = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )
