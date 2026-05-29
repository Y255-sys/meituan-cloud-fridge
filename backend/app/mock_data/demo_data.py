from datetime import date, timedelta

from sqlalchemy import select

from app.constants.enums import InventorySourceType, StorageLocation
from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.base import generate_prefixed_id
from app.models.household import Household
from app.models.ingredient import IngredientBase, UserIngredient
from app.models.recipe import RecipeBase, RecipeIngredientRel
from app.models.user import User

DEMO_PHONE = "13800000000"
DEMO_PASSWORD = "12345678"

INGREDIENTS = [
    {"id": "ing_tomato", "name": "番茄", "aliases": ["西红柿"], "category": "蔬菜", "default_unit": "个", "default_expire_days": 4, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["番茄", "西红柿"]},
    {"id": "ing_egg", "name": "鸡蛋", "aliases": ["蛋"], "category": "蛋奶", "default_unit": "个", "default_expire_days": 12, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["鸡蛋"]},
    {"id": "ing_potato", "name": "土豆", "aliases": ["马铃薯"], "category": "蔬菜", "default_unit": "个", "default_expire_days": 7, "storage_location": StorageLocation.AMBIENT.value, "searchable_keywords": ["土豆", "马铃薯"]},
    {"id": "ing_onion", "name": "洋葱", "aliases": [], "category": "蔬菜", "default_unit": "个", "default_expire_days": 7, "storage_location": StorageLocation.AMBIENT.value, "searchable_keywords": ["洋葱"]},
    {"id": "ing_green_pepper", "name": "青椒", "aliases": ["辣椒"], "category": "蔬菜", "default_unit": "个", "default_expire_days": 5, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["青椒"]},
    {"id": "ing_beef", "name": "牛肉", "aliases": [], "category": "肉类", "default_unit": "g", "default_expire_days": 2, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["牛肉"]},
    {"id": "ing_chicken", "name": "鸡胸肉", "aliases": ["鸡肉"], "category": "肉类", "default_unit": "g", "default_expire_days": 2, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["鸡胸肉", "鸡肉"]},
    {"id": "ing_cucumber", "name": "黄瓜", "aliases": [], "category": "蔬菜", "default_unit": "根", "default_expire_days": 4, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["黄瓜"]},
    {"id": "ing_rice", "name": "米饭", "aliases": ["大米"], "category": "主食", "default_unit": "份", "default_expire_days": 2, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["米饭", "大米"]},
    {"id": "ing_garlic", "name": "大蒜", "aliases": ["蒜"], "category": "调料", "default_unit": "瓣", "default_expire_days": 10, "storage_location": StorageLocation.AMBIENT.value, "searchable_keywords": ["蒜", "大蒜"]},
    {"id": "ing_carrot", "name": "胡萝卜", "aliases": [], "category": "蔬菜", "default_unit": "根", "default_expire_days": 6, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["胡萝卜"]},
    {"id": "ing_broccoli", "name": "西兰花", "aliases": [], "category": "蔬菜", "default_unit": "颗", "default_expire_days": 4, "storage_location": StorageLocation.CHILLED.value, "searchable_keywords": ["西兰花"]},
]

