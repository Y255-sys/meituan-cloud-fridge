import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useLoginMutation, useRegisterMutation } from "features/auth/hooks";
import { setToken } from "lib/utils/storage";

export function LoginPage() {
  const navigate = useNavigate();
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({
    phone: "13800000000",
    password: "12345678",
    nickname: "小王",
  });

  const loginMutation = useLoginMutation();
  const registerMutation = useRegisterMutation();
  const mutation = isRegister ? registerMutation : loginMutation;

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const result = isRegister
      ? await registerMutation.mutateAsync({
          phone: form.phone,
          password: form.password,
          nickname: form.nickname,
        })
      : await loginMutation.mutateAsync({
          phone: form.phone,
          password: form.password,
        });
    setToken(result.token);
    navigate("/");
  };

  return (
    <div className="auth-shell">
      <section className="auth-panel">
        <span className="eyebrow-tag">黑客松 Demo</span>
        <h1>今晚吃什么，从家里真实库存开始</h1>
        <p>美团云冰箱把“库存、做饭、补购、外卖、代付”压成一条可演示主链路。</p>
        <div className="demo-account">
          <strong>体验账号</strong>
          <span>手机号 13800000000</span>
          <span>密码 12345678</span>
        </div>
      </section>
      <form className="auth-form panel" onSubmit={handleSubmit}>
        <div className="tab-row">
          <button className={!isRegister ? "primary-tab" : "secondary-tab"} onClick={() => setIsRegister(false)} type="button">
            登录
          </button>
          <button className={isRegister ? "primary-tab" : "secondary-tab"} onClick={() => setIsRegister(true)} type="button">
            注册
          </button>
        </div>
        <label>
          手机号
          <input value={form.phone} onChange={(event) => setForm((prev) => ({ ...prev, phone: event.target.value }))} />
        </label>
        {isRegister ? (
          <label>
            昵称
            <input value={form.nickname} onChange={(event) => setForm((prev) => ({ ...prev, nickname: event.target.value }))} />
          </label>
        ) : null}
        <label>
          密码
          <input
            type="password"
            value={form.password}
            onChange={(event) => setForm((prev) => ({ ...prev, password: event.target.value }))}
          />
        </label>
        {mutation.error ? <p className="form-error">{mutation.error.message}</p> : null}
        <button className="primary-button large-button" disabled={mutation.isPending} type="submit">
          {mutation.isPending ? "提交中..." : isRegister ? "注册并进入" : "登录并进入"}
        </button>
      </form>
    </div>
  );
}
