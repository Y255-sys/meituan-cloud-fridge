import { Link } from "react-router-dom";

import { EmptyState } from "components/common/EmptyState";
import { ErrorState } from "components/common/ErrorState";
import { LoadingState } from "components/common/LoadingState";
import { PageHeader } from "components/common/PageHeader";
import { useInventoryQuery } from "features/inventory/hooks";
import { useProfileQuery } from "features/profile/hooks";
import { useRecommendationsQuery } from "features/recipe/hooks";

export function HomePage() {
  const profileQuery = useProfileQuery();
  const inventoryQuery = useInventoryQuery({});
  const recommendationQuery = useRecommendationsQuery("worker_evening");

  if (profileQuery.isLoading || inventoryQuery.isLoading || recommendationQuery.isLoading) {
    return <LoadingState text="正在准备今晚的家庭晚饭看板..." />;
  }

  if (profileQuery.error || inventoryQuery.error || recommendationQuery.error) {
    return <ErrorState message="首页信息加载失败，请检查后端或切换 Mock 模式。" />;
  }

  if (!profileQuery.data || !inventoryQuery.data || !recommendationQuery.data) {
    return <EmptyState title="首页信息暂不可用" description="请稍后重试，或者重新登录后再进入首页。" />;
  }

  const profile = profileQuery.data;
  const inventory = inventoryQuery.data;
  const firstGroup = recommendationQuery.data.groups[0];

  return (
    <>
      <PageHeader
        title={`晚上好，${profile.nickname}`}
        description="先看家里有什么，再决定今晚吃什么、差什么、要不要补购。"
        actions={
          <div className="hero-cta-group">
            <Link className="primary-button" to="/recognize">
              拍照识别入库
            </Link>
            <Link className="secondary-button" to="/recipes">
              看今晚推荐
            </Link>
          </div>
        }
      />
      <section className="metric-grid">
        <article className="metric-card panel">
          <span>家庭库存总数</span>
          <strong>{inventory.summary.total_items}</strong>
          <p>今天随时可调度的家庭食材</p>
        </article>
        <article className="metric-card panel warm-card">
          <span>临期提醒</span>
          <strong>{inventory.summary.expiring_items}</strong>
          <p>建议优先做掉，减少浪费</p>
        </article>
        <article className="metric-card panel green-card">
          <span>爸妈模式</span>
          <strong>{profile.senior_mode_enabled ? "已开启" : "未开启"}</strong>
          <p>适合大字版和亲情代付</p>
        </article>
      </section>
      <section className="two-column">
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>今日库存摘要</h3>
              <p>{profile.household_name} 当前最适合先处理的食材</p>
            </div>
            <Link className="secondary-button" to="/inventory">
              去管理
            </Link>
          </div>
          {inventory.items.length ? (
            <div className="stack-list">
              {inventory.items.slice(0, 4).map((item) => (
                <div className="mini-card" key={item.id}>
                  <strong>{item.ingredient_name}</strong>
                  <p>
                    {item.quantity}
                    {item.unit} · {item.storage_location}
                  </p>
                  <span className="mini-hint">{item.status === "expiring" ? "建议今天优先消耗" : "库存状态良好"}</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="还没有库存" description="先去识别或手动添加一些食材。" />
          )}
        </article>
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>今晚优先推荐</h3>
              <p>{firstGroup.title}</p>
            </div>
            <Link className="secondary-button" to="/recipes">
              展开全部
            </Link>
          </div>
          {firstGroup.recipes.length ? (
            <div className="stack-list">
              {firstGroup.recipes.map((recipe) => (
                <div className="mini-card" key={recipe.recipe_id}>
                  <strong>{recipe.recipe_name}</strong>
                  <p>
                    {recipe.cook_time_minutes} 分钟 · {recipe.match_score} 分匹配
                  </p>
                  <span className="mini-hint">{recipe.highlight_reason}</span>
                </div>
              ))}
            </div>
          ) : (
            <EmptyState title="暂时没有推荐" description="补充库存后就能生成更准确的晚饭建议。" />
          )}
        </article>
      </section>
    </>
  );
}
