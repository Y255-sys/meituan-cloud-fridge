# 第一阶段：从 0 重构方案

## 1. 阶段目标

本阶段只做“新项目蓝图”，不兼容旧目录、不复用旧代码、不背旧技术债，目标是先把后续开发的骨架一次定清楚：

1. 明确新项目目录结构
2. 明确前后端职责边界
3. 明确主链路数据流
4. 明确 API 契约
5. 明确数据库表结构
6. 明确前端 TypeScript 类型
7. 明确页面与接口映射

设计原则：

- 优先保证 P0 演示链路稳定可跑
- 复杂能力先规则化、Mock 化，但接口必须真实
- 结构按“可维护全栈项目”设计，而不是一次性脚本 Demo
- 移动端优先，但兼容桌面路演

## 2. 新项目目录结构

项目根目录固定为 `0522/meituan-cloud-fridge`。

```text
0522/meituan-cloud-fridge
├── README.md
├── docs/
│   ├── stage-1-architecture.md
│   └── demo-script.md                     # 第四阶段补充
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── postcss.config.js
│   ├── tailwind.config.ts
│   └── src/
│       ├── app/
│       │   ├── router.tsx
│       │   ├── providers.tsx
│       │   └── layouts/
│       ├── assets/
│       ├── components/
│       │   ├── common/
│       │   ├── inventory/
│       │   ├── recipe/
│       │   ├── purchase/
│       │   └── senior-mode/
│       ├── features/
│       │   ├── auth/
│       │   ├── profile/
│       │   ├── recognition/
│       │   ├── inventory/
│       │   ├── recipe/
│       │   ├── purchase/
│       │   └── senior-mode/
│       ├── hooks/
│       ├── lib/
│       │   ├── api/
│       │   ├── config/
│       │   ├── mock/
│       │   └── utils/
│       ├── pages/
│       │   ├── HomePage.tsx
│       │   ├── RecognizePage.tsx
│       │   ├── InventoryPage.tsx
│       │   ├── RecipesPage.tsx
│       │   ├── PurchasePage.tsx
│       │   ├── SeniorModePage.tsx
│       │   ├── LoginPage.tsx
│       │   └── NotFoundPage.tsx
│       ├── services/
│       ├── styles/
│       ├── types/
│       └── main.tsx
├── backend/
│   ├── pyproject.toml
│   ├── .env.example
│   ├── alembic.ini
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   ├── database.py
│   │   │   ├── exceptions.py
│   │   │   └── response.py
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── profile.py
│   │   │   ├── recognition.py
│   │   │   ├── inventory.py
│   │   │   ├── order_sync.py
│   │   │   ├── recipe.py
│   │   │   ├── purchase.py
│   │   │   └── senior_mode.py
│   │   ├── deps/
│   │   ├── constants/
│   │   └── mock_data/
│   ├── alembic/
│   │   ├── env.py
│   │   └── versions/
│   ├── tests/
│   │   ├── api/
│   │   └── services/
│   └── scripts/
│       ├── seed_demo_data.py
│       └── verify_demo_flow.py
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   └── postgres/
│   ├── env/
│   │   ├── backend.env.example
│   │   └── frontend.env.example
│   └── sql/
│       └── bootstrap.sql
└── scripts/
    ├── dev.sh
    ├── dev.ps1
    └── check.sh
```

### 为什么这样拆

- `frontend` 与 `backend` 彻底分离，符合前后端分离开发与部署方式
- `docs` 单独管理，方便黑客松汇报、交接和复盘
- `infra` 放环境与数据库脚本，避免应用代码与运维配置混在一起
- `features` 与 `components` 分层，避免前端所有逻辑堆在页面里
- `routers / services / repositories / models / schemas` 明确后端职责边界，方便后续扩展

## 3. 系统架构设计

## 3.1 总体架构

```text
React + Vite + TypeScript
        |
TanStack Query + API Client
        |
      FastAPI
        |
service -> repository -> SQLAlchemy
        |
    PostgreSQL
```

补充能力：

- 鉴权：JWT Access Token，P0 不做复杂刷新机制
- Mock 策略：识别、商品匹配、优惠解释、外卖替代允许规则 + Mock 数据
- 演示稳定性：前端支持 `mock` / `real` 双模式切换

## 3.2 核心模块

### 前端模块

