import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { EmptyState } from "components/common/EmptyState";
import { ErrorState } from "components/common/ErrorState";
import { LoadingState } from "components/common/LoadingState";
import { PageHeader } from "components/common/PageHeader";
import { RecommendationGroup } from "components/recipe/RecommendationGroup";
import { useMissingAnalysisMutation, useRecipeDetailQuery, useRecommendationsQuery } from "features/recipe/hooks";

const scenes = [
  { value: "worker_evening", label: "打工人晚饭决策" },
  { value: "family_save_money", label: "家庭采购省钱" },
  { value: "senior_simple", label: "爸妈模式简单做" },
];

export function RecipesPage() {
  const navigate = useNavigate();
  const [scene, setScene] = useState("worker_evening");
  const [selectedRecipeId, setSelectedRecipeId] = useState<string | null>(null);

  const recommendationsQuery = useRecommendationsQuery(scene);
  const recipeDetailQuery = useRecipeDetailQuery(selectedRecipeId);
  const missingAnalysisMutation = useMissingAnalysisMutation();

  useEffect(() => {
    if (!recommendationsQuery.data) {
      return;
    }
    const firstRecipe = recommendationsQuery.data.groups.flatMap((group) => group.recipes)[0];
    if (firstRecipe) {
      setSelectedRecipeId(firstRecipe.recipe_id);
    }
  }, [recommendationsQuery.data]);

  const selectedRecipeName = useMemo(() => recipeDetailQuery.data?.recipe_name ?? "当前菜谱", [recipeDetailQuery.data]);

  if (recommendationsQuery.isLoading) {
    return <LoadingState text="正在根据库存生成今晚推荐..." />;
  }

  if (recommendationsQuery.error) {
    return <ErrorState message="推荐页加载失败，请稍后重试。" />;
  }

  if (!recommendationsQuery.data) {
    return <EmptyState title="暂时没有推荐结果" description="请先补充库存，或者稍后重新生成推荐。" />;
  }

  return (
    <>
      <PageHeader
        title="菜谱推荐"
        description="清楚分成三类：不补购就能做、少量补购就能做、直接外卖替代。"
        actions={
          <select className="scene-select" value={scene} onChange={(event) => setScene(event.target.value)}>
            {scenes.map((item) => (
              <option key={item.value} value={item.value}>
                {item.label}
              </option>
            ))}
          </select>
        }
      />
      <div className="stack-list">
        {recommendationsQuery.data.groups.map((group) => (
          <RecommendationGroup group={group} key={group.type} onSelectRecipe={setSelectedRecipeId} />
        ))}
      </div>
      <section className="two-column">
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>菜谱详情</h3>
              <p>{selectedRecipeName}</p>
            </div>
          </div>
          {recipeDetailQuery.isLoading ? <LoadingState text="正在读取菜谱详情..." /> : null}
          {recipeDetailQuery.error ? <ErrorState message="菜谱详情加载失败。" /> : null}
          {recipeDetailQuery.data ? (
            <div className="stack-list">
              <div className="mini-card">
                <strong>{recipeDetailQuery.data.recipe_name}</strong>
                <p>
                  {recipeDetailQuery.data.cook_time_minutes} 分钟 · {recipeDetailQuery.data.difficulty}
                </p>
                <span className="mini-hint">{recipeDetailQuery.data.description}</span>
              </div>
              <div className="mini-card">
                <strong>所需食材</strong>
                <div className="stack-list compact-gap">
                  {recipeDetailQuery.data.ingredients.map((ingredient) => (
                    <div className="ingredient-row" key={`${ingredient.ingredient_name}-${ingredient.unit}`}>
                      <span>
                        {ingredient.ingredient_name} · {ingredient.required_quantity}
                        {ingredient.unit}
                      </span>
                      <span>{ingredient.missing_quantity > 0 ? `还差 ${ingredient.missing_quantity}${ingredient.unit}` : "已具备"}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <EmptyState title="请选择一个菜谱" description="上面任意点开一个推荐项，就能看到详细食材和步骤。" />
          )}
        </article>
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>缺失分析</h3>
              <p>选中一个菜谱后，直接分析还差哪些食材。</p>
            </div>
          </div>
          <div className="stack-list">
            <button
              className="primary-button"
              disabled={!selectedRecipeId || missingAnalysisMutation.isPending}
              onClick={() => {
                if (!selectedRecipeId) {
                  return;
                }
                void missingAnalysisMutation.mutate([selectedRecipeId]);
              }}
              type="button"
            >
              {missingAnalysisMutation.isPending ? "分析中..." : "分析缺失食材"}
            </button>
            {missingAnalysisMutation.data ? (
              <>
                {missingAnalysisMutation.data.aggregated_missing.length ? (
                  <>
                    {missingAnalysisMutation.data.aggregated_missing.map((item) => (
                      <div className="mini-card" key={`${item.ingredient_name}-${item.unit}`}>
                        <strong>{item.ingredient_name}</strong>
                        <p>
                          还差 {item.missing_quantity}
                          {item.unit}
                        </p>
                      </div>
                    ))}
                    <button
                      className="secondary-button"
                      onClick={() => navigate(`/purchase?recipeIds=${selectedRecipeId}`)}
                      type="button"
                    >
                      去生成补购方案
                    </button>
                  </>
                ) : (
                  <EmptyState title="这个菜谱不用补购" description="已经具备全部关键食材，可以直接开做。" />
                )}
              </>
            ) : (
              <p className="muted">点击上面的按钮后，这里会展示缺口和补购入口。</p>
            )}
            {missingAnalysisMutation.error ? <p className="form-error">{missingAnalysisMutation.error.message}</p> : null}
          </div>
        </article>
      </section>
    </>
  );
}
