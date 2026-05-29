export function LoadingState({ text = "正在加载..." }: { text?: string }) {
  return <div className="panel subtle-center">{text}</div>;
}
