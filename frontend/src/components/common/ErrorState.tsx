export function ErrorState({ message = "加载失败，请稍后重试。" }: { message?: string }) {
  return <div className="panel error-center">{message}</div>;
}
