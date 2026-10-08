import tkinter as tk
from tkinter import messagebox
from todo import load_data, save_data
import uuid


def refresh_list():
    sel = lb.curselection()

    lb.delete(0, tk.END)
    items = load_data()
    for item in items:
        mark = "[x]" if item.get("done", False) else "[ ]"
        lb.insert(tk.END, f"{mark} {item['content']}")

    if sel and sel[0] < lb.size():
        lb.selection_set(sel[0])

    done = sum(1 for item in items if item.get("done", False))
    status_label.config(text=f"共 {len(items)} 条，已完成 {done} 条")

def on_add(event=None):
    text = entry.get().strip()
    if not text:
        return
    items = load_data()
    items.append({"id": uuid.uuid4().hex[:8], "content": text, "done": False})
    save_data(items)
    entry.delete(0, tk.END)
    refresh_list()


def on_toggle():
    sel = lb.curselection()
    if not sel:
        messagebox.showinfo("提示", "请先选择一个任务")
        return
    idx = sel[0]
    items = load_data()
    if idx >= len(items):
        refresh_list()
        return
    items[idx]["done"] = not items[idx].get("done", False)
    save_data(items)
    refresh_list()


def on_del():
    sel = lb.curselection()
    if not sel:
        messagebox.showinfo("提示", "请先选择一个任务")
        return
    idx = sel[0]
    items = load_data()
    if idx >= len(items):
        refresh_list()
        return
    items.pop(idx)
    save_data(items)
    refresh_list()


# --- UI 搭建 ---
root = tk.Tk()
root.title("Todo GUI")
root.geometry("400x500")

# 顶部输入区
top_frame = tk.Frame(root)
top_frame.pack(fill=tk.X, padx=10, pady=10)

entry = tk.Entry(top_frame)
entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
entry.bind("<Return>", on_add)

tk.Button(top_frame, text="添加", command=on_add).pack(side=tk.LEFT, padx=(5, 0))

# 中间任务列表
lb = tk.Listbox(root)
lb.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

# 双击切换完成状态，按 Delete 键删除
lb.bind("<Double-Button-1>", lambda e: on_toggle())
lb.bind("<Delete>", lambda e: on_del())

# 底部按钮区
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Button(bottom_frame, text="切换完成状态", command=on_toggle).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
tk.Button(bottom_frame, text="删除", command=on_del).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

# 状态栏
status_label = tk.Label(root, text="", anchor="w", fg="gray")
status_label.pack(fill=tk.X, padx=10, pady=(0, 10))

refresh_list()
root.mainloop()