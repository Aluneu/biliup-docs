# 登录方式详解

biliup 支持 **5 种 B站账号登录方式**，适用于不同使用场景。登录成功后 Cookie 会自动保存，通常有效期 1-3 个月，过期后需重新登录。

> [!TIP]
> 推荐优先使用**扫码登录**，最安全也最便捷。如无法使用扫码，再根据场景选择其他方式。

---

## 方式一：扫码登录（推荐）

适用于所有场景，手机端 B站 App 扫码即可，无需输入密码。

### WebUI 操作

1. 进入「投稿管理」→ 点击左上角「新增」
2. 选择「扫码登录」
3. 使用哔哩哔哩 App 扫描屏幕上显示的二维码
4. 手机确认登录后，页面自动刷新，显示账号信息

### CLI 操作

```bash
biliup login
# 终端会显示二维码链接，浏览器打开后扫码确认
```

> ✅ 登录成功后 Cookie 自动保存，无需重复登录。

---

## 方式二：短信登录

适用于手机在身边但无法扫码的场景。

### WebUI 操作

1. 进入「投稿管理」→「新增账号」
2. 选择「短信登录」
3. 输入绑定的手机号
4. 点击「获取验证码」，填入收到的短信验证码
5. 确认登录

### CLI 操作

```bash
biliup login --sms
# 按提示输入手机号和验证码
```

> [!WARNING]
> 短信登录需要账号已绑定手机号。如开启两步验证，仍需通过 App 确认。

---

## 方式三：账号密码登录

适用于自动化环境或无手机的场景。**不推荐日常使用**，因为存在账号安全风险。

### CLI 操作

```bash
biliup login --username YOUR_USERNAME --password YOUR_PASSWORD
```

> [!WARNING]
> 在命令行中直接传密码可能被 Shell 历史记录捕获。**推荐使用环境变量或扫码登录**。
> 
> 部分账号开启了风控，密码登录可能被拒绝，此时请改用扫码登录。

---

## 方式四：浏览器登录

适用于想在浏览器中手动登录、然后将登录态导入 biliup 的场景。

### 操作步骤

1. 在浏览器中正常登录 [bilibili 主页](https://www.bilibili.com)
2. 登录后，在浏览器地址栏确认已登录状态
3. 打开浏览器开发者工具（F12）→「应用」/「Application」→「Cookie」
4. 导出 `bilibili.com` 域名下的所有 Cookie
5. 将 Cookie 内容保存为 `cookies.json` 文件
6. 在 biliup 的「空间配置」→「各平台设置」→「哔哩哔哩」中，选择该 Cookie 文件

### 使用 Playwright/Selenium 自动化（进阶）

开发者可通过浏览器自动化工具完成登录并自动提取 Cookie，适合 CI/CD 环境。

> [!TIP]
> 详见[开发者选项文档](/guide/introduce/Config/developerOptions.html)中的相关说明。

---

## 方式五：网页 Cookie 文件登录

适用于已有 Cookie 文件，或希望通过第三方工具获取 Cookie 的场景。

### Cookie 文件格式

biliup 支持两种 Cookie 文件格式：

**格式一：Netscape Cookie 文件**（推荐，`curl -c` 导出）

```text
# Netscape HTTP Cookie File
.bilibili.com	TRUE	/	TRUE	0	buvid3	xxxxxxxx
.bilibili.com	TRUE	/	FALSE	0	i-wanna-go-back	-1
...
```

**格式二：JSON 格式**

```json
[
  {"name": "buvid3", "value": "xxxxx", "domain": ".bilibili.com"},
  {"name": "DedeUserID", "value": "123456", "domain": ".bilibili.com"}
]
```

### 获取 Cookie 文件的方式

| 工具 | 方式 |
|---|---|
| 浏览器扩展（EditThisCookie 等） | 登录后导出为 JSON |
| `curl -c cookies.txt` | 通过 API 登录后保存 |
| 浏览器开发者工具 | 手动复制 Cookie 字符串 |

### 在 biliup 中配置

1. 将 Cookie 文件放到 biliup 配置目录
   - Windows：`%APPDATA%\biliup\cookies.json`
   - Linux/macOS：`~/.config/biliup/cookies.json`
2. 在 WebUI「空间配置」→「哔哩哔哩」中指定 Cookie 文件路径
3. 保存后重启 biliup 生效

---

## 多账号管理

biliup 支持同时添加多个 B站账号：

- 不同主播可以指定不同的投稿账号
- 在「投稿管理」→「账号列表」中可查看所有已登录账号的 UID、昵称、Cookie 有效期
- 点击「刷新登录」可重新扫码续期

> [!TIP]
> Cookie 有效期通常为 1-3 个月，建议定期检查和刷新，避免投稿失败。

---

## 登录失败排查

| 问题 | 可能原因 | 解决方案 |
|---|---|---|
| 扫码后无反应 | 二维码已过期 | 刷新页面重新获取二维码 |
| 短信验证码收不到 | 手机号未绑定或运营商拦截 | 改用扫码登录 |
| 密码登录被拒绝 | 账号开启风控 | 改用扫码登录 |
| Cookie 登录无效 | Cookie 已过期或格式错误 | 重新获取 Cookie 文件 |
| 上传时提示「未登录」| Cookie 已过期 | 重新登录，刷新 Cookie |

---

## 相关链接

- [WebUI 使用指南](/guide/webui/usage.html)
- [投稿管理](/guide/webui/usage.html#投稿管理-upload-manager)
- [开发者选项](/guide/introduce/Config/developerOptions.html)
