import { useMemo, useState } from "react";

import { EmptyState } from "components/common/EmptyState";
import { ErrorState } from "components/common/ErrorState";
import { LoadingState } from "components/common/LoadingState";
import { PageHeader } from "components/common/PageHeader";
import { InventoryList } from "components/inventory/InventoryList";
import { useCreateInventoryMutation, useDeleteInventoryMutation, useInventoryQuery, useUpdateInventoryMutation } from "features/inventory/hooks";
import type { InventoryCreatePayload, InventoryItem } from "types/contracts";

const initialForm: InventoryCreatePayload = {
  ingredient_name: "",
  quantity: 1,
  unit: "个",
  storage_location: "冷藏",
  expire_at: "",
};

export function InventoryPage() {
  const [filters, setFilters] = useState({
    keyword: "",
    status: "",
    category: "",
  });
  const [form, setForm] = useState<InventoryCreatePayload>(initialForm);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  const [formError, setFormError] = useState("");

  const inventoryQuery = useInventoryQuery(filters);
  const createMutation = useCreateInventoryMutation();
  const updateMutation = useUpdateInventoryMutation();
  const deleteMutation = useDeleteInventoryMutation();

  const categories = useMemo(
    () => Array.from(new Set((inventoryQuery.data?.items ?? []).map((item) => item.category))).filter(Boolean),
    [inventoryQuery.data?.items],
  );

  const handleCreate = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!form.ingredient_name.trim()) {
      setFormError("请先填写食材名称。");
      return;
    }
    if (form.quantity <= 0) {
      setFormError("数量必须大于 0。");
      return;
    }
    await createMutation.mutateAsync({
      ...form,
      ingredient_name: form.ingredient_name.trim(),
      expire_at: form.expire_at || null,
    });
    setFormError("");
    setForm(initialForm);
  };

  if (inventoryQuery.isLoading) {
    return <LoadingState text="正在读取家庭库存..." />;
  }

  if (inventoryQuery.error) {
    return <ErrorState message="库存加载失败，请稍后重试。" />;
  }

  if (!inventoryQuery.data) {
    return <EmptyState title="库存暂不可用" description="请稍后再试，或者先确认后端服务是否正常。" />;
  }

  return (
    <>
      <PageHeader title="库存管理" description="支持筛选、临期标记、手动增删改，是家庭真实库存的主工作台。" />
      <section className="two-column wide-left">
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>筛选与列表</h3>
              <p>
                当前共 {inventoryQuery.data.summary.total_items} 项，临期 {inventoryQuery.data.summary.expiring_items} 项
              </p>
            </div>
          </div>
          <div className="filter-row">
            <input
              placeholder="搜索食材"
              value={filters.keyword}
              onChange={(event) => setFilters((prev) => ({ ...prev, keyword: event.target.value }))}
            />
            <select value={filters.status} onChange={(event) => setFilters((prev) => ({ ...prev, status: event.target.value }))}>
              <option value="">全部状态</option>
              <option value="fresh">新鲜</option>
              <option value="expiring">临期</option>
              <option value="expired">过期</option>
            </select>
            <select value={filters.category} onChange={(event) => setFilters((prev) => ({ ...prev, category: event.target.value }))}>
              <option value="">全部分类</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>
          {inventoryQuery.data.items.length ? (
            <InventoryList
              items={inventoryQuery.data.items}
              onDelete={(itemId) => {
                void deleteMutation.mutateAsync(itemId);
              }}
              onEdit={(item) => setEditingItem(item)}
            />
          ) : (
            <EmptyState title="暂无库存" description="先从识别页或右侧手动新增一些食材。" />
          )}
        </article>
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>{editingItem ? "编辑库存" : "手动新增"}</h3>
              <p>给没被识别到的食材补录，或纠正库存数量。</p>
            </div>
          </div>
          <form className="stack-form" onSubmit={handleCreate}>
            <label>
              食材名
              <input
                value={editingItem?.ingredient_name ?? form.ingredient_name}
                onChange={(event) =>
                  editingItem
                    ? setEditingItem({ ...editingItem, ingredient_name: event.target.value })
                    : setForm((prev) => ({ ...prev, ingredient_name: event.target.value }))
                }
              />
            </label>
            <div className="grid-two">
              <label>
                数量
                <input
                  type="number"
                  value={editingItem?.quantity ?? form.quantity}
                  onChange={(event) =>
                    editingItem
                      ? setEditingItem({ ...editingItem, quantity: Number(event.target.value) || 0 })
                      : setForm((prev) => ({ ...prev, quantity: Number(event.target.value) || 0 }))
                  }
                />
              </label>
              <label>
                单位
                <input
                  value={editingItem?.unit ?? form.unit}
                  onChange={(event) =>
                    editingItem ? setEditingItem({ ...editingItem, unit: event.target.value }) : setForm((prev) => ({ ...prev, unit: event.target.value }))
                  }
                />
              </label>
            </div>
            <div className="grid-two">
              <label>
                储存方式
                <select
                  value={editingItem?.storage_location ?? form.storage_location}
                  onChange={(event) =>
                    editingItem
                      ? setEditingItem({ ...editingItem, storage_location: event.target.value as InventoryItem["storage_location"] })
                      : setForm((prev) => ({ ...prev, storage_location: event.target.value as InventoryCreatePayload["storage_location"] }))
                  }
                >
                  <option value="冷藏">冷藏</option>
                  <option value="冷冻">冷冻</option>
                  <option value="常温">常温</option>
                </select>
              </label>
              <label>
                到期日期
                <input
                  type="date"
                  value={editingItem?.expire_at?.slice(0, 10) ?? (form.expire_at ?? "")}
                  onChange={(event) =>
                    editingItem
                      ? setEditingItem({ ...editingItem, expire_at: event.target.value })
                      : setForm((prev) => ({ ...prev, expire_at: event.target.value }))
                  }
                />
              </label>
            </div>
            {editingItem ? (
              <div className="hero-cta-group">
                <button
                  className="primary-button"
                  disabled={!editingItem.ingredient_name.trim() || editingItem.quantity <= 0 || updateMutation.isPending}
                  onClick={async () => {
                    if (!editingItem.ingredient_name.trim()) {
                      setFormError("编辑时也需要填写食材名称。");
                      return;
                    }
                    if (editingItem.quantity <= 0) {
                      setFormError("编辑数量必须大于 0。");
                      return;
                    }
                    await updateMutation.mutateAsync({
                      itemId: editingItem.id,
                      payload: {
                        ingredient_name: editingItem.ingredient_name.trim(),
                        quantity: editingItem.quantity,
                        unit: editingItem.unit,
                        storage_location: editingItem.storage_location,
                        expire_at: editingItem.expire_at,
                      },
                    });
                    setFormError("");
                    setEditingItem(null);
                  }}
                  type="button"
                >
                  保存修改
                </button>
                <button className="ghost-button" onClick={() => setEditingItem(null)} type="button">
                  取消编辑
                </button>
              </div>
            ) : (
              <button className="primary-button" disabled={createMutation.isPending} type="submit">
                {createMutation.isPending ? "新增中..." : "新增到库存"}
              </button>
            )}
            {formError ? <p className="form-error">{formError}</p> : null}
            {createMutation.error ? <p className="form-error">{createMutation.error.message}</p> : null}
            {updateMutation.error ? <p className="form-error">{updateMutation.error.message}</p> : null}
          </form>
        </article>
      </section>
    </>
  );
}
