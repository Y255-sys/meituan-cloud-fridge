import type { ReactNode } from "react";

export function SeniorActionCard({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action: ReactNode;
}) {
  return (
    <div className="panel senior-card">
      <h3>{title}</h3>
      <p>{description}</p>
      <div>{action}</div>
    </div>
  );
}
