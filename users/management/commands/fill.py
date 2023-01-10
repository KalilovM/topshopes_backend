import itertools
import os
import random

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from faker import Faker

from attributes.models import Attribute, AttributeValue
from orders.models import Order
from products.models import (Brand, BrandType, Category, Image, Product,
                             ProductVariant)
from reviews.models import Review
from shops.models import Link, Shop
from users.models import Address, Customer

DJANGO_SETTINGS_MODULE = "core.settings"
image_path = "tests/img/"
image_list = os.listdir(image_path)
image_list = [image_path + image for image in image_list]
fake: Faker = Faker()

# run project with command: python manage.py fill_dummy --delete
# create process done loading data


class Command(BaseCommand):
    help = "Fill database with dummy data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete all data in database",
        )

    def handle(self, *args, **options):
        if options["delete"]:
            self.stdout.write("Deleting all data in database")
            Customer.objects.all().delete()
            Address.objects.all().delete()
            Shop.objects.all().delete()
            BrandType.objects.all().delete()
            Brand.objects.all().delete()
            Category.objects.all().delete()
            Product.objects.all().delete()
            Order.objects.all().delete()
            Link.objects.all().delete()
            Image.objects.all().delete()
            Review.objects.all().delete()
            self.stdout.write("All data deleted")
        else:
            self.stdout.write("Filling database with dummy data")
            self.stdout.write("Filling customer")
            fill_customer()
            self.stdout.write("Filling address")
            fill_address()
            self.stdout.write("Filling brand type")
            fill_brand_type()
            self.stdout.write("Filling brand")
            fill_brand()
            self.stdout.write("Filling category")
            fill_category()
            self.stdout.write("Filling shop")
            fill_shop()
            self.stdout.write("Filling product")
            fill_product()
            self.stdout.write("Filling image")
            fill_image()
            self.stdout.write("Filling order")
            fill_order()
            self.stdout.write("Filling link")
            fill_link()
            self.stdout.write("Creating superuser and user")
            fill_basic_data()
            # fill_review()
            self.stdout.write("Database filled with dummy data")


