import tkinter as tk
from tkinter import messagebox
from todo import load_data, save_data
import uuid


def refresh_list():
    lb.delete(0, tk.END)
    for item in load_data():
        mark = "[x]" if item["done"] else "[ ]"
        lb.insert(tk.END, f"{mark} {item['content']}")


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
    items[idx]["done"] = not items[idx]["done"]
    save_data(items)
    refresh_list()


def on_del():
    sel = lb.curselection()
    if not sel:
        messagebox.showinfo("提示", "请先选择一个任务")
        return
    idx = sel[0]
    items = load_data()
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

# 底部按钮区
bottom_frame = tk.Frame(root)
bottom_frame.pack(fill=tk.X, padx=10, pady=(0, 10))

tk.Button(bottom_frame, text="切换完成状态", command=on_toggle).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
tk.Button(bottom_frame, text="删除", command=on_del).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

refresh_list()
root.mainloop()