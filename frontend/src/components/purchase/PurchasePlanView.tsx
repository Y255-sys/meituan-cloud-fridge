import { formatCurrency } from "lib/utils/format";
import type { ProductMatchData, PurchasePlan } from "types/contracts";

export function PurchasePlanView({
  plan,
  productMatch,
}: {
  plan: PurchasePlan | null;
  productMatch: ProductMatchData | null;
}) {
  if (!plan) {
    return null;
  }

  return (
    <div className="two-column">
      <section className="panel section-panel">
        <div className="section-heading">
          <div>
            <h3>补购方案</h3>
            <p>{plan.promotion_explanation}</p>
          </div>
          <strong>{formatCurrency(plan.estimated_total_price)}</strong>
        </div>
        <div className="stack-list">
          {plan.items.map((item) => (
            <div className="mini-card" key={`${item.ingredient_name}-${item.unit}`}>
              <strong>{item.ingredient_name}</strong>
              <p>
                缺 {item.required_quantity}
                {item.unit} · 预计 {formatCurrency(item.estimated_price)}
              </p>
              <span className="mini-hint">{item.reason}</span>
            </div>
          ))}
        </div>
      </section>
      <section className="panel section-panel">
        <div className="section-heading">
          <div>
            <h3>商品匹配</h3>
            <p>优先匹配刚好够用的小规格，适合黑客松演示</p>
          </div>
        </div>
        {productMatch ? (
          <div className="stack-list">
            {productMatch.products.map((product) => (
              <div className="mini-card" key={product.matched_product_id}>
                <strong>{product.product_name}</strong>
                <p>
                  {formatCurrency(product.price)} · {product.discount_text}
                </p>
                <span className="mini-hint">
                  {product.merchant_name} · {product.eta_minutes} 分钟送达
                </span>
              </div>
            ))}
            {productMatch.takeout_alternatives.map((item) => (
              <div className="mini-card alt-card" key={item.merchant_id}>
                <strong>{item.dish_name}</strong>
                <p>
                  {item.merchant_name} · {formatCurrency(item.price)}
                </p>
                <span className="mini-hint">{item.reason}</span>
              </div>
            ))}
          </div>
        ) : (
          <p className="muted">先生成商品匹配结果。</p>
        )}
      </section>
    </div>
  );
}
