// 用法：Chrome 打开 xiaohongshu.com 并登录 → F12 → 点「控制台」→ 在底部 > 后面粘贴本文件全部内容 → 回车
// 保存：把输出/剪贴板内容存为 C:\Users\你的用户名\cookies.json
// 勿把 cookies 写进本 .js 文件；应保存到 xhs-cookies.json 或 %USERPROFILE%\cookies.json

(function () {
  const cookies = document.cookie.split(";").map((s) => s.trim()).filter(Boolean);
  if (cookies.length === 0) {
    console.error("document.cookie 为空：请确认已登录，且当前标签页是 xiaohongshu.com");
    return;
  }
  const list = cookies.map((pair) => {
    const i = pair.indexOf("=");
    return {
      name: pair.slice(0, i),
      value: pair.slice(i + 1),
      domain: ".xiaohongshu.com",
    };
  });
  const text = JSON.stringify(list, null, 2);
  let copied = false;
  try {
    if (typeof copy === "function") {
      copy(text);
      copied = true;
    }
  } catch (e) {}
  console.log(
    copied
      ? "✅ 已复制 " + list.length + " 条 cookie 到剪贴板"
      : "⚠️ 无法自动复制，请展开下面 JSON 全选复制"
  );
  console.log("请保存为: C:\\Users\\你的用户名\\cookies.json");
  console.log("或 vault: 0 工作流/scripts/xhs-cookies.json");
  console.log(text);
})();
