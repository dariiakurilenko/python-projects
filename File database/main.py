from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from configparser import ConfigParser
form = Tk()
W, H = 1000, 700
L, T = (form.winfo_screenwidth() - W) // 2, (form.winfo_screenheight() - H) // 2
form.geometry(f"{W}x{H}+{L}+{T}")
form.title("AmDBMSF - Парки Москвы")
parse = ConfigParser()
parse.read('./AmDBMSF.ini', encoding='utf-8')
data_parser = ConfigParser()
menu = Menu(tearoff=0)
fond = Menu(tearoff=0)
info = Menu(tearoff=0)
menu.add_cascade(label="Фонд", menu=fond)
menu.add_cascade(label="Справка", menu=info)
form.config(menu=menu)
paned = PanedWindow(orient=HORIZONTAL)
select_file = PanedWindow(master=paned, width=form.winfo_screenwidth()/5)
info_file = PanedWindow(master=paned, orient=VERTICAL)
paned.add(select_file)
paned.add(info_file)
paned.pack(fill=BOTH, expand=1)
info_text = ScrolledText(master=info_file)
list = Listbox(master=select_file)
image = Label(master=info_file, height=form.winfo_screenheight()//2, bg="white")
way = parse['main']['datapath']
def show_object(event):
    selected_section = data_parser.sections()[list.curselection()[0]]
    image_path = way + data_parser[selected_section]["image"]
    info_path = way + data_parser[selected_section]["info"]
    try:
        photo = PhotoImage(file=image_path)
        updated = int(round(photo.width() / (form.winfo_screenwidth() // 2), 1) * 0.7)
        photo = photo.subsample(updated + 1)
        image.config(image=photo)
        image.image = photo
        with open(info_path, "r", encoding="utf-8") as file:
            text = ''.join(file.readlines())
            info_text.config(state=NORMAL)
            info_text.delete('1.0', END)
            info_text.insert(END, text)
            info_text.config(state=DISABLED)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить информацию о парке: {e}")
def initialization():
    global data_parser, list, image, info_text, select_file, info_file, way
    try:
        data_parser = ConfigParser()
        data_parser.read(way + "index.ini", encoding='utf-8')
        sections = [x for x in data_parser.sections()]
        section_list = Variable(value=sections)
        list.config(listvariable=section_list)
        img_path = way + data_parser[sections[0]]["image"]
        img = PhotoImage(file=img_path)
        img = img.subsample(round(img.width() / (form.winfo_screenwidth() // 2)), 1)
        image.config(image=img)
        image.image = img
        with open(way + data_parser[sections[0]]["info"], "r", encoding="utf-8") as file:
            text = file.read()
            info_text.config(wrap="word")
            info_text.insert(END, text)
            info_text.config(state=DISABLED)
        list.bind("<<ListboxSelect>>", show_object)
        list.select_set(0)
        select_file.add(list)
        info_file.add(image)
        info_file.add(info_text)
    except Exception as e:
        messagebox.showerror(title="Ошибка", message=f"Не удалось загрузить информацию о парке: {e}")
def close():
    for widget in select_file.panes():
        select_file.remove(widget)
    for widget in info_file.panes():
        info_file.remove(widget)
def open_db():
    global way
    way = filedialog.askdirectory(initialdir="./") + "/"
    initialization()
def info_window():
    info_window = Tk()
    info_window.title("Содержание")
    Wid, Hei = 500, 500
    Lef, Top = (info_window.winfo_screenwidth() - Wid) // 2, (info_window.winfo_screenheight() - Hei) // 2
    info_window.geometry(f"{Wid}x{Hei}+{Lef}+{Top}")
    textbox = Text(info_window)
    textbox.pack(anchor=NW, fill=BOTH, padx=1, pady=1, expand=True)
    textbox.insert(END, "О программе... \nПрограмма визуализации файловой базы данных "
                        "\nБаза данных представляет собой папку с файлами "
                        "\n\nКоманды программы:\nF1 - Вызов справки \nАвторские права: \n(c)Kurilenko, Moscow, 2024 ")
    textbox.config(state=DISABLED)
fond.add_command(label="Открыть", command=open_db)
fond.add_separator()
fond.add_command(label="Выход", command=close)
info.add_command(label="Содержание", command=lambda title_="О программе...",
                                text_="Программа визуализации файловой базы данных: "
                                "\n'Парки Москвы'  \nСпасибо моим родителям, Куриленко Сергею Николаевичу и Куриленко Ирине Викторовне, за все! Очень сильно люблю! "
                                "\n\n(c)Kurilenko, Moscow, 2024":messagebox.showinfo(title=title_, message=text_))
info.add_separator()
info.add_command(label="О программе", command=info_window)
form.bind("<F1>", info_window)
initialization()
form.mainloop()