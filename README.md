# 美团云冰箱

一个面向黑客松 Demo 的全栈项目重构版本，目标是把“家庭真实库存 -> 晚饭决策 -> 缺货分析 -> 补购/外卖跳转”做成一条稳定、可演示、可扩展的主链路。

## 当前阶段

- `第一阶段：架构与契约设计` 已完成
- `第二阶段：后端从 0 搭建` 已完成
- `第三阶段：前端从 0 搭建` 已完成
- `第四阶段：联调与演示收口` 已完成

## 目录约定

后续所有新代码、文档、脚本都放在当前目录下，不复用旧仓库结构。

```text
meituan-cloud-fridge/
├── README.md
├── docs/
│   └── stage-1-architecture.md
├── frontend/                # 第二阶段后创建
├── backend/                 # 第二阶段后创建
├── infra/                   # docker、env、seed、脚本
└── scripts/                 # 一键启动、校验脚本
```

## 第一阶段文档

- 架构与契约设计：[docs/stage-1-architecture.md](/Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/docs/stage-1-architecture.md)
- 本地运行手册：[docs/local-run-guide.md](/Users/yujingyi/Desktop/研1下/美团黑客松/0522/meituan-cloud-fridge/docs/local-run-guide.md)

## 下一步

确认第一阶段方案后，直接进入：

1. FastAPI + PostgreSQL 后端脚手架
2. 核心数据模型与统一 API 返回结构
3. Mock 识别、推荐、补购主链路
4. React + Vite 前端页面与联调
