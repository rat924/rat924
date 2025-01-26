import tkinter as tk
import json
import re
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, Toplevel, colorchooser
import tkinter.font as tkFont
from datetime import datetime
import subprocess
import threading
import os
import time
global ver
ver="0.3137"
global font
font="Consolas", 12, "bold"
global run
run=0
if os.path.exists("unknown.ssl"):
    os.remove("unknown.ssl")
    
global Seperator1, Seperator2, Variable_Marker
with open("Achoo.cfg",encoding="UTF-8") as f:
    for line in f:
        Name,Value=line.split("=",1)
        globals()[Name.strip()]=Value.strip()

class AchooEditor:
    def __init__(self, root):
        self.root = root
        self.file_path="unknown.ssl"
        self.root.title("Blessya for Achoo "+ver+" - "+ self.file_path)
        self.root.geometry("970x600")
        self.file_path = None
        self.create_menu()
        self.create_widgets()
        self.text_editor.bind("<KeyRelease>", self.highlight_syntax)
        self.populate_script_listbox()
        self.load_colors()
        self.user_input = ""  
        self.console.bind("<KeyRelease>", self.capture_input)
        self.console.bind('<Control-c>', self.stop_execution)
        self.console.config(state='disabled')

    def capture_input(self, event):
        if event.keysym == "Return":
            self.console.config(state='disabled')
            if self.user_input:
                self.process.stdin.write(self.user_input + '\n')
                self.console.config(state='disabled')
                try:
                    self.process.stdin.flush()
                except:
                    pass
                self.user_input = ""  
        elif event.keysym == "BackSpace":
            self.user_input = self.user_input[:-1]  
        else:
            if len(event.char) == 1:  
                self.user_input += event.char
        

    def append_console(self, text):
        self.console.insert(tk.END, text)
        self.console.see(tk.END)
        self.console.config(state='disabled')

    def process_input(self, event):
        if self.process: 
            user_input = self.console.get("end-2c", tk.END).strip() 
            if user_input:
                self.process.stdin.write(user_input + '\n') 
                self.process.stdin.flush() 
                self.console.config(state='disabled')

    def read_output(self, process):
        waiting_for_input = False 
        for stdout_line in iter(process.stdout.readline, ""):
            self.append_console(stdout_line)
            self.root.update_idletasks()


            if "Prompt:" in stdout_line:  
                if not waiting_for_input:
                    self.append_console("> ")  
                    waiting_for_input = True  
            else:
                waiting_for_input = False  

        process.stdout.close()
        process.wait()

        stderr_output = process.stderr.read()
        if stderr_output:
            self.append_console(stderr_output)


    def run_script(self):
        global run
        run=1
        if self.file_path:
            self.save_file()
            threading.Thread(target=self.execute_script, args=(self.file_path,), daemon=True).start()
        else:
            self.file_path="unknown.ssl"
            
            self.run_script()
        run=0

    def execute_script(self, script_path):
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        start_time = datetime.now()

        python_script = 'Achoo.py'
        exe_script = 'Achoo.exe'

        self.process = None  
        try:
            if os.path.isfile(python_script):
                self.process = subprocess.Popen(['python', '-u', python_script, script_path],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE,
                                                text=True,
                                                creationflags=subprocess.CREATE_NO_WINDOW)
            elif os.path.isfile(exe_script):
                self.process = subprocess.Popen([exe_script, script_path],
                                                stdout=subprocess.PIPE,
                                                stderr=subprocess.PIPE,
                                                stdin=subprocess.PIPE,
                                                text=True,
                                                creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                self.append_console("Error: Neither Achoo.py nor Achoo.exe were found.\n")
                return

            output_thread = threading.Thread(target=self.read_output, args=(self.process,), daemon=True)
            output_thread.start()

            self.process.wait()

            output_thread.join()

            end_time = datetime.now()
            duration = end_time - start_time
            self.append_console(f"Start:    {start_time}\n")            
            self.append_console(f"End:      {end_time}\n")
            self.append_console(f"Duration: {duration}\n")

            if os.path.exists("unknown.ssl"):
                os.remove("unknown.ssl")

        except Exception as e:
            self.append_console(f"Error: {e}\n")
        finally:
            self.console.config(state='disabled')

    def stop_execution(self, event=None):
        """Stop the running process."""
        if self.process:
            self.process.terminate()
            self.process = None
            self.appf_console("Execution stopped.\n")


    def load_colors(self):
        if os.path.exists("Blessya.set"):
            with open("Blessya.set", "r") as file:
                self.current_colors = json.load(file)
        else:
            self.current_colors = {
                "text": ("black", "white"),
                "command": ("blue", "white"),
                "variable": ("green", "white"),
                "comment": ("gray", "white"),
                "seperator1": ("red", "white"),
                "seperator2": ("red", "white"),
                "lineseperator": ("red","white"),
                "operator": ("magenta", "white"),
                "python": ("brown", "white"),
                "subs": ("white", "black"),
                "background": ("white", "white")
            }
        self.text_editor.config(bg=self.current_colors["background"][1])


    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open ...", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save as...", accelerator="Ctrl+Shift+S", command=self.save_as)
        file_menu.add_separator()
        file_menu.add_command(label="Quit", accelerator="Alt+F4", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Search", accelerator="Ctrl+f", command=self.search_text)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+h", command=lambda: self.replace_text(False))
        edit_menu.add_command(label="Replace (case sensitive)", accelerator="Ctrl+H", command=lambda: self.replace_text(True))
        menubar.add_cascade(label="Edit", menu=edit_menu)


        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="Execute Script", accelerator="F5", command=self.run_script)
        menubar.add_cascade(label="Execute", menu=run_menu)

        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Colorsettings", command=self.open_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        

        self.root.config(menu=menubar)

        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-S>", lambda event: self.save_as())
        self.root.bind_all("<Control-h>", lambda event: self.replace_text(False))
        self.root.bind_all("<Control-H>", lambda event: self.replace_text(True))
        self.root.bind_all("<Control-f>", lambda event: self.search_text())
        self.root.bind_all("<F5>", lambda event: self.run_script())

    def save_colors(self, settings_dialog):
        with open("Blessya.set", "w") as file:
            json.dump(self.current_colors, file)
        settings_dialog.destroy()  # Fenster schließen

    def open_settings(self):
        settings_dialog = Toplevel(self.root)
        settings_dialog.title("Settings")

        def choose_foreground_color(tag, label):
            color = colorchooser.askcolor()[1]
            if color:
                self.current_colors[tag] = (color, self.current_colors[tag][1])
                self.text_editor.tag_configure(tag, foreground=color)
                label.config(bg=color)
                settings_dialog.focus_force()

        def choose_background_color(tag, label):
            color = colorchooser.askcolor()[1]
            if color:
                self.current_colors[tag] = (self.current_colors[tag][0], color)
                self.text_editor.tag_configure(tag, background=color)
                label.config(bg=color)
                settings_dialog.focus_force()

        def choose_global_background():
            color = colorchooser.askcolor()[1]
            if color:
                self.current_colors["background"] = (self.current_colors["background"][0], color)
                self.text_editor.config(bg=color)
                settings_dialog.focus_force()

        for tag, colors in self.current_colors.items():
            if tag != "background":
                fg_color, bg_color = colors
                frame = tk.Frame(settings_dialog)
                frame.pack(pady=5)

                tk.Label(frame, text=f"{tag.capitalize()} Color:").pack(side=tk.LEFT)

                fg_label = tk.Label(frame, width=10, bg=fg_color)
                fg_label.pack(side=tk.LEFT, padx=5)

                fg_button = tk.Button(frame, text="Choose Foreground", command=lambda t=tag, lbl=fg_label: choose_foreground_color(t, lbl))
                fg_button.pack(side=tk.LEFT)

                bg_label = tk.Label(frame, width=10, bg=bg_color)
                bg_label.pack(side=tk.LEFT, padx=5)

                bg_button = tk.Button(frame, text="Choose Background", command=lambda t=tag, lbl=bg_label: choose_background_color(t, lbl))
                bg_button.pack(side=tk.LEFT)

        global_bg_button = tk.Button(settings_dialog, text="Choose Global Background", command=choose_global_background)
        global_bg_button.pack(pady=10)

        apply_button = tk.Button(settings_dialog, text="Save to file", command=lambda: [self.highlight_syntax(), self.save_colors(settings_dialog)])
        apply_button.pack(pady=10)




    def search_text(self):
        search_term = simpledialog.askstring("Search", "Enter the text you want to highlight:")
        self.text_editor.tag_remove("highlight", "1.0", tk.END)
        if search_term:
            content = self.text_editor.get("1.0", tk.END)
            if search_term.lower() in content.lower():
                start_idx = "1.0"
                while True:
                    start_idx = self.text_editor.search(search_term, start_idx, tk.END, nocase=1)
                    if not start_idx:
                        break
                    
                    end_idx = self.text_editor.index(f"{start_idx}+{len(search_term)}c")
                    
                    self.text_editor.tag_add("highlight", start_idx, end_idx)
                    start_idx = end_idx  

                self.text_editor.tag_config("highlight", background="red")
            else:
                messagebox.showinfo("Search Result", f"'{search_term}' not found.")


    def replace_text(self, case):
        dialog = tk.Toplevel(self.text_editor)
        dialog.title("Replace")
        dialog.geometry("300x175") 

        search_label = tk.Label(dialog, text="Enter text to search:")
        search_label.pack(pady=5)
        search_entry = tk.Entry(dialog)
        search_entry.pack(pady=5)

        replace_label = tk.Label(dialog, text="Enter text to replace with:")
        replace_label.pack(pady=5)
        replace_entry = tk.Entry(dialog)
        replace_entry.pack(pady=5)

        def on_replace():
            search_term = search_entry.get()
            replace_term = replace_entry.get()
            if search_term:
                content = self.text_editor.get("1.0", tk.END)
                if case:
                    new_content = content.replace(search_term, replace_term)
                else:
                    new_content = re.sub(re.escape(search_term), replace_term, content, flags=re.IGNORECASE)

                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", new_content)
            dialog.destroy()  

        replace_button = tk.Button(dialog, text="Replace", command=on_replace)
        replace_button.pack(pady=10)

    def create_widgets(self):
        global font
        font = font
        line_font = tkFont.Font(font=font)
        line_font.configure(weight="normal")

        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        editor_frame = tk.Frame(main_frame)
        editor_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        editor_scrollbar = tk.Scrollbar(editor_frame)
        editor_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.line_numbers = tk.Text(editor_frame, width=4, padx=0, takefocus=0, border=0, background='lightgrey', state='disabled', font=line_font)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        self.text_editor = tk.Text(editor_frame, wrap=tk.NONE, undo=True, font=font, yscrollcommand=editor_scrollbar.set)
        self.text_editor.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        editor_scrollbar.config(command=self.text_editor.yview)

        self.script_listbox = tk.Listbox(editor_frame, height=20, width=30)
        self.script_listbox.pack(side=tk.RIGHT, fill=tk.Y)
        self.script_listbox.bind("<<ListboxSelect>>", self.on_script_select)

        self.console = scrolledtext.ScrolledText(main_frame, height=10, state='disabled', bg='black', fg='white')
        self.console.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=False)

        self.text_editor.bind('<KeyRelease>', self.update_line_numbers)
        self.text_editor.bind('<ButtonRelease>', self.update_line_numbers)

        self.update_line_numbers()
        self.text_editor.bind('<MouseWheel>', self.on_mouse_wheel)

    def on_mouse_wheel(self, event):
        self.text_editor.yview_scroll(int(-1 * (event.delta / 120)), "units")

        self.update_line_numbers()
        return 'break'

    def sync_scroll(self, event=None):
        self.line_numbers.yview_moveto(self.text_editor.yview()[0])
        return 'break'

    def update_line_numbers(self, event=None):
        line_count = int(self.text_editor.index('end-1c').split('.')[0])  
        line_numbers = "\n".join(str(i) for i in range(1, line_count + 1)) 

        self.line_numbers.config(state='normal')
        self.line_numbers.delete('1.0', tk.END)
        self.line_numbers.insert('1.0', line_numbers)
        self.line_numbers.config(state='disabled')

        self.line_numbers.yview_moveto(self.text_editor.yview()[0])
        
    def populate_script_listbox(self):
        scripts = ["Script 1", "Script 2", "Script 3"]
        for script in scripts:
            self.script_listbox.insert(tk.END, script)

    def on_script_select(self, event):
        selected_script = self.script_listbox.get(self.script_listbox.curselection())
        self.console.config(state='disabled')
        self.console.insert(tk.END, f"Selected script: {selected_script}\n")
        #self.console.config(state='disabled')

    def populate_script_listbox(self):
        directory = os.getcwd()
        
        self.script_listbox.delete(0, tk.END) 
        for filename in os.listdir(directory):
            if filename.endswith(".ssl") or filename.endswith(".sub"):
                self.script_listbox.insert(tk.END, filename)

    def on_script_select(self, event):
        if self.file_path=="unknown.ssl" or self.file_path==None:
            response = messagebox.askyesno("Save file", "Do you want to save the file before you continue?")
            if response:
                self.save_file()
        selection = self.script_listbox.curselection()
        if selection:  
            file_name = self.script_listbox.get(selection[0])  
            file_path = os.path.join(os.getcwd(), file_name) 
            self.load_file(file_path)

    def new_file(self):
        if self.confirm_discard_changes():
            self.text_editor.delete(1.0, tk.END)
            self.file_path = None
            self.root.title("Blessya for Achoo "+ver+" - New Script")

    def open_file(self):
        if self.confirm_discard_changes():
            file_path = filedialog.askopenfilename(filetypes=[("Achoo Scriptfiles", "*.ssl;*.sub"),("Achoo Scripts", "*.ssl"),("Achoo Sub", "*.sub"), ("All files", "*.*")])
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as file:
                        content = file.read()
                    self.text_editor.delete(1.0, tk.END)
                    self.text_editor.insert(tk.END, content)
                    self.file_path = file_path
                    self.root.title(f"Blessya for Achoo "+ver+" - {self.file_path}")
                    self.highlight_syntax() 
                except Exception as e:
                    pass


    def load_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.text_editor.delete(1.0, tk.END)  
            self.text_editor.insert(tk.END, content)  
            self.file_path = file_path  
            self.root.title(f"Blessya for Achoo {ver} - {self.file_path}")  
            self.highlight_syntax()  
        except Exception as e:
            pass


    def save_file(self):
        global run
        if self.file_path=="unknown.ssl" and run==0:
            self.save_as()
            return
        if self.file_path:
            try:
                content = self.text_editor.get(1.0, tk.END)
                with open(self.file_path, "w", encoding="utf-8") as file:
                    file.write(content)
            except Exception as e:
                pass
        else:
            self.save_as()

    def save_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ssl",
                                                 filetypes=[("Achoo Scriptfiles", "*.ssl"),("Achoo Sub", "*.sub"), ("All files", "*.*")])
        if file_path:
            try:
                content = self.text_editor.get(1.0, tk.END)
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(content)
                self.file_path = file_path
                self.root.title(f"Blessya for Achoo - {self.file_path}")
            except Exception as e:
                pass

        self.populate_script_listbox()            

    def confirm_discard_changes(self):
        if self.text_editor.edit_modified():
            response = messagebox.askyesnocancel("Save changes", "Do you want to save the changes?")
            if response:  
                self.save_file()
                return True
            elif response is False:  
                return True
            else:  
                return False
        return True             



    def append_console(self, text):
        self.console.config(state='normal')
        self.console.insert(tk.END, text)
        self.console.see(tk.END)

    def highlight_syntax(self, event=None):
        self.update_line_numbers()
        global font
        italic_font = tkFont.Font(font=font)
        italic_font.configure(slant="italic") 
        self.text_editor.tag_remove("command", "1.0", tk.END)
        self.text_editor.tag_remove("variable", "1.0", tk.END)
        self.text_editor.tag_remove("seperator1", "1.0", tk.END)
        self.text_editor.tag_remove("seperator2", "1.0", tk.END)
        self.text_editor.tag_remove("lineseperator", "1.0", tk.END)
        self.text_editor.tag_remove("comment", "1.0", tk.END)
        self.text_editor.tag_remove("operator", "1.0", tk.END)
        self.text_editor.tag_remove("python", "1.0", tk.END)
        self.text_editor.tag_remove("subs", "1.0", tk.END)
        

        for tag, colors in self.current_colors.items():
            fg_color, bg_color = colors  
            self.text_editor.tag_configure(tag, foreground=fg_color, background=bg_color, font=font)

        self.text_editor.tag_configure("comment", foreground=self.current_colors["comment"][0], font=italic_font)
        self.text_editor.tag_configure("subs", foreground=self.current_colors["subs"][0], background=self.current_colors["subs"][1], font=font)

        operators = ["=", "<", "<=", ">", ">=", "!=", "==","+","-","/","*"]

        commands = ["exe", "fod", "fid", "ted", "log", "cmd", "wrf", "crf", "ifc", "get", 
                    "qut", "men", "set", "got", "ref", "que", "sea", "gel", "wrl", "str", 
                    "rsv", "cal", "dat", "tim", "foe", "fie", "sst", "ton", "dnl", 
                    "rxm", "wxm", "rjs", "wjs", "tit", "rsf", "bgr", "fgr", "spl", "slp", 
                    "loc", "cls", "kyi", "brk", "kyo", "rnd", "inp", "ver", "mou", "hlp", 
                    "exc", "kiw", "win", "sqi", "thr", "window", "button", "start", "end",
                    "getcontent", "setcontent","label","entry","checkbox", "snd", "dbq",
                    "req", "password", "cry", "add", "for", "nxt", "whi", "wnd", "cwi", "bwi", "len",
                    "kow", "sav", "loa", "env", "fil", "sch", "aut", "any", "tmr"]

        content = self.text_editor.get("1.0", tk.END)

        for cmd in commands:
            start_idx = "1.0"
            while True:
                start_idx = self.text_editor.search(cmd+"", start_idx, tk.END, nocase=1)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(cmd)}c"
                self.text_editor.tag_add("command", start_idx, end_idx)
                start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search(Variable_Marker, start_idx, tk.END)
            if not start_idx:
                break
            end_idx = self.text_editor.search(Variable_Marker, start_idx + "+1c", tk.END)
            if not end_idx:
                break
            self.text_editor.tag_add("variable", start_idx, end_idx + "+1c")
            start_idx = end_idx + "+1c"

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search("   ", start_idx, tk.END ,nocase=1)
            if not start_idx:
                break
            line_end_idx = self.text_editor.index(f"{start_idx} lineend") 
            self.text_editor.tag_add("python", start_idx, line_end_idx)
            start_idx = line_end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search("rem ", start_idx, tk.END ,nocase=1)
            if not start_idx:
                break
            line_end_idx = self.text_editor.index(f"{start_idx} lineend") 
            self.text_editor.tag_add("comment", start_idx, line_end_idx)
            start_idx = line_end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search("sub ", start_idx, tk.END, nocase=1)
            if not start_idx:
                break

            line_end_idx = self.text_editor.index(f"{start_idx} lineend")
            separator_idx = self.text_editor.search("|", start_idx, tk.END)

            if separator_idx:               
                end_idx = separator_idx if separator_idx < line_end_idx else line_end_idx
            else:
                end_idx = line_end_idx 

            self.text_editor.tag_add("subs", start_idx, end_idx)
            start_idx = end_idx



        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search("got ", start_idx, tk.END, nocase=1)
            if not start_idx:
                break

            line_end_idx = self.text_editor.index(f"{start_idx} lineend")
            separator_idx = self.text_editor.search("|", start_idx, tk.END)

            if separator_idx:            
                end_idx = separator_idx if separator_idx < line_end_idx else line_end_idx
            else:
                end_idx = line_end_idx  

            self.text_editor.tag_add("subs", start_idx, end_idx)
            start_idx = end_idx       
    
        for op in operators:
            start_idx = "1.0"
            while True:
                start_idx = self.text_editor.search(op, start_idx, tk.END)
                if not start_idx:
                    break
                end_idx = f"{start_idx}+{len(op)}c"
                self.text_editor.tag_add("operator", start_idx, end_idx)
                start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search(Seperator1, start_idx, tk.END)  
            if not start_idx:
                break
            length = len(Seperator1)
            end_idx = f"{start_idx}+{length}c"
            self.text_editor.tag_add("seperator1", start_idx, end_idx)
            start_idx = end_idx

        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search(Seperator2, start_idx, tk.END)  
            if not start_idx:
                break
            length = len(Seperator2)
            end_idx = f"{start_idx}+{length}c"
            self.text_editor.tag_add("seperator2", start_idx, end_idx)
            start_idx = end_idx
        
        start_idx = "1.0"
        while True:
            start_idx = self.text_editor.search(LineSeperator, start_idx, tk.END)  
            if not start_idx:
                break
            length = len(LineSeperator)
            end_idx = f"{start_idx}+{length}c"
            self.text_editor.tag_add("lineseperator", start_idx, end_idx)
            start_idx = end_idx
        

'''if __name__ == "__main__":
    root = tk.Tk()
    app = AchooEditor(root)
    root.mainloop()'''


root = tk.Tk()
app = AchooEditor(root)
root.mainloop()
