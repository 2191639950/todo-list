import json
import os
import sys
import uuid


DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        return []
    except Exception:
        return []


def save_data(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)


def cmd_add(items, text):
    if not text.strip():
        print("任务内容不能为空。")
        return

    item = {
        "id": uuid.uuid4().hex[:8],
        "content": text,
        "done": False,
    }
    items.append(item)
    save_data(items)
    print("已添加：" + text)


def show_list(items):
    if not items:
        print("当前没有待办事项。")
        return

    for index, item in enumerate(items, start=1):
        mark = "[x]" if item.get("done") else "[ ]"
        print("{}. {} {}".format(index, mark, item.get("content", "")))


def parse_args(args):
    if not args:
        return None, None

    command = args[0]
    rest = args[1:]

    if command == "add":
        text = " ".join(rest)
        return "add", text

    if command == "list":
        if rest:
            return "invalid", None
        return "list", None

    if command in ("done", "undo"):
        if len(rest) != 1:
            return "invalid", None
        raw_index = rest[0]
        if not raw_index.isdigit():
            return "invalid", None
        index = int(raw_index) - 1
        return command, index

    if command == "del":
        if len(rest) != 1:
            return "invalid", None
        raw_index = rest[0]
        if not raw_index.isdigit():
            return "invalid", None
        index = int(raw_index) - 1
        return command, index

    if command == "help":
        if rest:
            return "invalid", None
        return "help", None

    return "unknown", None


def cmd_done(items, index):
    count = len(items)
    if index < 0 or index >= count:
        print("序号无效，请输入 1 到 {} 之间的序号。".format(count))
        return

    items[index]["done"] = not items[index].get("done", False)
    save_data(items)

    status = "已完成" if items[index].get("done") else "未完成"
    print("序号 {} 已 {}".format(index + 1, status))


def cmd_del(items, index):
    count = len(items)
    if index < 0 or index >= count:
        print("序号无效，请输入 1 到 {} 之间的序号。".format(count))
        return

    removed = items[index]
    del items[index]
    save_data(items)
    print("已删除：" + removed.get("content", ""))


def cmd_help():
    help_text = """Todo CLI - 命令行待办清单
用法：
  todo.py add <任务内容>    添加待办
  todo.py list              查看待办
  todo.py done <序号>       标记已完成 / 撤销
  todo.py undo <序号>       取消已完成
  todo.py del <序号>        删除待办
  todo.py help              显示帮助"""
    print(help_text)


def main():
    args = sys.argv[1:]
    command, value = parse_args(args)

    items = load_data()

    if command is None:
        cmd_help()
        return

    if command == "invalid":
        print("参数错误。")
        cmd_help()
        return

    if command == "unknown":
        cmd_help()
        return

    if command == "add":
        cmd_add(items, value)
        return

    if command == "list":
        show_list(items)
        return

    if command == "done":
        cmd_done(items, value)
        return

    if command == "undo":
        cmd_done(items, value)
        return

    if command == "del":
        cmd_del(items, value)
        return

    if command == "help":
        cmd_help()
        return


if __name__ == "__main__":
    main()