RECIPES = [
    {
        "id": "rcp_tomato_egg",
        "name": "番茄炒蛋",
        "category": "家常菜",
        "description": "12 分钟快手菜，适合工作日晚餐",
        "cook_time_minutes": 12,
        "difficulty": "easy",
        "servings": 2,
        "cover_image": "/mock/recipes/tomato-egg.jpg",
        "steps": ["番茄切块", "鸡蛋打散", "热锅翻炒 5 分钟", "加少量盐出锅"],
        "tags": ["worker_evening", "family_save_money"],
        "takeout_keywords": ["番茄炒蛋", "家常小炒"],
        "ingredients": [
            {"ingredient_base_id": "ing_tomato", "ingredient_name": "番茄", "required_quantity": 2, "unit": "个", "optional": False},
            {"ingredient_base_id": "ing_egg", "ingredient_name": "鸡蛋", "required_quantity": 3, "unit": "个", "optional": False},
        ],
    },
    {
        "id": "rcp_potato_egg",
        "name": "土豆鸡蛋饼",
        "category": "快手菜",
        "description": "省事省钱，爸妈模式也容易操作",
        "cook_time_minutes": 15,
        "difficulty": "easy",
        "servings": 2,
        "cover_image": "/mock/recipes/potato-egg.jpg",
        "steps": ["土豆擦丝", "鸡蛋打散", "平底锅摊熟", "切块装盘"],
        "tags": ["worker_evening", "senior_simple"],
        "takeout_keywords": ["土豆饼", "家常早餐"],
        "ingredients": [
            {"ingredient_base_id": "ing_potato", "ingredient_name": "土豆", "required_quantity": 2, "unit": "个", "optional": False},
            {"ingredient_base_id": "ing_egg", "ingredient_name": "鸡蛋", "required_quantity": 2, "unit": "个", "optional": False},
            {"ingredient_base_id": "ing_onion", "ingredient_name": "洋葱", "required_quantity": 1, "unit": "个", "optional": True},
        ],
    },
    {
        "id": "rcp_beef_pepper",
        "name": "青椒牛肉",
        "category": "家常菜",
        "description": "差一点主料就能做，适合少量补购",
        "cook_time_minutes": 20,
        "difficulty": "medium",
        "servings": 2,
        "cover_image": "/mock/recipes/beef-pepper.jpg",
        "steps": ["牛肉切片腌制", "青椒切丝", "大火快炒", "调味出锅"],
        "tags": ["worker_evening", "family_save_money"],
        "takeout_keywords": ["青椒牛肉", "小炒牛肉"],
        "ingredients": [
            {"ingredient_base_id": "ing_beef", "ingredient_name": "牛肉", "required_quantity": 250, "unit": "g", "optional": False},
            {"ingredient_base_id": "ing_green_pepper", "ingredient_name": "青椒", "required_quantity": 2, "unit": "个", "optional": False},
            {"ingredient_base_id": "ing_onion", "ingredient_name": "洋葱", "required_quantity": 1, "unit": "个", "optional": True},
        ],
    },
    {
        "id": "rcp_chicken_broccoli",
        "name": "西兰花鸡胸肉",
        "category": "轻食",
        "description": "少量补购就能做的健康晚餐",
        "cook_time_minutes": 18,
        "difficulty": "easy",
        "servings": 2,
        "cover_image": "/mock/recipes/chicken-broccoli.jpg",
        "steps": ["鸡胸肉切片", "西兰花焯水", "热锅翻炒", "少油少盐"],
        "tags": ["worker_evening"],
        "takeout_keywords": ["轻食鸡胸肉", "西兰花鸡肉"],
        "ingredients": [
            {"ingredient_base_id": "ing_chicken", "ingredient_name": "鸡胸肉", "required_quantity": 200, "unit": "g", "optional": False},
            {"ingredient_base_id": "ing_broccoli", "ingredient_name": "西兰花", "required_quantity": 1, "unit": "颗", "optional": False},
            {"ingredient_base_id": "ing_garlic", "ingredient_name": "大蒜", "required_quantity": 2, "unit": "瓣", "optional": True},
        ],
    },
    {
        "id": "rcp_cucumber_egg",
        "name": "黄瓜炒鸡蛋",
        "category": "家常菜",
        "description": "先消耗临期黄瓜的好选择",
        "cook_time_minutes": 10,
        "difficulty": "easy",
        "servings": 2,
        "cover_image": "/mock/recipes/cucumber-egg.jpg",
        "steps": ["黄瓜切片", "鸡蛋炒散", "合炒调味"],
        "tags": ["family_save_money", "senior_simple"],
        "takeout_keywords": ["黄瓜炒蛋", "家常菜"],
        "ingredients": [
            {"ingredient_base_id": "ing_cucumber", "ingredient_name": "黄瓜", "required_quantity": 1, "unit": "根", "optional": False},
            {"ingredient_base_id": "ing_egg", "ingredient_name": "鸡蛋", "required_quantity": 2, "unit": "个", "optional": False},
        ],
    },
]

