import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import os


class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor - Untitled")
        self.filepath = None
        self.set_icon()
        self.create_widgets()

    def set_icon(self):
        icon_path = 'text-editor.ico'
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)

    def create_widgets(self):
        # Create Menu
        self.menu_bar = tk.Menu(self.root)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.exit_editor)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut", command=self.cut_text)
        self.edit_menu.add_command(label="Copy", command=self.copy_text)
        self.edit_menu.add_command(label="Paste", command=self.paste_text)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Undo", command=self.undo_text)
        self.edit_menu.add_command(label="Redo", command=self.redo_text)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.view_menu.add_command(label="Word Count", command=self.word_count)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)

        self.root.config(menu=self.menu_bar)

        # Create Text Area with Scrollbar
        self.text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=80, height=30, undo=True)
        self.text_area.pack(expand=True, fill='both')

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.root.title("Simple Text Editor - Untitled")
        self.filepath = None

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if filepath:
            try:
                with open(filepath, "r") as file:
                    content = file.read()
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(1.0, content)
                    self.filepath = filepath
                    self.root.title(f"Simple Text Editor - {os.path.basename(filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open the file: {e}")

    def save_file(self):
        if not self.filepath:
            self.save_as_file()
        else:
            try:
                with open(self.filepath, "w") as file:
                    text = self.text_area.get(1.0, tk.END)
                    file.write(text)
                    self.root.title(f"Simple Text Editor - {os.path.basename(self.filepath)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save the file: {e}")

    def save_as_file(self):
        try:
            filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if filepath:
                with open(filepath, "w") as file:
                    text = self.text_area.get(1.0, tk.END)
                    file.write(text)
                    self.filepath = filepath
                    self.root.title(f"Simple Text Editor - {os.path.basename(filepath)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save the file: {e}")

    def exit_editor(self):
        self.root.quit()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def undo_text(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo_text(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def word_count(self):
        content = self.text_area.get(1.0, tk.END)
        words = content.split()
        num_words = len(words)
        messagebox.showinfo("Word Count", f"Total words: {num_words}")


def main():
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