- 认证模块：登录、注册、Token 存储
- 识别模块：上传图片、展示候选食材、用户修正后入库
- 库存模块：列表、筛选、临期标记、增删改
- 推荐模块：三类菜谱分组展示
- 补购模块：缺失分析、补购方案、商品匹配、下单跳转
- 爸妈模式模块：大字版首页、极简操作、代付入口

### 后端模块

- Auth Service：注册登录与当前用户获取
- Profile Service：用户配置、饮食偏好、爸妈模式
- Recognition Service：Mock 图像识别与标准化食材映射
- Inventory Service：库存 CRUD、临期判断、家庭库存聚合
- Recipe Service：三类推荐、菜谱详情、缺失分析
- Purchase Service：补购方案、商品匹配、优惠说明、下单跳转
- Order Sync Service：模拟美团买菜/闪购订单同步入库

## 3.3 数据流说明

### 主链路 1：拍照识别入库

1. 用户上传食材图片
2. 前端调用 `POST /recognitions`
3. 后端返回候选识别项列表与置信度
4. 用户手动调整名称、数量、单位、保质期
5. 前端调用 `POST /inventory/import-recognition`
6. 后端写入 `user_ingredient`，返回最新库存摘要

### 主链路 2：今晚吃什么

1. 前端读取库存 `GET /inventory`
2. 前端调用 `GET /recipes/recommendations`
3. 后端基于库存和偏好生成三类结果：
   - 现有库存可做
   - 少量补购可做
   - 直接外卖替代
4. 用户点击某个菜谱进入详情 `GET /recipes/{recipeId}`

### 主链路 3：缺失分析与补购

1. 用户在推荐页选择“少量补购可做”的菜谱
2. 前端调用 `POST /recipes/missing-analysis`
3. 后端返回缺失食材和缺口数量
4. 前端调用 `POST /purchase-plans`
5. 后端聚合缺失食材，生成补购方案、凑单建议、优惠解释
6. 前端再调用 `POST /products/match`
7. 后端返回商品匹配结果与外卖替代入口
8. 前端调用 `POST /checkout/redirect`
9. 后端返回跳转链接与代付说明

### 主链路 4：爸妈模式

1. 用户切换爸妈模式 `PATCH /profile/senior-mode`
2. 前端切换到大字版 UI
3. 关键动作简化为：
   - 看库存
   - 拍照入库
   - 今晚吃什么
   - 发给孩子代付

## 4. API 契约清单

## 4.1 统一返回结构

成功返回：

```json
{
  "code": 0,
  "message": "ok",
  "data": {},
  "request_id": "req_123456"
}
```

失败返回：

```json
{
  "code": 40001,
  "message": "invalid request",
  "data": null,
  "request_id": "req_123456"
}
```

### 错误码约定

- `0` 成功
- `40000` 通用参数错误
- `40001` 数据校验失败
- `40100` 未登录或 Token 无效
- `40300` 无权限
- `40400` 资源不存在
- `40900` 资源冲突
- `50000` 服务内部错误
- `50010` Mock 能力暂不可用

## 4.2 认证与用户配置

### `POST /api/v1/auth/register`

用途：注册

请求体：

```json
{
  "phone": "13800000000",
  "password": "12345678",
  "nickname": "小王"
}
```

响应 `data`：

```json
{
  "user": {
    "id": "usr_x1",
    "nickname": "小王",
    "phone": "13800000000"
  },
  "token": "jwt_token"
}
```

### `POST /api/v1/auth/login`

用途：登录

请求体：

```json
{
  "phone": "13800000000",
  "password": "12345678"
}
```

响应 `data`：

```json
{
  "user": {
    "id": "usr_x1",
    "nickname": "小王",
    "phone": "13800000000"
  },
  "token": "jwt_token"
}
```

### `GET /api/v1/profile`

用途：获取用户配置

响应 `data`：

```json
{
  "user_id": "usr_x1",
  "nickname": "小王",
  "phone": "13800000000",
  "household_name": "小王家",
  "senior_mode_enabled": false,
  "dietary_preferences": ["low_oil"],
  "allergy_tags": ["peanut"],
  "taste_tags": ["spicy"],
  "city_code": "310100"
}
```

### `PATCH /api/v1/profile`

用途：更新用户配置

请求体：

```json
{
  "nickname": "小王妈妈",
  "dietary_preferences": ["light"],
  "taste_tags": ["not_spicy"]
}
```

