from ecommerce.models import Category, Brand, Product

# Assurez-vous d'avoir déjà créé des catégories et des marques, ou utilisez des données factices pour ces champs.

# Récupérez une catégorie et une marque existantes (ou créez-les si elles n'existent pas encore)
category_smartphones = Category.objects.get(name="Smartphones")
brand_samsung = Brand.objects.get(name="Samsung")
category_laptops = Category.objects.get(name="Ordinateurs portables")
brand_apple = Brand.objects.get(name="Apple")
category_tablets = Category.objects.get(name="Tablettes")
brand_lenovo = Brand.objects.get(name="Lenovo")
category_cameras = Category.objects.get(name="Appareils photo")
brand_canon = Brand.objects.get(name="Canon")
category_tv = Category.objects.get(name="Téléviseurs")
brand_sony = Brand.objects.get(name="Sony")

# Créez 5 produits supplémentaires
products_data = [
    {
        "category": category_smartphones,
        "name": "iPhone 13 Pro",
        "image": "product_images/iphone_13_pro.jpg",
        "description": "Le dernier iPhone avec des fonctionnalités exceptionnelles.",
        "brand": brand_apple,
        "price": 999999,  # Prix en FCFA
        "promo_price": 899999,  # Prix promo en FCFA
        "in_promo": True,
        "is_vedette": True,
        "in_stock": True,
        "is_new": True,
        "stock_count": 30,
        "specification": "6.1-inch Super Retina XDR display, A15 Bionic chip, 6GB RAM",
        "warranty_info": "Garantie Apple d'un an",
        "display": "6,1 pouces Super Retina XDR",
        "processor_capacity": "A15 Bionic",
        "camera_quality": "Triple caméra 12 MP",
        "memory": "6 Go de RAM",
        "harddisk_capacity": "256 Go",
        "graphics": "Apple GPU",
    },
    {
        "category": category_laptops,
        "name": "MacBook Air M2",
        "image": "product_images/macbook_air_m2.jpg",
        "description": "L'ordinateur portable ultra-léger d'Apple avec une puce M2 puissante.",
        "brand": brand_apple,
        "price": 1299999,  # Prix en FCFA
        "promo_price": None,
        "in_promo": False,
        "is_vedette": True,
        "in_stock": True,
        "is_new": True,
        "stock_count": 20,
        "specification": "13.3-inch Retina display, Apple M2 chip, 16GB RAM",
        "warranty_info": "Garantie Apple d'un an",
        "display": "13,3 pouces Retina",
        "processor_capacity": "Apple M2",
        "camera_quality": None,
        "memory": "16 Go de RAM",
        "harddisk_capacity": "512 Go",
        "graphics": "Apple GPU",
    },
    {
        "category": category_tablets,
        "name": "Lenovo Tab P11",
        "image": "product_images/lenovo_tab_p11.jpg",
        "description": "Tablette Android polyvalente avec un écran magnifique.",
        "brand": brand_lenovo,
        "price": 349999,  # Prix en FCFA
        "promo_price": 299999,  # Prix promo en FCFA
        "in_promo": True,
        "is_vedette": True,
        "in_stock": True,
        "is_new": True,
        "stock_count": 40,
        "specification": "11-inch 2K display, Qualcomm Snapdragon 662, 4GB RAM",
        "warranty_info": "Garantie Lenovo de 2 ans",
        "display": "11 pouces 2K",
        "processor_capacity": "Qualcomm Snapdragon 662",
        "camera_quality": "Caméra arrière 13 MP",
        "memory": "4 Go de RAM",
        "harddisk_capacity": "64 Go",
        "graphics": "Adreno 610",
    },
    {
        "category": category_cameras,
        "name": "Canon EOS 90D",
        "image": "product_images/canon_eos_90d.jpg",
        "description": "Appareil photo reflex numérique pour les photographes enthousiastes.",
        "brand": brand_canon,
        "price": 1499999,  # Prix en FCFA
        "promo_price": None,
        "in_promo": False,
        "is_vedette": True,
        "in_stock": True,
        "is_new": True,
        "stock_count": 15,
        "specification": "32.5 MP APS-C sensor, 4K video recording, Dual Pixel AF",
        "warranty_info": "Garantie Canon de 1 an",
        "display": "N/A",
        "processor_capacity": "N/A",
        "camera_quality": "32.5 MP",
        "memory": "N/A",
        "harddisk_capacity": "N/A",
        "graphics": "N/A",
    },
    {
        "category": category_tv,
        "name": "Sony Bravia X900H",
        "image": "product_images/sony_bravia_x900h.jpg",
        "description": "Téléviseur 4K HDR avec des couleurs éclatantes et un son immersif.",
        "brand": brand_sony,
        "price": 799999,  # Prix en FCFA
        "promo_price": 749999,  # Prix promo en FCFA
        "in_promo": True,
        "is_vedette": True,
        "in_stock": True,
        "is_new": True,
        "stock_count": 25,
        "specification": "55-inch 4K HDR display, Dolby Atmos audio, Android TV",
        "warranty_info": "Garantie Sony de 1 an",
        "display": "55 pouces 4K HDR",
        "processor_capacity": "N/A",
        "camera_quality": "N/A",
        "memory": "N/A",
        "harddisk_capacity": "N/A",
        "graphics": "N/A",
    },
]

for data in products_data:
    Product.objects.create(**data)

# Vérification des produits créés
products = Product.objects.all()
for product in products:
    print(f"Produit créé : {product.name}")
