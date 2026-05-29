import { NavLink, Navigate, Outlet, useNavigate } from "react-router-dom";

import { runtimeConfig } from "lib/config/runtime";
import { clearToken, isAuthed } from "lib/utils/storage";

import styles from "./AppShell.module.css";

const navItems = [
  { to: "/", label: "首页" },
  { to: "/recognize", label: "识别入库" },
  { to: "/inventory", label: "库存管理" },
  { to: "/recipes", label: "菜谱推荐" },
  { to: "/purchase", label: "补购结算" },
  { to: "/senior", label: "爸妈模式" },
];

export function ProtectedLayout() {
  const navigate = useNavigate();

  if (!isAuthed()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className={styles.shell}>
      <div className={styles.container}>
        <header className={styles.topbar}>
          <div className={styles.brand}>
            <span className={styles.eyebrow}>Meituan Cloud Fridge</span>
            <h1 className={styles.title}>美团云冰箱</h1>
            <p className={styles.subtitle}>基于真实家庭库存的晚饭决策与本地生活调度中心</p>
          </div>
          <div className={styles.actions}>
            <div className={styles.modeBadge}>当前模式：{runtimeConfig.apiMode === "real" ? "真实接口" : "本地 Mock"}</div>
            <button
              className={styles.logoutButton}
              onClick={() => {
                clearToken();
                navigate("/login");
              }}
              type="button"
            >
              退出登录
            </button>
          </div>
        </header>
        <main className={styles.content}>
          <Outlet />
        </main>
      </div>
      <nav className={styles.bottomNav}>
        {navItems.map((item) => (
          <NavLink
            key={item.to}
            className={({ isActive }) => `${styles.navLink} ${isActive ? styles.navLinkActive : ""}`}
            to={item.to}
          >
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </div>
  );
}