### `PATCH /api/v1/profile/senior-mode`

用途：切换爸妈模式

请求体：

```json
{
  "enabled": true
}
```

响应 `data`：

```json
{
  "enabled": true
}
```

## 4.3 图像识别与订单同步

### `POST /api/v1/recognitions`

用途：上传图片并识别食材

请求体：`multipart/form-data`

- `image`
- `scene`，可选值：`fridge` / `countertop` / `shopping_bag`

响应 `data`：

```json
{
  "recognition_id": "rec_001",
  "image_url": "/mock/recognition/rec_001.jpg",
  "items": [
    {
      "temp_id": "tmp_1",
      "ingredient_base_id": "ing_tomato",
      "ingredient_name": "番茄",
      "quantity": 4,
      "unit": "个",
      "confidence": 0.97,
      "source": "vision_mock",
      "editable": true,
      "suggested_storage_location": "冷藏",
      "suggested_expire_days": 4
    }
  ]
}
```

### `POST /api/v1/inventory/import-recognition`

用途：把修正后的识别结果入库

请求体：

```json
{
  "recognition_id": "rec_001",
  "items": [
    {
      "ingredient_base_id": "ing_tomato",
      "ingredient_name": "番茄",
      "quantity": 4,
      "unit": "个",
      "storage_location": "冷藏",
      "expire_at": "2026-05-26"
    }
  ]
}
```

### `POST /api/v1/order-sync`

用途：同步平台订单并入库

请求体：

```json
{
  "channel": "meituan_grocery",
  "external_order_id": "mt_20260522001"
}
```

响应 `data`：

```json
{
  "synced": true,
  "order_id": "ord_001",
  "imported_items": 5
}
```

## 4.4 库存管理

### `GET /api/v1/inventory`

用途：获取库存列表

查询参数：

- `keyword`
- `category`
- `status`：`fresh` / `expiring` / `expired`
- `storage_location`
- `sort_by`：`expire_at` / `updated_at`

响应 `data`：

```json
{
  "summary": {
    "total_items": 22,
    "expiring_items": 4,
    "expired_items": 1
  },
  "items": [
    {
      "id": "ui_001",
      "ingredient_base_id": "ing_tomato",
      "ingredient_name": "番茄",
      "category": "蔬菜",
      "quantity": 4,
      "unit": "个",
      "storage_location": "冷藏",
      "status": "expiring",
      "expire_at": "2026-05-24",
      "days_to_expire": 2,
      "source_type": "manual",
      "source_ref_id": null,
      "updated_at": "2026-05-22T19:00:00+08:00"
    }
  ]
}
```

### `POST /api/v1/inventory`

用途：手动新增库存

### `PATCH /api/v1/inventory/{itemId}`

用途：编辑库存

### `DELETE /api/v1/inventory/{itemId}`

用途：删除库存

### `GET /api/v1/inventory/{itemId}`

用途：获取单个库存详情

## 4.5 菜谱推荐

### `GET /api/v1/recipes/recommendations`

用途：生成三类推荐

查询参数：

- `meal_type`：`dinner` / `lunch`
- `servings`
- `scene`：`worker_evening` / `family_save_money` / `senior_simple`

响应 `data`：

```json
{
  "context": {
    "meal_type": "dinner",
    "scene": "worker_evening",
    "inventory_count": 22
  },
  "groups": [
    {
      "type": "cook_now",
      "title": "不补购也能做",
      "description": "优先消耗现有库存",
      "recipes": [
        {
          "recipe_id": "rcp_001",
          "recipe_name": "番茄炒蛋",
          "cover_image": "/mock/recipe/tomato-egg.jpg",
          "cook_time_minutes": 12,
          "match_score": 96,
          "missing_count": 0,
          "highlight_reason": "家里现有番茄和鸡蛋，可直接开做"
        }
      ]
    },
    {
      "type": "buy_little",
      "title": "少量补购就能做",
      "description": "差 1-3 样食材即可完成",
      "recipes": []
    },
    {
      "type": "takeout",
      "title": "不想做饭，直接外卖替代",
      "description": "同风味外卖替代",
      "recipes": []
    }
  ]
}
```

### `GET /api/v1/recipes/{recipeId}`

用途：获取菜谱详情

响应 `data`：

