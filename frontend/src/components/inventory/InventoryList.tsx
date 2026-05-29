import { formatDate, formatExpireText } from "lib/utils/format";
import type { InventoryItem } from "types/contracts";

import { StatusPill } from "components/common/StatusPill";

export function InventoryList({
  items,
  onEdit,
  onDelete,
}: {
  items: InventoryItem[];
  onEdit: (item: InventoryItem) => void;
  onDelete: (itemId: string) => void;
}) {
  return (
    <div className="stack-list">
      {items.map((item) => (
        <article className="panel list-item-card" key={item.id}>
          <div className="list-item-main">
            <div>
              <div className="list-title-row">
                <strong>{item.ingredient_name}</strong>
                <StatusPill status={item.status} />
              </div>
              <p className="muted">
                {item.quantity}
                {item.unit} · {item.storage_location} · {item.category}
              </p>
              <p className="muted">
                到期：{formatDate(item.expire_at)} · {formatExpireText(item.days_to_expire)}
              </p>
            </div>
            <div className="row-actions">
              <button className="secondary-button" onClick={() => onEdit(item)} type="button">
                编辑
              </button>
              <button className="ghost-button danger-button" onClick={() => onDelete(item.id)} type="button">
                删除
              </button>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
