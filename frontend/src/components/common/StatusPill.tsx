export function StatusPill({ status }: { status: "fresh" | "expiring" | "expired" }) {
  const textMap = {
    fresh: "新鲜",
    expiring: "临期",
    expired: "过期",
  };
  return <span className={`status-pill status-${status}`}>{textMap[status]}</span>;
}
