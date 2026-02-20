from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
import tkinter.messagebox as tmsg
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
from tkinter import font, colorchooser, filedialog, messagebox
import datetime
import random
from tkinter import PhotoImage



from notepad_features import NotepadFeatures


def newFile(event = None):
    global file
    root.title("Untitled - Notepad")
    file = None
    TextArea.delete(1.0, END)


def openFile(event = None):
    global file
    file = askopenfilename(defaultextension = ".txt",filetypes = [("All Files","."),("Text Documents","*.txt")])
    if file == "":
        file = None

    else:
        root.title(os.path.basename(file) + " - Notepad")
        TextArea.delete(1.0, END)
        f = open(file, "r")
        TextArea.insert(1.0, f.read())
        f.close 

def saveFile(event = None):
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt',defaultextension = ".txt",filetypes = [("All Files","."),("Text Documents","*.txt")])

        if file == "":
            file =None
        
        else:
            f = open(file, "w")
            f.write(TextArea.get(1.0,END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
            print("File Saved")

    else:
        f= open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()

def saveasFile(event = None):
    global file
    if file == None:
        file = asksaveasfilename(initialfile = 'Untitled.txt',defaultextension = ".txt",filetypes = [("All Files","."),("Text Documents","*.txt")])

        if file == "":
            file =None

        else:
            f = open(file, "w")
            f.write(TextArea.get(1.0,END))
            f.close()

            root.title(os.path.basename(file) + " - Notepad")
            print("File Saved")

    else:
        f= open(file, "w")
        f.write(TextArea.get(1.0, END))
        f.close()


def quitApp(event = NONE):
    # root.destroy()
    global text_change, file
    try:
        if text_change:
            mbox = messagebox.askyesnocancel("Warning", "Do You want to save this File ")
            if mbox is True:
                if file:
                    content = TextArea.get(1.0,END)
                    with open (file, "w", encoding=utf-8) as for_read:
                        for_read.write(content)
                        root.destroy()
                else:
                    content2 = TextArea.get(1.0,END)
                    file = filedialog.asksaveasfile(mode = "w" ,defaultextension = ".txt",filetypes = [("All Files","."),("Text Documents","*.txt")])
                    file.write(content2)
                    file.close()
                    root.destroy()
            elif mbox is False:
                root.destroy()
        else:
            root.destroy()
    except:
        return

def cut():
    TextArea.event_generate("<<Cut>>")

def copy():
    TextArea.event_generate("<<Copy>>")

def Paste():
    TextArea.event_generate("<<Paste>>")

def undoFunction(event=None):
    try:
        TextArea.edit_undo()
    except:
        pass
    return "break"

def redoFunction(event=None):
    try:
        TextArea.edit_redo()
    except:
        pass
    return "break"



def find(event = None):

    def find_fun():
        word = find_input.get()
        TextArea.tag_remove("match","1.0",END)
        matches = 0
        if word:
            start_pos = "1.0"
            while True:
                start_pos =TextArea.search(word,start_pos,stopindex=END)
                if not start_pos:
                    break
                end_pos = f"{start_pos}+{len(word)}c"
                TextArea.tag_add("match",start_pos,end_pos)
                matches += 1
                start_pos = end_pos
                TextArea.tag_config('match', foreground = "red", background = '#FFFF66')

        
    def replace_fun():
        word = find_input.get()
        replace_text = replace_input.get()
        content = TextArea.get(1.0,END)
        new_content = content.replace(word,replace_text)
        TextArea.delete(1.0,END)
        TextArea.insert(1.0,new_content)

    find_popup = Toplevel()
    find_popup.geometry("350x200")
    find_popup.title("Find Word")
    find_popup.resizable(0,0)

    find_fram = ttk.LabelFrame(find_popup,text = "Find and Replace Word")
    find_fram.pack(pady = 35)

    text_find = ttk.Label(find_fram,text = "Find")
    text_replace = ttk.Label(find_fram,text = "Replace")

    find_input = ttk.Entry(find_fram,width = 30)
    replace_input = ttk.Entry(find_fram,width = 30)

    find_button = ttk.Button(find_fram,text = "Find",command = find_fun )
    replace_button = ttk.Button(find_fram,text = "Replace",command = replace_fun)

    text_find.grid(row = 0, column = 0,padx = 4 ,pady = 4)
    text_replace.grid(row = 1, column = 0,padx = 4 ,pady = 4)

    find_input.grid(row = 0, column = 1,padx = 4 ,pady = 4)
    replace_input.grid(row = 1, column = 1,padx = 4 ,pady = 4)
    
    find_button.grid(row = 2, column = 0,padx = 8 ,pady = 4)
    replace_button.grid(row = 2, column = 1,padx = 8 ,pady = 4)

    

def clear(event = None):
    TextArea.delete(1.0,END)

def toolbar():
    global show_tool_bar
    if show_tool_bar is False:
        
        TextArea.pack_forget()
        status_bars.pack_forget()
        tool_bars_label.pack(side = TOP, fill = X)
        TextArea.pack(fill = BOTH, expand = True)
        status_bars.pack(side = BOTTOM)
        show_tool_bar = True

    else:
        
        tool_bars_label.pack_forget()
        show_tool_bar = False

def statusbar():
    global show_status_bar
    if show_status_bar:
        status_bars.pack_forget()
        show_status_bar =False
    
    else:
        status_bars.pack(side = BOTTOM)
        show_status_bar = True

def about():
    showinfo("Notepad", "Advance Notepad by 22SE02ML063(Dharm Rathod)")

def change_word(event = None):
    global text_change
    if TextArea.edit_modified():
        text_change = True
        word = len(TextArea.get(1.0,"end-1c").split())
        character = len(TextArea.get(1.0,"end-1c").replace(" ",""))
        status_bars.config(text = f"Character : {character}  Word : {word}")
    TextArea.edit_modified(FALSE)

def change_font(root):
    global font_default
    font_default = font_family.get()
    TextArea.configure(font=(font_default, font_size_default))

def change_font_size(root):
    global font_size_default
    font_size_default = size_var.get()
    TextArea.configure(font = (font_default, font_size_default))



def bold_fun():
    text_get = font.Font(font = TextArea["font"])
    if text_get.actual()["weight"] == 'normal':
        TextArea.configure(font = (font_default,font_size_default,"bold"))
    if text_get.actual()["weight"] == 'bold':
        TextArea.configure(font = (font_default,font_size_default,"normal"))


def italic_fun():
    text_get = font.Font(font = TextArea["font"])
    if text_get.actual()["slant"] == 'roman':
        TextArea.configure(font = (font_default,font_size_default,"italic"))
    if text_get.actual()["slant"] == 'italic':
        TextArea.configure(font = (font_default,font_size_default,"roman"))


def underline_fun():
    text_get = font.Font(font = TextArea["font"])
    if text_get.actual()["underline"] == 0:
        TextArea.configure(font = (font_default,font_size_default,"underline"))
    if text_get.actual()["underline"] == 1:
        TextArea.configure(font = (font_default,font_size_default,"normal"))

def color_choose():
    color_var = colorchooser.askcolor()
    TextArea.configure(fg = color_var[1])


def left_align_fun():
    text_get_all = TextArea.get(1.0,"end")
    TextArea.tag_config("left", justify = LEFT)
    TextArea.delete(1.0,END)
    TextArea.insert(INSERT,text_get_all,"left")

def center_align_fun():
    text_get_all = TextArea.get(1.0,"end")
    TextArea.tag_config("center", justify = CENTER)
    TextArea.delete(1.0,END)
    TextArea.insert(INSERT,text_get_all,"center")

def right_align_fun():
    text_get_all = TextArea.get(1.0,"end")
    TextArea.tag_config("right", justify = RIGHT)
    TextArea.delete(1.0,END)
    TextArea.insert(INSERT,text_get_all,"right")


def default():
    theme_choose = StringVar()
    theme_choose.set("Default")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)

def light():
    theme_choose = StringVar()
    theme_choose.set("Light")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)