```json
{
  "recipe_id": "rcp_001",
  "recipe_name": "番茄炒蛋",
  "description": "12 分钟快手菜",
  "cook_time_minutes": 12,
  "difficulty": "easy",
  "servings": 2,
  "steps": [
    "番茄切块",
    "鸡蛋打散",
    "热锅翻炒"
  ],
  "ingredients": [
    {
      "ingredient_base_id": "ing_tomato",
      "ingredient_name": "番茄",
      "required_quantity": 2,
      "unit": "个",
      "owned_quantity": 4,
      "missing_quantity": 0
    }
  ],
  "nutrition_tip": "适合工作日晚餐",
  "can_cook_now": true
}
```

### `POST /api/v1/recipes/missing-analysis`

用途：分析菜谱缺失食材

请求体：

```json
{
  "recipe_ids": ["rcp_002", "rcp_007"],
  "servings": 2
}
```

响应 `data`：

```json
{
  "recipes": [
    {
      "recipe_id": "rcp_002",
      "recipe_name": "青椒牛肉",
      "missing_ingredients": [
        {
          "ingredient_base_id": "ing_beef",
          "ingredient_name": "牛肉",
          "missing_quantity": 250,
          "unit": "g"
        }
      ]
    }
  ],
  "aggregated_missing": [
    {
      "ingredient_base_id": "ing_beef",
      "ingredient_name": "牛肉",
      "missing_quantity": 250,
      "unit": "g"
    }
  ]
}
```

## 4.6 补购与商品匹配

### `POST /api/v1/purchase-plans`

用途：生成补购方案

请求体：

```json
{
  "recipe_ids": ["rcp_002"],
  "strategy": "lowest_cost"
}
```

响应 `data`：

```json
{
  "plan_id": "plan_001",
  "strategy": "lowest_cost",
  "recipes": [
    {
      "recipe_id": "rcp_002",
      "recipe_name": "青椒牛肉"
    }
  ],
  "items": [
    {
      "ingredient_base_id": "ing_beef",
      "ingredient_name": "牛肉",
      "required_quantity": 250,
      "unit": "g",
      "estimated_price": 18.9,
      "reason": "核心主料缺失"
    }
  ],
  "promotion_explanation": "当前方案优先选择一人份补货，避免浪费",
  "estimated_total_price": 22.8
}
```

### `POST /api/v1/products/match`

用途：匹配商品

请求体：

```json
{
  "plan_id": "plan_001"
}
```

响应 `data`：

```json
{
  "plan_id": "plan_001",
  "products": [
    {
      "ingredient_base_id": "ing_beef",
      "ingredient_name": "牛肉",
      "matched_product_id": "prd_1001",
      "product_name": "鲜切牛里脊 300g",
      "price": 21.9,
      "original_price": 25.9,
      "discount_text": "限时直降 4 元",
      "merchant_name": "美团买菜自营",
      "eta_minutes": 29
    }
  ],
  "takeout_alternatives": [
    {
      "merchant_id": "mt_rest_01",
      "merchant_name": "家常小炒",
      "dish_name": "青椒牛肉盖饭",
      "price": 26.8,
      "eta_minutes": 32,
      "reason": "如果今晚不做饭，可直接替代"
    }
  ]
}
```

### `POST /api/v1/checkout/redirect`

用途：生成下单跳转信息

请求体：

```json
{
  "source_type": "grocery",
  "selected_product_ids": ["prd_1001"],
  "senior_mode_delegate_pay": true
}
```

响应 `data`：

```json
{
  "checkout_url": "https://mock.meituan.com/checkout/plan_001",
  "delegate_pay": {
    "enabled": true,
    "share_message": "妈，今晚做青椒牛肉差一份牛肉，我已经帮你选好了，点这里让孩子代付。"
  }
}
```

## 5. 数据库表结构设计

说明：P0 只建能支撑 Demo 主链路的核心表，复杂推荐画像、对话历史、优惠引擎明细暂不入库。

## 5.1 `users`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| phone | varchar(20) | 登录手机号，唯一 |
| password_hash | varchar(255) | 密码哈希 |
| nickname | varchar(50) | 昵称 |
| household_id | uuid | 家庭 ID |
| senior_mode_enabled | boolean | 爸妈模式开关 |
| city_code | varchar(20) | 城市编码 |
| dietary_preferences | jsonb | 饮食偏好 |
| allergy_tags | jsonb | 过敏标签 |
| taste_tags | jsonb | 口味标签 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