RECOGNITION_PRESETS = {
    "fridge": [
        {"ingredient_base_id": "ing_tomato", "ingredient_name": "番茄", "quantity": 4, "unit": "个", "confidence": 0.97, "suggested_storage_location": StorageLocation.CHILLED.value, "suggested_expire_days": 4},
        {"ingredient_base_id": "ing_egg", "ingredient_name": "鸡蛋", "quantity": 6, "unit": "个", "confidence": 0.95, "suggested_storage_location": StorageLocation.CHILLED.value, "suggested_expire_days": 10},
        {"ingredient_base_id": "ing_green_pepper", "ingredient_name": "青椒", "quantity": 2, "unit": "个", "confidence": 0.89, "suggested_storage_location": StorageLocation.CHILLED.value, "suggested_expire_days": 5},
    ],
    "countertop": [
        {"ingredient_base_id": "ing_potato", "ingredient_name": "土豆", "quantity": 2, "unit": "个", "confidence": 0.96, "suggested_storage_location": StorageLocation.AMBIENT.value, "suggested_expire_days": 7},
        {"ingredient_base_id": "ing_onion", "ingredient_name": "洋葱", "quantity": 2, "unit": "个", "confidence": 0.93, "suggested_storage_location": StorageLocation.AMBIENT.value, "suggested_expire_days": 7},
    ],
    "shopping_bag": [
        {"ingredient_base_id": "ing_broccoli", "ingredient_name": "西兰花", "quantity": 1, "unit": "颗", "confidence": 0.94, "suggested_storage_location": StorageLocation.CHILLED.value, "suggested_expire_days": 4},
        {"ingredient_base_id": "ing_chicken", "ingredient_name": "鸡胸肉", "quantity": 300, "unit": "g", "confidence": 0.88, "suggested_storage_location": StorageLocation.CHILLED.value, "suggested_expire_days": 2},
    ],
}

MOCK_ORDERS = {
    "mt_20260522001": {
        "items": [
            {"ingredient_base_id": "ing_broccoli", "ingredient_name": "西兰花", "quantity": 1, "unit": "颗"},
            {"ingredient_base_id": "ing_chicken", "ingredient_name": "鸡胸肉", "quantity": 300, "unit": "g"},
            {"ingredient_base_id": "ing_carrot", "ingredient_name": "胡萝卜", "quantity": 2, "unit": "根"},
        ]
    }
}

PRODUCT_CATALOG = {
    "ing_beef": [{"product_id": "prd_beef_300g", "product_name": "鲜切牛里脊 300g", "price": 21.9, "original_price": 25.9, "discount_text": "限时直降 4 元", "merchant_name": "美团买菜自营", "eta_minutes": 29}],
    "ing_chicken": [{"product_id": "prd_chicken_250g", "product_name": "鲜嫩鸡胸肉 250g", "price": 12.8, "original_price": 15.8, "discount_text": "立减 3 元", "merchant_name": "美团闪购精选", "eta_minutes": 31}],
    "ing_broccoli": [{"product_id": "prd_broccoli_1", "product_name": "西兰花 1 颗", "price": 6.9, "original_price": 7.9, "discount_text": "第 2 件 8 折", "merchant_name": "美团买菜自营", "eta_minutes": 26}],
    "ing_green_pepper": [{"product_id": "prd_pepper_2", "product_name": "青椒 2 个装", "price": 5.8, "original_price": 6.8, "discount_text": "限时特价", "merchant_name": "美团买菜自营", "eta_minutes": 27}],
    "ing_onion": [{"product_id": "prd_onion_2", "product_name": "洋葱 2 个装", "price": 4.5, "original_price": 5.2, "discount_text": "凑单好物", "merchant_name": "美团闪购精选", "eta_minutes": 30}],
}

TAKEOUT_ALTERNATIVES = {
    "rcp_tomato_egg": [{"merchant_id": "mt_rest_01", "merchant_name": "家常小炒", "dish_name": "番茄炒蛋盖饭", "price": 22.8, "eta_minutes": 28, "reason": "想省时间可直接点家常风味外卖"}],
    "rcp_beef_pepper": [{"merchant_id": "mt_rest_02", "merchant_name": "下饭小馆", "dish_name": "青椒牛肉盖饭", "price": 26.8, "eta_minutes": 32, "reason": "如果今晚不做饭，可直接替代"}],
    "rcp_chicken_broccoli": [{"merchant_id": "mt_rest_03", "merchant_name": "轻食能量站", "dish_name": "西兰花鸡胸肉轻食碗", "price": 29.9, "eta_minutes": 30, "reason": "补蛋白同时少油省事"}],
    "rcp_potato_egg": [{"merchant_id": "mt_rest_04", "merchant_name": "早点厨房", "dish_name": "土豆鸡蛋饼套餐", "price": 18.6, "eta_minutes": 24, "reason": "爸妈模式下更容易一键下单"}],
}


