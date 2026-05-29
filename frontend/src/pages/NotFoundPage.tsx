import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="panel empty-state">
      <h2>页面不存在</h2>
      <p>这个路由还没有接进美团云冰箱的演示流程里。</p>
      <Link className="primary-button" to="/">
        回到首页
      </Link>
    </div>
  );
}