设计理由：

- P0 把配置先收敛进 `users`，减少 join 成本
- `jsonb` 足够承载轻量偏好标签

## 5.2 `households`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| name | varchar(100) | 家庭名称 |
| owner_user_id | uuid | 家庭拥有者 |
| created_at | timestamptz | 创建时间 |

设计理由：

- 没有 `household` 就很难把“家庭库存”讲清楚
- 后续多人协作、家庭共享天然可扩展

## 5.3 `ingredient_base`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | varchar(50) | 主键，例如 `ing_tomato` |
| name | varchar(100) | 标准食材名 |
| aliases | jsonb | 别名列表 |
| category | varchar(50) | 蔬菜、肉类、蛋奶等 |
| default_unit | varchar(20) | 默认单位 |
| default_expire_days | integer | 默认保鲜天数 |
| storage_location | varchar(20) | 常规储存方式 |
| searchable_keywords | tsvector/jsonb | 搜索关键词 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

## 5.4 `user_ingredient`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| user_id | uuid | 所属用户 |
| household_id | uuid | 所属家庭 |
| ingredient_base_id | varchar(50) | 标准食材 ID |
| ingredient_name | varchar(100) | 入库时展示名 |
| quantity | numeric(10,2) | 数量 |
| unit | varchar(20) | 单位 |
| storage_location | varchar(20) | 冷藏/冷冻/常温 |
| expire_at | date | 到期时间 |
| status | varchar(20) | fresh/expiring/expired |
| source_type | varchar(20) | manual/recognition/order_sync |
| source_ref_id | varchar(64) | 来源记录 ID |
| notes | varchar(255) | 备注 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

索引建议：

- `(household_id, status)`
- `(user_id, updated_at desc)`
- `(ingredient_base_id)`

## 5.5 `recipe_base`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | varchar(50) | 主键 |
| name | varchar(100) | 菜谱名 |
| category | varchar(50) | 家常菜、快手菜等 |
| description | varchar(255) | 简述 |
| cook_time_minutes | integer | 烹饪时长 |
| difficulty | varchar(20) | easy/medium |
| servings | integer | 默认份数 |
| cover_image | varchar(255) | 封面图 |
| steps | jsonb | 步骤 |
| tags | jsonb | 适用标签 |
| takeout_keywords | jsonb | 外卖替代关键词 |
| created_at | timestamptz | 创建时间 |
| updated_at | timestamptz | 更新时间 |

## 5.6 `recipe_ingredient_rel`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| recipe_id | varchar(50) | 菜谱 ID |
| ingredient_base_id | varchar(50) | 食材 ID |
| ingredient_name | varchar(100) | 展示名兜底 |
| required_quantity | numeric(10,2) | 所需数量 |
| unit | varchar(20) | 单位 |
| optional | boolean | 是否可选 |
| created_at | timestamptz | 创建时间 |

## 5.7 `order_sync_rel`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| user_id | uuid | 用户 ID |
| household_id | uuid | 家庭 ID |
| channel | varchar(50) | 来源渠道 |
| external_order_id | varchar(100) | 外部订单号 |
| raw_payload | jsonb | 原始订单数据 |
| sync_status | varchar(20) | synced/failed |
| imported_count | integer | 入库数量 |
| created_at | timestamptz | 创建时间 |

## 5.8 `purchase_plan`

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | uuid | 主键 |
| user_id | uuid | 用户 ID |
| household_id | uuid | 家庭 ID |
| strategy | varchar(30) | lowest_cost/minimum_items |
| recipe_ids | jsonb | 关联菜谱 |
| aggregated_missing | jsonb | 缺失食材聚合 |
| estimated_total_price | numeric(10,2) | 预估价格 |
| promotion_explanation | varchar(255) | 优惠说明 |
| created_at | timestamptz | 创建时间 |

说明：

- 商品匹配结果可以先作为接口实时计算，不强制入库
- 如果需要留痕，可追加 `purchase_plan_item` 与 `product_match_snapshot`

## 6. 前端 TypeScript 类型设计

## 6.1 基础响应类型

```ts
export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
  request_id: string;
}

export interface PagelessListResponse<T> {
  items: T[];
}
```

## 6.2 认证与用户