def seed_demo_data() -> None:
    db = SessionLocal()
    try:
        existing_user = db.scalar(select(User).where(User.phone == DEMO_PHONE))
        if existing_user is not None:
            return

        household = Household(id=generate_prefixed_id("house"), name="小王家", owner_user_id=None)
        db.add(household)
        db.flush()

        user = User(
            id=generate_prefixed_id("usr"),
            phone=DEMO_PHONE,
            password_hash=hash_password(DEMO_PASSWORD),
            nickname="小王",
            household_id=household.id,
            senior_mode_enabled=False,
            city_code="310100",
            dietary_preferences=["light"],
            allergy_tags=[],
            taste_tags=["home_style"],
        )
        db.add(user)
        db.flush()
        household.owner_user_id = user.id

        for ingredient in INGREDIENTS:
            db.add(IngredientBase(**ingredient))

        for recipe in RECIPES:
            recipe_row = RecipeBase(
                id=recipe["id"],
                name=recipe["name"],
                category=recipe["category"],
                description=recipe["description"],
                cook_time_minutes=recipe["cook_time_minutes"],
                difficulty=recipe["difficulty"],
                servings=recipe["servings"],
                cover_image=recipe["cover_image"],
                steps=recipe["steps"],
                tags=recipe["tags"],
                takeout_keywords=recipe["takeout_keywords"],
            )
            db.add(recipe_row)
            for ingredient in recipe["ingredients"]:
                db.add(
                    RecipeIngredientRel(
                        id=generate_prefixed_id("rel"),
                        recipe_id=recipe["id"],
                        ingredient_base_id=ingredient["ingredient_base_id"],
                        ingredient_name=ingredient["ingredient_name"],
                        required_quantity=ingredient["required_quantity"],
                        unit=ingredient["unit"],
                        optional=ingredient["optional"],
                    )
                )

        today = date.today()
        seed_inventory = [
            {"ingredient_base_id": "ing_tomato", "ingredient_name": "番茄", "category": "蔬菜", "quantity": 4, "unit": "个", "storage_location": StorageLocation.CHILLED.value, "expire_at": today + timedelta(days=3)},
            {"ingredient_base_id": "ing_egg", "ingredient_name": "鸡蛋", "category": "蛋奶", "quantity": 6, "unit": "个", "storage_location": StorageLocation.CHILLED.value, "expire_at": today + timedelta(days=8)},
            {"ingredient_base_id": "ing_potato", "ingredient_name": "土豆", "category": "蔬菜", "quantity": 2, "unit": "个", "storage_location": StorageLocation.AMBIENT.value, "expire_at": today + timedelta(days=5)},
            {"ingredient_base_id": "ing_onion", "ingredient_name": "洋葱", "category": "蔬菜", "quantity": 2, "unit": "个", "storage_location": StorageLocation.AMBIENT.value, "expire_at": today + timedelta(days=5)},
            {"ingredient_base_id": "ing_green_pepper", "ingredient_name": "青椒", "category": "蔬菜", "quantity": 2, "unit": "个", "storage_location": StorageLocation.CHILLED.value, "expire_at": today + timedelta(days=2)},
            {"ingredient_base_id": "ing_cucumber", "ingredient_name": "黄瓜", "category": "蔬菜", "quantity": 1, "unit": "根", "storage_location": StorageLocation.CHILLED.value, "expire_at": today + timedelta(days=1)},
        ]
        for item in seed_inventory:
            db.add(
                UserIngredient(
                    id=generate_prefixed_id("ui"),
                    user_id=user.id,
                    household_id=household.id,
                    ingredient_base_id=item["ingredient_base_id"],
                    ingredient_name=item["ingredient_name"],
                    category=item["category"],
                    quantity=item["quantity"],
                    unit=item["unit"],
                    storage_location=item["storage_location"],
                    expire_at=item["expire_at"],
                    status="fresh",
                    source_type=InventorySourceType.MANUAL.value,
                    source_ref_id=None,
                    notes=None,
                )
            )

        db.commit()
    finally:
        db.close()

