import { Link } from "react-router-dom";

import { PageHeader } from "components/common/PageHeader";
import { SeniorActionCard } from "components/senior-mode/SeniorActionCard";
import { useProfileQuery, useToggleSeniorModeMutation } from "features/profile/hooks";
import { useRecommendationsQuery } from "features/recipe/hooks";

export function SeniorModePage() {
  const profileQuery = useProfileQuery();
  const toggleMutation = useToggleSeniorModeMutation();
  const recommendationQuery = useRecommendationsQuery("senior_simple");

  if (!profileQuery.data) {
    return null;
  }

  return (
    <>
      <PageHeader title="爸妈模式" description="大字号、少按钮、直白文案，让长辈也能顺着流程走下去。" />
      <section className="panel senior-mode-panel">
        <div className="senior-switch-row">
          <div>
            <h2>{profileQuery.data.senior_mode_enabled ? "爸妈模式已开启" : "爸妈模式未开启"}</h2>
            <p>开启后更适合直接看库存、拍照入库、今晚吃什么、让孩子代付。</p>
          </div>
          <button
            className="primary-button extra-large-button"
            disabled={toggleMutation.isPending}
            onClick={() => void toggleMutation.mutate(!profileQuery.data?.senior_mode_enabled)}
            type="button"
          >
            {profileQuery.data.senior_mode_enabled ? "关闭大字模式" : "开启大字模式"}
          </button>
        </div>
      </section>
      <section className="senior-grid">
        <SeniorActionCard action={<Link className="primary-button extra-large-button" to="/inventory">看家里有什么</Link>} description="先看库存，再决定今晚做什么。" title="第一步：看库存" />
        <SeniorActionCard action={<Link className="primary-button extra-large-button" to="/recognize">拍照自动识别</Link>} description="不会打字也没关系，拍一张就能认。" title="第二步：拍照入库" />
        <SeniorActionCard action={<Link className="primary-button extra-large-button" to="/recipes">今晚吃什么</Link>} description="系统把能直接做的和要补一点的都分开讲清楚。" title="第三步：今晚吃什么" />
        <SeniorActionCard action={<Link className="primary-button extra-large-button" to="/purchase">发给孩子代付</Link>} description="差的食材会自动配好商品，也能直接让孩子代付。" title="第四步：一键代付" />
      </section>
      <section className="panel section-panel">
        <div className="section-heading">
          <div>
            <h3>适合爸妈的晚饭建议</h3>
            <p>更偏简单、少步骤、解释直白。</p>
          </div>
        </div>
        <div className="stack-list">
          {recommendationQuery.data?.groups[0]?.recipes.map((recipe) => (
            <div className="mini-card senior-mini-card" key={recipe.recipe_id}>
              <strong>{recipe.recipe_name}</strong>
              <p>{recipe.highlight_reason}</p>
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
