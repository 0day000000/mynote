import os
import sys

# 自动修复某些 Windows 环境下 Python 3.12 的 Tcl/Tk 环境变量缺失问题 
tcl_dir = r'C:\Users\zn\AppData\Local\Programs\Python\Python312\tcl\tcl8.6'
tk_dir = r'C:\Users\zn\AppData\Local\Programs\Python\Python312\tcl\tk8.6'
if os.path.exists(tcl_dir):
    os.environ['TCL_LIBRARY'] = tcl_dir
if os.path.exists(tk_dir):
    os.environ['TK_LIBRARY'] = tk_dir

import tkinter as tk
from tkinter import messagebox, filedialog

class StickyNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title('MyNote 桌面便签')
        self.root.geometry('350x400+100+100')
        
        # 1. 永远在前台 (置顶)
        self.root.attributes('-topmost', True)
        
        # 2. 窗口半透明 (透明度 0.85，可按需调整 0.1 ~ 1.0)
        self.root.attributes('-alpha', 0.85)
        
        # 自动存盘配置文件路径
        self.config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.mynote_cache.txt')
        
        # 创建顶部菜单栏 (提供另存为与打开功能)
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label='打开文件...', command=self.open_file)
        file_menu.add_command(label='另存为...', command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label='退出', command=self.root.quit)
        menubar.add_cascade(label='文件', menu=file_menu)
        self.root.config(menu=menubar)
        
        # 3. 文本输入区域 (支持任意内容输入)
        self.text_area = tk.Text(self.root, wrap='word', undo=True, font=('Microsoft YaHei', 11))
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 4. 加载历史内容
        self.load_content()
        
        # 5. 绑定实时存盘事件 (每次输入修改时触发)
        self.text_area.bind('<<Modified>>', self.on_text_modified)
        
        # 状态栏提示
        self.status_label = tk.Label(self.root, text=' 💡 实时存盘中...', anchor='w', font=('Microsoft YaHei', 8), fg='gray')
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def load_content(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.text_area.insert('1.0', content)
            except Exception as e:
                print('加载缓存失败:', e)

    def on_text_modified(self, event=None):
        if self.text_area.edit_modified():
            try:
                content = self.text_area.get('1.0', tk.END)
                with open(self.config_file, 'w', encoding='utf-8') as f:
                    f.write(content)
            except Exception as e:
                print('实时存盘失败:', e)
            finally:
                self.text_area.edit_modified(False)

    def open_file(self):
        file_path = filedialog.askopenfilename(
            title='打开文本文件',
            filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')]
        )
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert('1.0', content)
                messagebox.showinfo('成功', '文件打开成功！')
            except Exception as e:
                messagebox.showerror('错误', f'打开文件失败：\n{e}')

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            title='另存为文本文件',
            defaultextension='.txt',
            filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')]
        )
        if file_path:
            try:
                content = self.text_area.get('1.0', 'end-1c')
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo('成功', '文件另存为成功！')
            except Exception as e:
                messagebox.showerror('错误', f'保存文件失败：\n{e}')

if __name__ == '__main__':
    root = tk.Tk()
    app = StickyNoteApp(root)
    root.mainloop()
