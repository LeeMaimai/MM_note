import sqlite3
import datetime
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown

class NoteManager:
    def __init__(self):
        self.conn = sqlite3.connect('notes.db')
        self.cursor = self.conn.cursor()
        self.console = Console()
        self.setup_database()
    
    def setup_database(self):
        """创建数据库表"""
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP,
            tags TEXT
        )
        ''')
        self.conn.commit()

    def add_note(self, title, content, tags=None):
        """添加新笔记"""
        current_time = datetime.datetime.now()
        self.cursor.execute('''
        INSERT INTO notes (title, content, created_at, updated_at, tags)
        VALUES (?, ?, ?, ?, ?)
        ''', (title, content, current_time, current_time, tags))
        self.conn.commit()
        self.console.print("[green]笔记添加成功！[/green]")

    def list_notes(self):
        """列出所有笔记"""
        table = Table(title="我的笔记")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("标题", style="magenta")
        table.add_column("创建时间", style="green")
        table.add_column("标签", style="yellow")

        self.cursor.execute('SELECT id, title, created_at, tags FROM notes')
        notes = self.cursor.fetchall()
        
        for note in notes:
            table.add_row(
                str(note[0]),
                note[1],
                str(note[2])[:19],
                note[3] or "无标签"
            )
        
        self.console.print(table)

    def view_note(self, note_id):
        """查看特定笔记"""
        self.cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
        note = self.cursor.fetchone()
        
        if note:
            self.console.print(f"\n[bold magenta]标题：{note[1]}[/bold magenta]")
            self.console.print(f"[bold blue]创建时间：{note[3]}[/bold blue]")
            self.console.print(f"[bold yellow]标签：{note[5] or '无标签'}[/bold yellow]")
            self.console.print("\n[bold green]内容：[/bold green]")
            md = Markdown(note[2])
            self.console.print(md)
        else:
            self.console.print("[red]未找到该笔记！[/red]")

    def update_note(self, note_id, title=None, content=None, tags=None):
        """更新笔记"""
        current_time = datetime.datetime.now()
        if title and content:
            self.cursor.execute('''
            UPDATE notes 
            SET title = ?, content = ?, updated_at = ?, tags = ?
            WHERE id = ?
            ''', (title, content, current_time, tags, note_id))
        self.conn.commit()
        self.console.print("[green]笔记更新成功！[/green]")

    def delete_note(self, note_id):
        """删除笔记"""
        self.cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
        self.conn.commit()
        self.console.print("[red]笔记已删除！[/red]")

    def search_notes(self, keyword):
        """搜索笔记"""
        self.cursor.execute('''
        SELECT id, title, created_at, tags 
        FROM notes 
        WHERE title LIKE ? OR content LIKE ? OR tags LIKE ?
        ''', (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        
        notes = self.cursor.fetchall()
        if notes:
            table = Table(title=f"搜索结果：{keyword}")
            table.add_column("ID", justify="right", style="cyan")
            table.add_column("标题", style="magenta")
            table.add_column("创建时间", style="green")
            table.add_column("标签", style="yellow")
            
            for note in notes:
                table.add_row(str(note[0]), note[1], str(note[2])[:19], note[3] or "无标签")
            
            self.console.print(table)
        else:
            self.console.print("[yellow]未找到相关笔记！[/yellow]")