def fill_basic_data():
    # create superuser
    admin = Customer.objects.create_superuser(
        email="admin@gmail.com",
        password="admin",
    )
    # create user
    user = Customer.objects.create_user(
        email="client@gmail.com",
        password="client",
    )

    Address.objects.create(
        user=Customer.objects.get(email="client@gmail.com"),
        city="Moscow",
        country="Russia",
        street="Lenina",
        phone="+7 999 999 99 99 00",
    )

    Address.objects.create(
        user=Customer.objects.get(email="admin@gmail.com"),
        city="Moscow",
        country="Russia",
        street="Lenina",
        phone="+7 999 999 99 99 00",
    )

    admin_shop = Shop.objects.create(
        name="Admin's Shop",
        user=Customer.objects.get(email="admin@gmail.com"),
        address="Moscow, Lenina",
        phone="+7 999 999 99 99 00",
        email="adminshop@gmail.com",
        cover_picture=SimpleUploadedFile(
            name="cover.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
        profile_picture=SimpleUploadedFile(
            name="profile.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )
    Shop.objects.create(
        name="Client's Shop",
        user=Customer.objects.get(email="client@gmail.com"),
        address="Moscow, Lenina",
        phone="+7 999 999 99 99",
        email="client@gmail.com",
        cover_picture=SimpleUploadedFile(
            name="cover.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
        profile_picture=SimpleUploadedFile(
            name="profile.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )

    product = Product.objects.create(
        name="Product",
        brand=Brand.objects.first(),
        shop=admin_shop,
        category=Category.objects.first(),
        rating=5,
    )

    variant = ProductVariant.objects.create(
        product=product,
        price=100,
        status="available",
        discount=0,
        stock=100,
        thumbnail=SimpleUploadedFile(
            name="product.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )

    product2 = Product.objects.create(
        name="Product2",
        brand=Brand.objects.first(),
        category=Category.objects.first(),
        shop=admin_shop,
        rating=5,
    )

    variant2 = ProductVariant.objects.create(
        product=product2,
        stock=100,
        price=100,
        status="available",
        discount=0,
        thumbnail=SimpleUploadedFile(
            name="product.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )

    Image.objects.create(
        product_variant=variant,
        image=SimpleUploadedFile(
            name="product.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )
    Image.objects.create(
        product_variant=variant2,
        image=SimpleUploadedFile(
            name="product.webp",
            content=open(
                image_list[random.randint(0, len(image_list) - 1)], "rb"
            ).read(),
            content_type="image/webp",
        ),
    )
    Order.objects.create(
        user=user,
        shop=admin_shop,
        quantity=1,
        product_variant=variant,
        address=user.addresses.first(),
        status="Pending",
    )

    Order.objects.create(
        user=user,
        shop=admin_shop,
        quantity=3,
        product_variant=variant2,
        address=user.addresses.first(),
        status="Pending",
    )


def fill_customer():
    for _ in range(22):
        Customer.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )


def fill_address():
    users = Customer.objects.all()
    for _ in range(Customer.objects.count()):
        for _ in range(random.randint(1, 3)):
            Address.objects.create(
                user=users[_],
                country=fake.country(),
                city=fake.city(),
                street=fake.street_name(),
                phone=fake.phone_number(),
            )


def fill_shop():

    for _ in range(3):
        user = Customer.objects.all()[_]
        # set user only unique user
        Shop.objects.create(
            name=fake.company(),
            user=user,
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.email(),
            cover_picture=fake.image_url(),
            profile_picture=fake.image_url(),
        )


COLORS = {
    "red": "#FF0000",
    "green": "#008000",
    "blue": "#0000FF",
    "yellow": "#FFFF00",
    "orange": "#FFA500",
    "purple": "#800080",
    "pink": "#FFC0CB",
    "brown": "#A52A2A",
    "black": "#000000",
    "white": "#FFFFFF",
    "gray": "#808080",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "violet": "#EE82EE",
    "indigo": "#4B0082",
    "turquoise": "#40E0D0",
    "cyan": "#00FFFF",
    "magenta": "#FF00FF",
    "lime": "#00FF00",
    "maroon": "#800000",
    "navy": "#000080",
}


SIZES = [
    "XXXS",
    "XXS",
    "XS",
    "S",
    "M",
    "L",
    "XL",
    "XXL",
    "XXXL",
    "XXXXL",
]


LINK_NAMES = [
    "Facebook",
    "Instagram",
    "Telegram",
    "Twitter",
    "Youtube",
    "TikTok",
    "Pinterest",
    "Linkedin",
    "Reddit",
    "VK",
]


def fill_link():
    for _ in range(10):
        Link.objects.create(
            name=fake.random_element(LINK_NAMES),
            link=fake.url(),
            shop=fake.random_element(Shop.objects.all()),
        )


PRODUCT_TITLES = [
    "T-shirt",
    "Shirt",
    "Pants",
    "Jeans",
    "Shorts",
    "Skirt",
    "Dress",
    "Jacket",
    "Coat",
    "Sweater",
    "Sweatshirt",
    "Blouse",
    "Shoes",
    "Boots",
    "Sneakers",
    "Sandals",
    "Slippers",
    "Hat",
    "Gloves",
    "Scarf",
    "Belt",
    "Backpack",
    "Wallet",
    "Bag",
    "Watch",
    "Orbital Keys",
    "XPress Bottle",
    "InstaPress",
    "Uno Wear",
    "Allure Kit",
    "Swish Wallet",
    "Onovo Supply",
    "Sharpy Knife",
    "Towlee",
    "Rhino Case",
    "Mono",
    "Handy Mop",
    "ONEset",
    "Vortex Bottle",
    "Terra Shsave",
    "Gymr Kit",
    "Villafy",
    "Stickem",
    "Snap It",
    "Scruncho",
]

UNITS = [
    "kg",
    "g",
    "l",
    "ml",
    "m",
    "cm",
    "mm",
    "pcs",
]


attr_names = ["color", "size"]


def fill_product():
    shop_names = [shop.name for shop in Shop.objects.all()]
    combinations = itertools.product(shop_names, PRODUCT_TITLES)
    for combination in combinations:
        product = Product.objects.create(
            name=combination[1],
            brand=fake.random_element(Brand.objects.all()),
            shop=Shop.objects.get(name=combination[0]),
            category=fake.random_element(Category.objects.all()),
            unit=fake.random_element(UNITS),
        )
    for _ in range(Product.objects.count()):
        product = Product.objects.all()[_]
        for _ in range(random.randint(1, 6)):
            variant = ProductVariant.objects.create(
                product=product,
                status=ProductVariant.STATUS_CHOICES[
                    random.randint(0, len(ProductVariant.STATUS_CHOICES) - 1)
                ][0],
                price=fake.random_int(min=1000, max=10000),
                stock=fake.random_int(min=20, max=100),
                discount=fake.random_int(min=0, max=100),
                thumbnail=SimpleUploadedFile(
                    image_list[_],
                    open(
                        image_list[random.randint(0, len(image_list) - 1)], "rb"
                    ).read(),
                    content_type="image/webp",
                ),
            )
            attribute = product.category.attributes.all()
            for i in attribute:
                if i.name == "color":
                    AttributeValue.objects.create(
                        attribute=i,
                        value=fake.random_element(COLORS.keys()),
                        product_variant=variant,
                    )
                elif i.name == "size":
                    AttributeValue.objects.create(
                        attribute=i,
                        value=fake.random_element(SIZES),
                        product_variant=variant,
                    )


def fill_image():
    for _ in range(ProductVariant.objects.count()):
        product = ProductVariant.objects.all()[_]
        for _ in range(random.randint(1, 5)):
            Image.objects.create(
                image=SimpleUploadedFile(
                    image_list[_],
                    open(
                        image_list[random.randint(0, len(image_list) - 1)], "rb"
                    ).read(),
                    content_type="image/webp",
                ),
                product_variant=product,
            )


BRAND_NAMES = [
    "Adidas",
    "Nike",
    "Puma",
    "Reebok",
    "New Balance",
    "Asics",
    "Vans",
    "Converse",
    "Fila",
    "Under Armour",
    "H&M",
    "Zara",
    "Bershka",
    "Pull&Bear",
    "Stradivarius",
    "Mango",
    "Hollister",
]


def fill_brand():
    for _ in range(10):
        brandtype = BrandType.objects.all()[_]
        name = BRAND_NAMES[_]
        Brand.objects.create(
            name=name,
            image=fake.image_url(),
            type=brandtype,
            featured=fake.pybool(),
        )


CATEGORY_NAMES = [
    "Food",
    "Fashion",
    "Beauty",
    "Sports",
    "Kids",
    "Pets",
    "Toys",
    "Books",
    "Stationery",
    "Tools",
    "Garden",
    "Automotive",
    "Health",
    "Baby",
    "Travel",
    "Jewelry",
    "Watches",
    "Shoes",
    "Bags",
    "Accessories",
    "Furniture",
    "Decor",
    "Art",
    "Music",
    "Movies",
    "Games",
    "Software",
    "Outdoors",
    "Grocery",
    "Home",
    "Industrial",
    "Electronics",
    "Computers",
    "Office",
    "Camera",
    "Video",
    "TV",
    "Audio",
    "Cell Phones",
    "Clothing",
    "Handbags",
    "Luggage",
]
SUB_CATEGORY_NAMES = [
    "Domestic",
    "International",
    "Local",
    "Foreign",
    "National",
    "Global",
    "Chinese",
    "English",
    "French",
    "German",
    "Italian",
    "Japanese",
    "Korean",
    "Russian",
    "Spanish",
]


def fill_category():
    for _ in range(10):
        name = CATEGORY_NAMES[_]
        sub_name = SUB_CATEGORY_NAMES[_]
        category = Category.objects.create(
            name=name,
            icon=fake.image_url(),
            image=fake.image_url(),
            description=fake.text(),
            featured=fake.pybool(),
            tax=fake.random_int(min=0, max=100),
        )
        for _ in range(2):
            attribute = Attribute.objects.create(name=attr_names[_])
            category.attributes.add(attribute)

        if _ % 2 == 0:
            parent = fake.random_element(Category.objects.all())
            Category.objects.create(
                name=sub_name,
                icon=fake.image_url(),
                image=fake.image_url(),
                description=fake.text(),
                featured=fake.pybool(),
                parent=parent,
                tax=parent.tax,
            )


BRANDTYPE_NAME = [
    "Digital",
    "Fashion",
    "Food",
    "Home",
    "Electronics",
    "Beauty",
    "Sports",
    "Kids",
    "Pets",
    "Toys",
]


def fill_brand_type():
    for _ in range(10):
        BrandType.objects.create(
            name=BRANDTYPE_NAME[_],
        )


# def fill_review():
#     for _ in range(10):
#         Review.objects.create(
#             text=fake.text(),
#             rating=fake.pyint(),
#             product=Product.objects.order_by("?").first(),
#         )


def fill_order():
    indexes = [i[0] for i in Order.STATUSES]
    for _ in range(3):
        customer = Customer.objects.all()[_]
        shop = Shop.objects.all()[2 - _]
        Order.objects.create(
            user=customer,
            quantity=fake.random_int(min=1, max=10),
            product_variant=ProductVariant.objects.order_by("?").first(),
            address=customer.addresses.first(),
            shop=shop,
            status=fake.random_element(indexes),
        )
