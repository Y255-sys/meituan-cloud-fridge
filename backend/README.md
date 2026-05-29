# Backend

FastAPI 后端，负责：

- 用户注册登录与 JWT 鉴权
- 用户配置与爸妈模式
- 图像识别 Mock 接口
- 家庭库存管理
- 三类菜谱推荐
- 缺失食材分析
- 补购方案与商品匹配
- 下单跳转与代付文案

## 启动

1. 复制环境变量：

```bash
cp .env.example .env
```

2. 启动 PostgreSQL：

```bash
docker compose -f ../infra/docker/docker-compose.yml up -d postgres
```

3. 安装依赖并启动：

```bash
python3.13 -m pip install --user ".[dev]"
python3.13 -m uvicorn app.main:app --reload
```

如果本机没有 `python3.13` 命令，直接运行根目录脚本也可以：

```bash
../scripts/dev.sh
```

## 默认 Demo 账号

- 手机号：`13800000000`
- 密码：`12345678`

## 验证

```bash
PYTHONPATH=. DATABASE_URL=sqlite+pysqlite:////private/tmp/meituan_cloud_fridge_verify.db AUTO_CREATE_TABLES=true AUTO_SEED_DEMO_DATA=true python3.13 scripts/verify_demo_flow.py
```