```ts
export interface User {
  id: string;
  phone: string;
  nickname: string;
}

export interface AuthPayload {
  user: User;
  token: string;
}

export interface UserProfile {
  user_id: string;
  nickname: string;
  phone: string;
  household_name: string;
  senior_mode_enabled: boolean;
  dietary_preferences: string[];
  allergy_tags: string[];
  taste_tags: string[];
  city_code: string;
}
```

## 6.3 食材识别与库存

```ts
export interface RecognitionItem {
  temp_id: string;
  ingredient_base_id: string | null;
  ingredient_name: string;
  quantity: number;
  unit: string;
  confidence: number;
  source: "vision_mock" | "vision_real";
  editable: boolean;
  suggested_storage_location: "冷藏" | "冷冻" | "常温";
  suggested_expire_days: number;
}

export interface RecognitionResult {
  recognition_id: string;
  image_url: string;
  items: RecognitionItem[];
}

export type InventoryStatus = "fresh" | "expiring" | "expired";

export interface InventoryItem {
  id: string;
  ingredient_base_id: string;
  ingredient_name: string;
  category: string;
  quantity: number;
  unit: string;
  storage_location: "冷藏" | "冷冻" | "常温";
  status: InventoryStatus;
  expire_at: string;
  days_to_expire: number;
  source_type: "manual" | "recognition" | "order_sync";
  source_ref_id: string | null;
  updated_at: string;
}

export interface InventorySummary {
  total_items: number;
  expiring_items: number;
  expired_items: number;
}

export interface InventoryListData {
  summary: InventorySummary;
  items: InventoryItem[];
}
```

## 6.4 菜谱推荐

```ts
export type RecommendationGroupType =
  | "cook_now"
  | "buy_little"
  | "takeout";

export interface RecipeCard {
  recipe_id: string;
  recipe_name: string;
  cover_image: string;
  cook_time_minutes: number;
  match_score: number;
  missing_count: number;
  highlight_reason: string;
}

export interface RecommendationGroup {
  type: RecommendationGroupType;
  title: string;
  description: string;
  recipes: RecipeCard[];
}

export interface RecipeRecommendationsData {
  context: {
    meal_type: string;
    scene: string;
    inventory_count: number;
  };
  groups: RecommendationGroup[];
}

export interface RecipeIngredientUsage {
  ingredient_base_id: string;
  ingredient_name: string;
  required_quantity: number;
  unit: string;
  owned_quantity: number;
  missing_quantity: number;
}

export interface RecipeDetail {
  recipe_id: string;
  recipe_name: string;
  description: string;
  cook_time_minutes: number;
  difficulty: string;
  servings: number;
  steps: string[];
  ingredients: RecipeIngredientUsage[];
  nutrition_tip: string;
  can_cook_now: boolean;
}
```

## 6.5 缺失分析与补购

```ts
export interface MissingIngredient {
  ingredient_base_id: string;
  ingredient_name: string;
  missing_quantity: number;
  unit: string;
}

export interface MissingAnalysisRecipe {
  recipe_id: string;
  recipe_name: string;
  missing_ingredients: MissingIngredient[];
}

export interface MissingAnalysisData {
  recipes: MissingAnalysisRecipe[];
  aggregated_missing: MissingIngredient[];
}

export interface PurchasePlanItem {
  ingredient_base_id: string;
  ingredient_name: string;
  required_quantity: number;
  unit: string;
  estimated_price: number;
  reason: string;
}

export interface PurchasePlan {
  plan_id: string;
  strategy: "lowest_cost" | "minimum_items";
  recipes: Array<{
    recipe_id: string;
    recipe_name: string;
  }>;
  items: PurchasePlanItem[];
  promotion_explanation: string;
  estimated_total_price: number;
}

export interface ProductMatchItem {
  ingredient_base_id: string;
  ingredient_name: string;
  matched_product_id: string;
  product_name: string;
  price: number;
  original_price: number;
  discount_text: string;
  merchant_name: string;
  eta_minutes: number;
}

export interface TakeoutAlternative {
  merchant_id: string;
  merchant_name: string;
  dish_name: string;
  price: number;
  eta_minutes: number;
  reason: string;
}

export interface ProductMatchData {
  plan_id: string;
  products: ProductMatchItem[];
  takeout_alternatives: TakeoutAlternative[];
}

export interface CheckoutRedirectData {
  checkout_url: string;
  delegate_pay: {
    enabled: boolean;
    share_message: string;
  };
}
```

