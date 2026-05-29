import type { RecommendationGroup as RecommendationGroupType } from "types/contracts";
import { resolveRecipeImage } from "lib/utils/images";

export function RecommendationGroup({
  group,
  onSelectRecipe,
}: {
  group: RecommendationGroupType;
  onSelectRecipe: (recipeId: string) => void;
}) {
  return (
    <section className="panel section-panel">
      <div className="section-heading">
        <div>
          <h3>{group.title}</h3>
          <p>{group.description}</p>
        </div>
      </div>
      <div className="recipe-grid">
        {group.recipes.map((recipe) => (
          <button className="recipe-card" key={recipe.recipe_id} onClick={() => onSelectRecipe(recipe.recipe_id)} type="button">
            <img
              alt={recipe.recipe_name}
              className="recipe-image-tag"
              src={resolveRecipeImage(recipe.cover_image, recipe.recipe_name, group.title)}
            />
            <div className="recipe-content">
              <div className="badge-row">
                <span className="soft-badge">{recipe.match_score} 分匹配</span>
                <span className="soft-badge">{recipe.cook_time_minutes} 分钟</span>
              </div>
              <strong>{recipe.recipe_name}</strong>
              <p>{recipe.highlight_reason}</p>
            </div>
          </button>
        ))}
      </div>
    </section>
  );
}
