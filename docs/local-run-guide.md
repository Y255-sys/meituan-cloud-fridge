# 美团云冰箱本地运行手册

这份文档按顺序说明如何在本机手动启动项目。

项目根目录：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge
```

## 1. 先确认本机环境

需要这些基础工具：

- `Docker Desktop`
- `Python 3.13`
- `Node.js 20+`
- `npm`

可以先执行：

```bash
docker --version
python3.13 --version
node -v
npm -v
```

如果你的机器没有 `python3.13` 命令，但装了 Miniconda，可以改用：

```bash
/opt/miniconda3/bin/python3.13 --version
```

## 2. 启动 PostgreSQL

这个项目当前的 Docker 映射端口是：

- 容器内 PostgreSQL：`5432`
- 本机访问端口：`5433`

直接启动数据库：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge
docker compose -f infra/docker/docker-compose.yml up -d postgres
```

确认容器已经起来：

```bash
docker ps
```

你应该能看到类似：

```text
meituan-cloud-fridge-postgres   0.0.0.0:5433->5432/tcp
```

## 3. 检查后端环境变量

进入后端目录：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/backend
```

如果 `.env` 不存在，先复制一份：

```bash
cp .env.example .env
```

确认 `backend/.env` 里最重要的是这一行：

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5433/meituan_cloud_fridge
```

如果你看到的是 `5432`，请改成 `5433`。

## 4. 安装后端依赖

在 `backend` 目录执行：

```bash
python3.13 -m pip install --user ".[dev]"
```

如果本机没有 `python3.13` 命令，就执行：

```bash
/opt/miniconda3/bin/python3.13 -m pip install --user ".[dev]"
```

## 5. 启动后端服务

仍然在 `backend` 目录执行：

```bash
PYTHONPATH=. python3.13 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

如果你用的是 Miniconda 里的 Python：

```bash
PYTHONPATH=. /opt/miniconda3/bin/python3.13 -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

后端启动成功后，会看到类似输出：

```text
Uvicorn running on http://127.0.0.1:8000
```

## 6. 验证后端是否正常

打开新的终端窗口，执行：

```bash
curl http://127.0.0.1:8000/health
```

预期返回：

```json
{"status":"ok"}
```

Swagger 文档地址：

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

默认 Demo 账号：

- 手机号：`13800000000`
- 密码：`12345678`

## 7. 检查前端环境变量

打开一个新的终端，进入前端目录：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/frontend
```

确认 `frontend/.env` 内容如下：

```env
VITE_API_MODE=real
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

这表示前端走真实后端接口。

## 8. 安装前端依赖

在 `frontend` 目录执行：

```bash
npm install
```

## 9. 启动前端服务

继续在 `frontend` 目录执行：

```bash
npm run dev -- --host 127.0.0.1 --port 5173
```

启动成功后，会看到类似输出：

```text
Local: http://127.0.0.1:5173/
```

## 10. 验证前端是否正常

浏览器打开：

- [http://127.0.0.1:5173/](http://127.0.0.1:5173/)

登录账号：

- 手机号：`13800000000`
- 密码：`12345678`

## 11. 推荐测试顺序

启动完成后，建议按这个顺序走一遍：

1. 登录
2. 首页看库存摘要
3. 进入库存页查看已有食材
4. 进入推荐页看三类推荐
5. 进入补购页生成补购方案
6. 进入爸妈模式看大字体和代付文案

## 12. 常见问题

### 1. 浏览器显示无法访问此站点

通常是前端或后端开发进程已经退出。

重新检查：

```bash
curl http://127.0.0.1:8000/health
curl -I http://127.0.0.1:5173
```

如果请求失败，就分别重新启动后端和前端。

### 2. 后端报数据库连接失败

优先检查两件事：

1. Docker 容器是否真的启动了
2. `backend/.env` 里的端口是不是 `5433`

可执行：

```bash
docker ps
```

### 3. `5173` 端口启动失败

说明前端端口被占用，先换一个端口试试：

```bash
npm run dev -- --host 127.0.0.1 --port 5174
```

如果换端口了，浏览器也改成：

- [http://127.0.0.1:5174/](http://127.0.0.1:5174/)

### 4. `8000` 端口启动失败

说明后端端口被占用，先找到占用进程，或者换端口：

```bash
PYTHONPATH=. python3.13 -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

如果后端改成 `8001`，记得同步修改：

- `frontend/.env`

改成：

```env
VITE_API_BASE_URL=http://127.0.0.1:8001/api/v1
```

## 13. 一键启动方式

如果你不想手动分步执行，也可以直接用项目脚本。

后端一键启动：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge
bash scripts/dev.sh
```

前端一键启动：

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge
bash scripts/dev-frontend.sh
```

但如果你是第一次跑项目，我更推荐按前面的 1 到 10 步手动来一次，这样后面排查问题会更快。