## 6.6 前端状态与配置

```ts
export type ApiMode = "mock" | "real";

export interface AppRuntimeConfig {
  apiBaseUrl: string;
  apiMode: ApiMode;
}
```

设计理由：

- 所有类型围绕接口契约定义，确保前后端对齐
- `mock` / `real` 切换作为一等配置，而不是散落在页面里
- 推荐、补购、外卖替代拆开建模，演示时更直观

## 7. 页面与接口映射关系

| 页面 | 核心目标 | 调用接口 | 说明 |
| --- | --- | --- | --- |
| 首页 `HomePage` | 展示入口与今日摘要 | `GET /profile` `GET /inventory` `GET /recipes/recommendations` | 展示库存摘要、推荐入口、爸妈模式入口 |
| 拍照识别页 `RecognizePage` | 上传图片并确认识别结果 | `POST /recognitions` `POST /inventory/import-recognition` | 必须允许手动修改后入库 |
| 库存管理页 `InventoryPage` | 看库存、筛选、临期管理、增删改 | `GET /inventory` `POST /inventory` `PATCH /inventory/{itemId}` `DELETE /inventory/{itemId}` | P0 的核心数据操作页 |
| 菜谱推荐页 `RecipesPage` | 三类推荐分组展示 | `GET /recipes/recommendations` `GET /recipes/{recipeId}` `POST /recipes/missing-analysis` | 支撑“今晚吃什么”主场景 |
| 补购结算页 `PurchasePage` | 生成补购方案和商品匹配 | `POST /purchase-plans` `POST /products/match` `POST /checkout/redirect` | 展示缺失食材、商品、优惠、外卖替代 |
| 爸妈模式页 `SeniorModePage` | 极简大字操作 | `GET /profile` `PATCH /profile/senior-mode` `GET /inventory` `GET /recipes/recommendations` `POST /checkout/redirect` | 强化低门槛和代付场景 |
| 登录页 `LoginPage` | 进入系统 | `POST /auth/login` `POST /auth/register` | P0 保持最小可用 |

## 8. 推荐与补购的简化实现策略

这些能力在 P0 阶段为保证稳定演示，采用“规则 + Mock 数据”：

### 图像识别

- 输入图片后按场景随机命中一组预设识别结果
- 返回值严格按真实识别接口结构设计
- 保留 `confidence`、`source`、`editable` 字段，为后续接入真实视觉模型留口

### 菜谱推荐

- 用库存匹配率计算 `cook_now`
- 缺 1 到 3 个食材归为 `buy_little`
- 按菜谱 `takeout_keywords` 匹配预设商家，生成 `takeout`

### 商品匹配

- 按食材类别和数量从预置商品池里挑最像的 SKU
- 优先返回“刚好够用”的规格，突出省钱补购逻辑

### 优惠解释

- 先不做真实券引擎
- 用规则文案解释：
  - 为什么选这个商品
  - 为什么这个方案更省
  - 是否适合爸妈直接代付

这样设计的原因：

- 能稳定跑完主链路
- 接口结构不需要重写
- 第四阶段联调成本低

## 9. 本阶段完成情况

### 做了什么

- 设计了新的项目根目录和工程分层
- 设计了前后端系统架构和主链路数据流
- 设计了统一 API 返回结构与接口清单
- 设计了 PostgreSQL 核心表
- 设计了前端 TypeScript 类型模型
- 设计了页面与接口映射关系

### 为什么这样设计

- 黑客松 Demo 最重要的是链路顺、解释清、结构稳
- 这套设计优先满足 3 到 5 分钟演示，而不是追求大而全
- 所有高风险能力都先做成“可演示、可替换”的稳定壳层

### 还剩什么

- 第二阶段：FastAPI 后端从 0 搭建
- 第三阶段：React 前端从 0 搭建
- 第四阶段：真实联调、空错态补齐、演示脚本收口

## 10. 第二阶段实施建议

确认后，下一步按下面顺序直接开工：

1. 初始化 `backend` 工程与依赖
2. 建立 `users / households / ingredient_base / user_ingredient / recipe_base / recipe_ingredient_rel / order_sync_rel / purchase_plan`
3. 完成统一响应、异常、JWT、配置
4. 先跑通 `auth / profile / recognition / inventory / recipe / purchase`
5. 写种子数据和 `verify_demo_flow.py` 验证主链路
