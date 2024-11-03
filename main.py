from note_app import NoteManager
from rich.console import Console
import sys

def main():
    console = Console()
    note_manager = NoteManager()
    
    while True:
        console.print("\n[bold cyan]离线笔记本[/bold cyan]")
        console.print("1. 添加笔记")
        console.print("2. 查看所有笔记")
        console.print("3. 查看特定笔记")
        console.print("4. 更新笔记")
        console.print("5. 删除笔记")
        console.print("6. 搜索笔记")
        console.print("0. 退出")
        
        choice = input("\n请选择操作 (0-6): ")
        
        if choice == "1":
            title = input("请输入笔记标题: ")
            console.print("请输入笔记内容 (支持Markdown格式，输入'END'结束):")
            content_lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                content_lines.append(line)
            content = '\n'.join(content_lines)
            tags = input("请输入标签 (用逗号分隔): ")
            note_manager.add_note(title, content, tags)
            
        elif choice == "2":
            note_manager.list_notes()
            
        elif choice == "3":
            note_id = input("请输入笔记ID: ")
            note_manager.view_note(int(note_id))
            
        elif choice == "4":
            note_id = input("请输入要更新的笔记ID: ")
            title = input("请输入新标题: ")
            console.print("请输入新内容 (输入'END'结束):")
            content_lines = []
            while True:
                line = input()
                if line == 'END':
                    break
                content_lines.append(line)
            content = '\n'.join(content_lines)
            tags = input("请输入新标签 (用逗号分隔): ")
            note_manager.update_note(int(note_id), title, content, tags)
            
        elif choice == "5":
            note_id = input("请输入要删除的笔记ID: ")
            confirm = input("确定要删除吗？(y/n): ")
            if confirm.lower() == 'y':
                note_manager.delete_note(int(note_id))
                
        elif choice == "6":
            keyword = input("请输入搜索关键词: ")
            note_manager.search_notes(keyword)
            
        elif choice == "0":
            console.print("[yellow]感谢使用，再见！[/yellow]")
            sys.exit()
            
        else:
            console.print("[red]无效的选择，请重试！[/red]")

if __name__ == "__main__":
    main()