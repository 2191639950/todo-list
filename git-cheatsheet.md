# Git 速查手册（Windows / PowerShell）

> 配套项目：命令行待办清单（todo.py + GUI）
> 用法：忘了命令就翻这一页，从上往下找。

---

## 0. 一次性检查（只做一次）

```powershell
git --version            # 能打印版本号 = 已安装
git config --global --list   # 看有没有 user.name / user.email
```

如果没配过身份，补一次（配完所有项目通用，不上传任何东西，只是给提交贴作者标签）：

```powershell
git config --global user.name "你的名字"
git config --global user.email "你的邮箱@example.com"
```

---

## 1. 本地备份：三步

在项目根目录执行，**每个项目只做一次**：

```powershell
git init                                  # 建仓库，生成隐藏的 .git 目录
git add .                                 # 把所有文件放进待提交清单
git commit -m "CLI + GUI first working version"   # 拍一张快照
```

验证是否成功：

```powershell
git log --oneline          # 能看到刚才那条记录就对了
```

---

## 2. 日常只记这两条

改完代码、自己验证功能正常之后：

```powershell
git add .
git commit -m "加了状态栏"
```

查看当前状态（改了哪些文件、哪些还没提交）：

```powershell
git status
```

查看历史快照：

```powershell
git log --oneline
```

---

## 3. 提交前先建 .gitignore

在项目根目录新建 `.gitignore`，写三行：

```gitignore
__pycache__/
*.pyc
.vscode/
```

说明：
- 这些是 Python 缓存和编辑器配置，没必要进仓库；
- `todo.json`（你的待办数据）**建议提交**，属于项目的一部分，换电脑能带走；
- `.gitignore` 文件本身**要提交**。

---

## 4. 后悔药：退回上一个可用版本

```powershell
git reset --hard HEAD
```

⚠️ **会丢弃所有未提交的改动，且不可恢复。**
让 Cline 大改代码之前，先 commit 一次；改坏了就执行这条退回。

只想看某个文件的改动内容、先不退回：

```powershell
git diff 文件名
```

---

## 5. 异地备份：推到 GitHub

本地提交只能防"改坏了"，防不了"硬盘坏了"。要真正防丢，去 GitHub 建一个**空仓库**（不要勾选初始化 README），然后：

```powershell
git branch -M main
git remote add origin https://github.com/你的用户名/仓库名.git
git push -u origin main
```

第一次 push 会弹浏览器让你授权 GitHub，授权完就自动推上去了。
之后每次只需：

```powershell
git push
```

---

## 6. 和 Cline 配合的工作节奏（重点）

这是本手册最实用的一条：

```
1. 让 Cline 改代码
2. 自己跑一遍，确认功能正常
3. git add . && git commit -m "说明"
4. 让它改下一件事
```

**每次改完且验证通过，就立刻 commit 一次。**
这样 Cline 下一次改坏了，不用靠回忆复原，一条 `git reset --hard HEAD` 回到上一个可用状态。

---

## 7. 不想敲命令：VS Code 图形界面

左侧活动栏那个**分叉形状图标** = 源代码管理（快捷键 `Ctrl+Shift+G`）：

| 图形界面操作 | 等价命令 |
|---|---|
| 点"初始化仓库" | `git init` |
| 写提交说明后按 `Ctrl+Enter` | `git add .` + `git commit` |
| 右上角 `↻` 图标 | 拉取 |
| 右上角 `↑` 图标 | 推送 |

鼠标操作和命令行是同一套东西的两种皮。建议先用命令行把概念跑通，之后懒了再用图形界面。

---

## 8. 常见报错速查

| 现象 | 原因 / 处理 |
|---|---|
| `fatal: not a git repository` | 当前目录不是仓库，先 `git init`，或 `cd` 到项目根目录 |
| `Please tell me who you are` | 没配 user.name / user.email，回到第 0 节 |
| `nothing to commit` | 没有新改动，或忘了 `git add .` |
| `failed to push some refs` | 远程有内容没拉下来，先 `git pull --rebase` 再 push |
| 中文文件名显示成 `\344\275\240` | Git 显示编码问题，不影响功能，可忽略 |

---

## 9. 命令清单（打印版）

```
# 一次性
git init
git config --global user.name "名字"
git config --global user.email "邮箱"

# 日常
git status
git add .
git commit -m "说明"
git log --oneline

# 回退
git reset --hard HEAD

# 远程
git remote add origin <仓库地址>
git push -u origin main
git push
git pull
```

---

*本手册针对 Windows PowerShell 环境编写。*
