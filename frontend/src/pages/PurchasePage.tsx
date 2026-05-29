import { useMemo, useState } from "react";
import { useSearchParams } from "react-router-dom";

import { EmptyState } from "components/common/EmptyState";
import { PageHeader } from "components/common/PageHeader";
import { PurchasePlanView } from "components/purchase/PurchasePlanView";
import { useProfileQuery } from "features/profile/hooks";
import { useCheckoutRedirectMutation, useProductMatchMutation, usePurchasePlanMutation } from "features/purchase/hooks";

export function PurchasePage() {
  const [searchParams] = useSearchParams();
  const recipeIds = useMemo(() => (searchParams.get("recipeIds") ? [searchParams.get("recipeIds") as string] : ["rcp_beef_pepper"]), [searchParams]);
  const [strategy, setStrategy] = useState<"lowest_cost" | "minimum_items">("lowest_cost");

  const profileQuery = useProfileQuery();
  const planMutation = usePurchasePlanMutation();
  const productMatchMutation = useProductMatchMutation();
  const checkoutMutation = useCheckoutRedirectMutation();

  const selectedProductIds = productMatchMutation.data?.products.map((product) => product.matched_product_id) ?? [];

  return (
    <>
      <PageHeader title="补购结算页" description="这里清楚展示缺失食材、商品匹配、优惠解释，以及最后的下单或代付动作。" />
      <section className="panel section-panel">
        <div className="section-heading">
          <div>
            <h3>补购策略</h3>
            <p>主链路里优先展示“低成本补齐”和“少件数更适合爸妈”。</p>
          </div>
        </div>
        <div className="hero-cta-group">
          <button className={strategy === "lowest_cost" ? "primary-button" : "secondary-button"} onClick={() => setStrategy("lowest_cost")} type="button">
            省钱优先
          </button>
          <button className={strategy === "minimum_items" ? "primary-button" : "secondary-button"} onClick={() => setStrategy("minimum_items")} type="button">
            少件数优先
          </button>
          <button
            className="primary-button"
            disabled={planMutation.isPending}
            onClick={() => {
              void planMutation.mutate({ recipeIds, strategy });
            }}
            type="button"
          >
            {planMutation.isPending ? "生成中..." : "生成补购方案"}
          </button>
          <button
            className="secondary-button"
            disabled={!planMutation.data || productMatchMutation.isPending}
            onClick={() => {
              if (!planMutation.data) {
                return;
              }
              void productMatchMutation.mutate(planMutation.data.plan_id);
            }}
            type="button"
          >
            {productMatchMutation.isPending ? "匹配中..." : "匹配商品"}
          </button>
        </div>
        {planMutation.error ? <p className="form-error">{planMutation.error.message}</p> : null}
        {productMatchMutation.error ? <p className="form-error">{productMatchMutation.error.message}</p> : null}
      </section>
      {planMutation.data ? (
        <>
          <PurchasePlanView plan={planMutation.data} productMatch={productMatchMutation.data ?? null} />
          <section className="panel section-panel">
            <div className="section-heading">
              <div>
                <h3>下单跳转与代付</h3>
                <p>最后一步展示平台承接能力，尤其是爸妈模式下的亲情代付。</p>
              </div>
            </div>
            <div className="stack-list">
              <button
                className="primary-button"
                disabled={!selectedProductIds.length || checkoutMutation.isPending}
                onClick={() => {
                  void checkoutMutation.mutate({
                    selectedProductIds,
                    seniorModeDelegatePay: profileQuery.data?.senior_mode_enabled ?? false,
                  });
                }}
                type="button"
              >
                {checkoutMutation.isPending ? "生成中..." : "生成下单跳转"}
              </button>
              {checkoutMutation.data ? (
                <div className="mini-card">
                  <strong>下单链接</strong>
                  <a href={checkoutMutation.data.checkout_url} rel="noreferrer" target="_blank">
                    {checkoutMutation.data.checkout_url}
                  </a>
                  <span className="mini-hint">{checkoutMutation.data.delegate_pay.share_message}</span>
                </div>
              ) : null}
              {checkoutMutation.error ? <p className="form-error">{checkoutMutation.error.message}</p> : null}
            </div>
          </section>
        </>
      ) : (
        <EmptyState title="还没生成补购方案" description="从推荐页带着菜谱过来，或者直接点上面的按钮生成一套演示方案。" />
      )}
    </>
  );
}
