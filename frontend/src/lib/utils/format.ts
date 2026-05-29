export function formatExpireText(daysToExpire: number | null) {
  if (daysToExpire === null) {
    return "未设置保质期";
  }
  if (daysToExpire < 0) {
    return `已过期 ${Math.abs(daysToExpire)} 天`;
  }
  if (daysToExpire === 0) {
    return "今天到期";
  }
  return `${daysToExpire} 天后到期`;
}

export function formatCurrency(value: number) {
  return `¥${value.toFixed(1)}`;
}

export function formatDate(value: string | null) {
  if (!value) {
    return "未设置";
  }
  return new Date(value).toLocaleDateString("zh-CN", {
    month: "numeric",
    day: "numeric",
  });
}