def red():
    theme_choose = StringVar()
    theme_choose.set("Red")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)

def blue():
    theme_choose = StringVar()
    theme_choose.set("Blue")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)

def monokai():
    theme_choose = StringVar()
    theme_choose.set("Monokai")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)

def dark():
    theme_choose = StringVar()
    theme_choose.set("Dark")
    get_theme = theme_choose.get() 
    color_tuple= color_dict.get(get_theme)
    fg_color,bg_color = color_tuple[0],color_tuple[1]
    TextArea.config(background = bg_color, fg = fg_color)


def plot_button_clicked(chart_type):
    if TextArea.tag_ranges("sel"):  # Check if any text is selected
        selected_text = TextArea.get("sel.first", "sel.last")
    else:
        messagebox.showerror("Selection Required", "Please select the dataset to plot.")
        return
    features.plot_data_selection(chart_type, selected_text)







if _name_ == "_main_":
    root = Tk()
    root.title("Untitled Notepad")
    root.wm_iconbitmap("ico/2.ico")
    root.geometry("1080x720")
    root.maxsize(1920,1080)
    root.minsize(600,300)

    number_list = [0,1,2]
    rand=random.choice(number_list)
    random=int(rand)



    # MenuBar

    MenuBar = Menu(root,cursor = "arrow")
    FileMenu = Menu(MenuBar, tearoff = 0)

    # icon

    new_icon = PhotoImage(file = "ico/file.png")
    open_icon = PhotoImage(file = "ico/open.png")
    save_icon = PhotoImage(file = "ico/save.png")
    save_as_icon = PhotoImage(file = "ico/save_as.png")
    exit_icon = PhotoImage(file = "ico/exit.png")
    cut_icon = PhotoImage(file = "ico/cut.png")
    copy_icon = PhotoImage(file = "ico/copy.png")
    paste_icon = PhotoImage(file = "ico/paste.png")
    find_icon = PhotoImage(file = "ico/find.png")
    clear_icon = PhotoImage(file = "ico/clear.png")
    about_icon = PhotoImage(file = "ico/about.png")
    tool_icon = PhotoImage(file = "ico/tool.png")
    status_icon = PhotoImage(file = "ico/status.png")
    blue_icon = PhotoImage(file = "ico/blue.png")
    dark_icon = PhotoImage(file = "ico/dark.png")
    default_icon = PhotoImage(file = "ico/default.png")
    red_icon = PhotoImage(file = "ico/red.png")
    monokai_icon = PhotoImage(file = "ico/monokai.png")
    light_icon = PhotoImage(file = "ico/light.png")
    bold_icon = PhotoImage(file = "ico/bold.png")
    italic_icon = PhotoImage(file = "ico/italic.png")
    underline_icon = PhotoImage(file = "ico/underline.png")
    align_center_icon = PhotoImage(file = "ico/align_center.png")
    align_left_icon = PhotoImage(file = "ico/align_left.png")
    align_right_icon = PhotoImage(file = "ico/align_right.png")
    color_wheel_icon = PhotoImage(file = "ico/color_wheel.png")
    star_icon = PhotoImage(file = "ico/star.png")
    time_icon = PhotoImage(file = "ico/time.png")


    solve_icon = PhotoImage(file="ico/calculator.png")
    plot_icon = PhotoImage(file="ico/chart.png")
    google_icon = PhotoImage(file="ico/google.png")
    youtube_icon = PhotoImage(file="ico/youtube.png")
    chatbot_icon = PhotoImage(file="ico/chatbot.png")
    college_logo_img = PhotoImage(file="ico/college.png")
 


    color_dict = {
        
        'Default' : ('#000000','#bdbdbd'), #(font_color, bg_color)
        'Light' : ('#000000','#ffffff'),
        'Red' : ('#2d2d2d','#ff7070'),
        'Blue' : ('#3c3d3d','#acdde3'),
        'Monokai' : ('#544e3f','#ffcd70'),
        'Dark' : ('#ffffff','#3c3d3d')

    }


    # Font family

    font_default = "Consolas"
    font_size_default = 12 
         
    # Open New File

    FileMenu.add_command(label = "New", image = new_icon,compound= LEFT, accelerator = "Cmd + N",command =newFile)

    # Open Exiting File

    FileMenu.add_command(label = "Open", image = open_icon,compound= LEFT, accelerator = "Cmd + O", command = openFile)
    
    FileMenu.add_separator()

    
    
    # Save File

    FileMenu.add_command(label = "Save", image = save_icon,compound= LEFT, accelerator = "Cmd + S", command = saveFile)
    FileMenu.add_command(label = "Save As..", image = save_as_icon,compound= LEFT, accelerator = "Cmd + Shift + S", command = saveasFile)
    FileMenu.add_separator()
    FileMenu.add_command(label = "Exit", image = exit_icon,compound= LEFT,command = quitApp, accelerator = "Cmd + Q")
    MenuBar.add_cascade(label = "File", menu = FileMenu)

    EditMenu = Menu(MenuBar, tearoff = 0)

    EditMenu.add_command(label = "Cut", image = cut_icon,compound= LEFT, accelerator = "Cmd + X", command = cut)
    EditMenu.add_separator()
    EditMenu.add_command(label = "copy" ,image = copy_icon,compound= LEFT, accelerator = "Cmd + C", command = copy)
    EditMenu.add_command(label = "Paste",image = paste_icon,compound= LEFT, accelerator = "Cmd + V", command = Paste)
    EditMenu.add_separator()
    EditMenu.add_command(label = "Find",image = find_icon,compound= LEFT, accelerator = "Cmd + F", command = find)
    EditMenu.add_command(label = "Clear",image = clear_icon,compound= LEFT, accelerator = " Alt + X",command = clear)
    MenuBar.add_cascade(label = "Edit", menu = EditMenu)


    root.bind_all("<Control-n>", newFile)
    root.bind_all("<Control-o>", openFile)
    root.bind_all("<Control-f>", find)
    root.bind_all("<Control-s>", saveFile)
    root.bind_all("<Control-Shift-KeyPress-S>", saveasFile)
    root.bind_all("<Control-q>", quitApp)
    root.bind_all("<Alt-x>", clear)


    tool_bars_label = Label(root)
    tool_bars_label.pack(side = TOP, fill = X)

    #college logo
    college_logo_label = Label(tool_bars_label, image=college_logo_img, bg="white")
    college_logo_label.grid(row=0, column=0, padx=5)

    # Keep reference to avoid garbage collection
    college_logo_label.image = college_logo_img

    # Font box

    get_fonts = font.families()
    font_family = StringVar()
    font_box = ttk.Combobox(tool_bars_label, width = 30 , textvariable = font_family, state = "readonly",justify = CENTER)
    font_box["values"] = get_fonts
    font_box.current(get_fonts.index("Arial"))
    font_box.grid(row = 0 , column =1, padx = 5, pady = 1 )
    font_box.bind("<<ComboboxSelected>>", change_font)

    # Size Box

    size_var = IntVar()
    size_box = ttk.Combobox(tool_bars_label, width = 20, textvariable = size_var, state = "readonly", justify = CENTER)
    size_box["values"] = tuple(range(8,72,2))
    size_box.current(2)
    size_box.grid(row = 0, column = 2, padx = 5, pady =1)
    size_box.bind("<<ComboboxSelected>>", change_font_size)

    # Bold

    bold_btn =ttk.Button(tool_bars_label,image = bold_icon,command = bold_fun)
    bold_btn.grid(row = 0 , column = 3, padx = 2)
    # print(font.Font(font = TextArea["font"]).actual())
    
    # itatic

    italic_btn = ttk.Button(tool_bars_label,image = italic_icon)
    italic_btn.grid(row = 0, column = 4,padx = 2)
    italic_btn.configure(command = italic_fun)

    # underline

    underline_btn = ttk.Button(tool_bars_label,image = underline_icon)
    underline_btn.grid(row = 0, column = 5,padx = 2)
    underline_btn.configure(command = underline_fun)

    # color_wheel

    color_wheel_btn = ttk.Button(tool_bars_label,image = color_wheel_icon)
    color_wheel_btn.grid(row = 0, column = 6, padx=8)
    color_wheel_btn.configure(command = color_choose)

    # right_align

    align_right_btn = ttk.Button(tool_bars_label,image = align_right_icon)
    align_right_btn.grid(row = 0, column = 9,padx = 3)
    align_right_btn.configure(command = right_align_fun)
    
    # left_align

    align_left_btn = ttk.Button(tool_bars_label,image = align_left_icon)
    align_left_btn.grid(row = 0, column = 7,padx = 3)
    align_left_btn.configure(command = left_align_fun)
    
    # center_align

    align_center_btn = ttk.Button(tool_bars_label,image = align_center_icon)
    align_center_btn.grid(row = 0, column = 8,padx = 3)
    align_center_btn.configure(command = center_align_fun)


    show_status_bar = BooleanVar()
    show_status_bar.set (False)
    
    show_tool_bar = BooleanVar()
    show_tool_bar.set(True)

    veiwMenu = Menu(MenuBar, tearoff = 0)
 
    veiwMenu.add_checkbutton(label= "Tool Bar Hide",onvalue = True,offvalue = 0,image = tool_icon, compound = LEFT , command = toolbar)
    veiwMenu.add_checkbutton(label= "Status Bar Hide",image = status_icon, compound = LEFT , command = statusbar)
    MenuBar.add_cascade(label = "View", menu = veiwMenu)


    themeMenu = Menu(MenuBar, tearoff = 0)
    
    themeMenu.add_radiobutton(label = "Night", image = default_icon, compound = LEFT, command =default)
    themeMenu.add_radiobutton(label = "Light", image = light_icon, compound = LEFT, command =light)
    themeMenu.add_radiobutton(label = "Red", image = red_icon, compound = LEFT, command =red)
    themeMenu.add_radiobutton(label = "Blue", image = blue_icon, compound = LEFT, command =blue)
    themeMenu.add_radiobutton(label = "Monokai", image = monokai_icon, compound = LEFT, command =monokai)
    themeMenu.add_radiobutton(label = "Dark", image = dark_icon, compound = LEFT, command =dark)

    MenuBar.add_cascade(label = "Theme", menu = themeMenu)

    HelpMenu = Menu(MenuBar, tearoff= 0)
    HelpMenu.add_command(label = "About" ,image = about_icon,compound= LEFT, command = about)

    MenuBar.add_cascade(label= "Help", menu = HelpMenu)

    root.config(menu = MenuBar)
    
    #Text Area
    TextArea = Text(root, font = ("Consolas",12), undo=True)
    file = None
    TextArea.pack(fill = BOTH, expand = True)
    TextArea.focus_set()
    TextArea.config(wrap = "word", relief = SUNKEN)

    Scroll = Scrollbar(TextArea)
    Scroll.pack(side = RIGHT, fill =Y)
    Scroll.config(command = TextArea.yview)
    TextArea.config(yscrollcommand = Scroll.set)

    scrollx = Scrollbar(TextArea)
    scrollx.pack(side= BOTTOM, fill = X)
    scrollx.config(orient = "horizontal",command = TextArea.xview)
    TextArea.config(xscrollcommand=scrollx.set)

    # status Bar

    status_bars = ttk.Label(root,text = " Lines" , cursor = "arrow")
    status_bars.pack(side =BOTTOM, fill = X)
    text_change = False
    TextArea.bind("<<Modified>>",change_word)


    #notepad_features
    features = NotepadFeatures(TextArea)

    

    smartMenu = Menu(MenuBar, tearoff=0)
    smartMenu.add_command(label="Solve", image=solve_icon, compound=LEFT, command=features.solveSelection)
    smartMenu.add_command(label="Graph", image=plot_icon, compound=LEFT, command=features.plotSelection)
    
    plotMenu = Menu(smartMenu, tearoff=0)

    plotMenu.add_command(label="Bar Chart", command=lambda: plot_button_clicked('bar'))
    plotMenu.add_command(label="Pie Chart", command=lambda: plot_button_clicked('pie')) 
    plotMenu.add_command(label="Line Graph", command=lambda: plot_button_clicked('line'))
    plotMenu.add_command(label="Scatter", command=lambda: plot_button_clicked('scatter'))
    plotMenu.add_command(label="Heatmap", command=lambda: plot_button_clicked('heatmap'))
    plotMenu.add_command(label="Box Plot", command=lambda: plot_button_clicked('box'))
    smartMenu.add_cascade(label="Plot", menu=plotMenu, image=plot_icon, compound=LEFT)

    smartMenu.add_command(label="Google", image=google_icon, compound=LEFT, command=features.googleSelection)
    smartMenu.add_command(label="YouTube", image=youtube_icon, compound=LEFT, command=features.youtubeSelection)
    smartMenu.add_command(label="Chatbot", image=chatbot_icon, compound=LEFT, command=features.chatbotSelection)
    MenuBar.add_cascade(label="Smart Tools", menu=smartMenu)


    # === Import Menu ===
    importMenu = Menu(MenuBar, tearoff=0)
    importMenu.add_command(label="Import File", command=features.import_file_with_column_selection)
    MenuBar.add_cascade(label="Import", menu=importMenu)


    # root.bind_all("<Control-f>", find)
    root.bind_all("<Command-n>", newFile)
    root.bind_all("<Command-o>", openFile)
    root.bind_all("<Command-f>", find)
    root.bind_all("<Command-s>", saveFile)
    root.bind_all("<Command-Shift-S>", saveasFile)
    root.bind_all("<Command-q>", quitApp)
    root.bind_all("<Alt-x>", clear)  # Alt generally works as is on Mac
    root.bind_all("<Command-z>", undoFunction)  # Undo
    root.bind_all("<Command-y>", redoFunction)  # Redo (sometimes Command-Shift-Z is used for Redo on Mac)


    root.mainloop()