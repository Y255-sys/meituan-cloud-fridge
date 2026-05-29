import { useMemo, useState } from "react";

import { ErrorState } from "components/common/ErrorState";
import { LoadingState } from "components/common/LoadingState";
import { PageHeader } from "components/common/PageHeader";
import { useImportRecognitionMutation } from "features/inventory/hooks";
import { useRecognitionMutation } from "features/recognition/hooks";
import type { RecognitionItem } from "types/contracts";

export function RecognizePage() {
  const recognitionMutation = useRecognitionMutation();
  const importMutation = useImportRecognitionMutation();

  const [scene, setScene] = useState("fridge");
  const [file, setFile] = useState<File | null>(null);
  const [editableItems, setEditableItems] = useState<RecognitionItem[]>([]);
  const [importError, setImportError] = useState("");

  const recognitionId = recognitionMutation.data?.recognition_id ?? null;

  const canImport = useMemo(() => editableItems.length > 0 && recognitionId, [editableItems, recognitionId]);

  const handleRecognize = async () => {
    if (!file) {
      return;
    }
    const result = await recognitionMutation.mutateAsync({ file, scene });
    setEditableItems(result.items);
  };

  const handleImport = async () => {
    if (!recognitionId) {
      return;
    }
    const invalidItem = editableItems.find((item) => !item.ingredient_name.trim() || item.quantity <= 0);
    if (invalidItem) {
      setImportError("请先把识别结果补全：食材名不能为空，数量必须大于 0。");
      return;
    }
    await importMutation.mutateAsync({
      recognition_id: recognitionId,
      items: editableItems.map((item) => ({
        ingredient_base_id: item.ingredient_base_id,
        ingredient_name: item.ingredient_name.trim(),
        quantity: item.quantity,
        unit: item.unit,
        storage_location: item.suggested_storage_location,
        expire_at: null,
      })),
    });
    setImportError("");
  };

  return (
    <>
      <PageHeader title="拍照识别入库" description="先识别，再允许用户手动修正，最后再入库到家庭云冰箱。" />
      <section className="two-column">
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>上传食材图片</h3>
              <p>为了演示稳定，mock 模式下上传任意图片都能返回结构化识别结果。</p>
            </div>
          </div>
          <div className="stack-form">
            <label>
              识别场景
              <select value={scene} onChange={(event) => setScene(event.target.value)}>
                <option value="fridge">冰箱内</option>
                <option value="countertop">台面食材</option>
                <option value="shopping_bag">购物袋</option>
              </select>
            </label>
            <label>
              选择图片
              <input accept="image/*" onChange={(event) => setFile(event.target.files?.[0] ?? null)} type="file" />
            </label>
            <button className="primary-button" disabled={!file || recognitionMutation.isPending} onClick={handleRecognize} type="button">
              {recognitionMutation.isPending ? "识别中..." : "开始识别"}
            </button>
          </div>
        </article>
        <article className="panel section-panel">
          <div className="section-heading">
            <div>
              <h3>识别后确认</h3>
              <p>这是给黑客松 Demo 留出的关键交互：识别结果必须可人工修正。</p>
            </div>
          </div>
          {recognitionMutation.isPending ? <LoadingState text="正在识别食材..." /> : null}
          {recognitionMutation.error ? <ErrorState message={recognitionMutation.error.message} /> : null}
          {editableItems.length ? (
            <div className="stack-list">
              {editableItems.map((item) => (
                <div className="mini-card" key={item.temp_id}>
                  <div className="grid-two">
                    <label>
                      食材名
                      <input
                        value={item.ingredient_name}
                        onChange={(event) =>
                          setEditableItems((prev) =>
                            prev.map((entry) => (entry.temp_id === item.temp_id ? { ...entry, ingredient_name: event.target.value } : entry)),
                          )
                        }
                      />
                    </label>
                    <label>
                      数量
                      <input
                        type="number"
                        value={item.quantity}
                        onChange={(event) =>
                          setEditableItems((prev) =>
                            prev.map((entry) =>
                              entry.temp_id === item.temp_id ? { ...entry, quantity: Number(event.target.value) || 0 } : entry,
                            ),
                          )
                        }
                      />
                    </label>
                  </div>
                  <span className="mini-hint">
                    置信度 {(item.confidence * 100).toFixed(0)}% · 建议 {item.suggested_storage_location}
                  </span>
                </div>
              ))}
              <button className="primary-button" disabled={!canImport || importMutation.isPending} onClick={handleImport} type="button">
                {importMutation.isPending ? "入库中..." : "确认并入库"}
              </button>
              {importError ? <p className="form-error">{importError}</p> : null}
              {importMutation.error ? <p className="form-error">{importMutation.error.message}</p> : null}
              {importMutation.isSuccess ? <p className="success-note">已成功入库 {importMutation.data.imported_count} 项。</p> : null}
            </div>
          ) : (
            <p className="muted">上传后这里会出现可编辑的识别结果。</p>
          )}
        </article>
      </section>
    </>
  );
}
