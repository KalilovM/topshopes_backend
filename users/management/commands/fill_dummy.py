from orders.models import Order, OrderItem
from django.core.management.base import BaseCommand
from faker import Faker
import random
from users.models import Customer, Address
from shops.models import (
    Shop,
    Color,
    Size,
    Link,
    Product,
    Image,
    Brand,
    Category,
    BrandType,
    Review,
)

DJANGO_SETTINGS_MODULE = "core.settings"

fake: Faker = Faker()

# run project with command: python manage.py fill_dummy --delete


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
            OrderItem.objects.all().delete()
            Link.objects.all().delete()
            Color.objects.all().delete()
            Size.objects.all().delete()
            Image.objects.all().delete()
            Review.objects.all().delete()
            self.stdout.write("All data deleted")
        else:
            self.stdout.write("Filling database with dummy data")
            fill_customer()
            fill_address()
            fill_brand_type()
            fill_brand()
            fill_category()
            fill_color()
            fill_size()
            fill_shop()
            fill_product()
            fill_image()
            fill_order()
            fill_order_item()
            fill_link()
            # fill_review()
            self.stdout.write("Database filled with dummy data")


def fill_customer():
    for _ in range(22):
        Customer.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
        )


def fill_address():
    users = random.choices(Customer.objects.all(), k=10)
    for _ in range(10):
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


def fill_color():
    names = list(COLORS.keys())
    colors = list(COLORS.values())
    for _ in range(10):
        Color.objects.create(
            name = names[_],
            color = colors[_],
        )


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


def fill_size():

    for _ in range(10):
        Size.objects.create(name=fake.random_element(SIZES))


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


def fill_product():
    indexes = [i[0] for i in Product.STATUSES]
    for _ in range(10):
        product = Product.objects.create(
            title=fake.random_element(PRODUCT_TITLES),
            brand=fake.random_element(Brand.objects.all()),
            shop=fake.random_element(Shop.objects.all()),
            price=fake.pyint(),
            status=fake.random_element(indexes),
            rating=fake.pyint(),
            unit=fake.random_element(UNITS),
            discount=fake.pyint(),
            thumbnail=fake.image_url(),
        )
        product.colors.set(fake.random_elements(Color.objects.all()))
        product.sizes.set(fake.random_elements(Size.objects.all()))
        product.categories.set(fake.random_elements(Category.objects.all()))
        product.colors.set(fake.random_elements(Color.objects.all()))
        product.colors.set(fake.random_elements(Color.objects.all()))
        product.sizes.set(fake.random_elements(Size.objects.all()))
        product.categories.set(fake.random_elements(Category.objects.all()))
        product.sizes.set(fake.random_elements(Size.objects.all()))
        product.categories.set(fake.random_elements(Category.objects.all()))
        product.save()


def fill_image():
    for _ in range(10):
        Image.objects.create(
            image=fake.image_url(),
            product=fake.random_element(Product.objects.all()),
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
        Category.objects.create(
            name=name,
            icon=fake.image_url(),
            image=fake.image_url(),
            description=fake.text(),
            featured=fake.pybool(),
        )

        if _ % 2 == 0:
            Category.objects.create(
                name=sub_name,
                icon=fake.image_url(),
                image=fake.image_url(),
                description=fake.text(),
                featured=fake.pybool(),
                parent=fake.random_element(Category.objects.all()),
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
            shop=shop,
            tax=fake.pyint(),
            discount=fake.pyint(),
            status=fake.random_element(indexes),
        )


def fill_order_item():
    for _ in range(10):
        OrderItem.objects.create(
            product_image=fake.image_url(),
            product_name=fake.random_element(PRODUCT_TITLES),
            product_price=fake.pyint(),
            product_quantity=fake.pyint(),
            order=fake.random_element(Order.objects.all()),
        )
