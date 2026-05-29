# Frontend

React + TypeScript + Vite 前端，覆盖：

- 首页
- 食材拍照识别页
- 库存管理页
- 菜谱推荐页
- 补购结算页
- 爸妈模式页

## 启动

```bash
cd /Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## 环境变量

默认读取 [`.env`](/Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/frontend/.env)：

```env
VITE_API_MODE=real
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

如需切到前端本地 mock：

```env
VITE_API_MODE=mock
VITE_API_BASE_URL=http://127.0.0.1:8000/api/v1
```

## 验证

```bash
npm run check
npm run build
```

## 页面入口

- [http://127.0.0.1:5173](http://127.0.0.1:5173)
- 默认登录账号：`13800000000 / 12345678`
