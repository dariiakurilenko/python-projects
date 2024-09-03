from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
from configparser import ConfigParser
import gallery
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
way = parse['main']['datapath']
def show_object(event):
    index = files_ls.curselection()[0]
    img_file = way + data_parser[data_parser.sections()[index]]["image"]
    txt_file = way + data_parser[data_parser.sections()[index]]["info"]
    img = PhotoImage(file=img_file)
    image.config(image=img)
    image.image = img
    info_text.config(state=NORMAL)
    info_text.delete('1.0', END)
    with open(txt_file, "r", encoding="utf-8") as f:
        text = ''.join(f.readlines())
        info_text.insert(END, text)
        info_text.config(state=DISABLED)
def initialization():
    global data_parser, files_ls, image, info_text, select_file, info_file, way
    try:
        close()
        data_parser = ConfigParser()
        data_parser.read(way + "index.ini", encoding='utf-8')
        files_ls.config(listvariable=Variable(value=[x for x in data_parser.sections()]))
        listscroll.config(command=files_ls.yview)
        files_ls.config(yscrollcommand=listscroll.set)
        image_path = way + data_parser[data_parser.sections()[0]]["image"]
        photo = PhotoImage(file=image_path)
        image.config(image=photo)
        image.image = photo
        info_text.config(state=NORMAL)
        info_text.delete('1.0', END)
        info_path = way + data_parser[data_parser.sections()[0]]["info"]
        with open(info_path, "r", encoding="utf-8") as file:
            text = ''.join(file.readlines())
            info_text.config(wrap="word")
            info_text.insert(END, text)
            info_text.config(state=DISABLED)
            info_text.pack(fill=BOTH, expand=1)
        files_ls.bind("<<ListboxSelect>>", show_object)
        files_ls.select_set(0)
        select_file.add(frame)
        info_file.add(image)
        info_file.add(info_text)
    except Exception:
        messagebox.showerror(title="Ошибка", message="Выбрана неверная папка")
def close():
    for selected_item in select_file.panes():
        select_file.remove(selected_item)
    for selected_item in info_file.panes():
        info_file.remove(selected_item)
def open_db():
    global way
    way = filedialog.askdirectory(initialdir="./") + "/"
    initialization()
def info_window():
    info_window = Tk()
    info_window.title("О программе")
    wid, hei = 500, 500
    lef, top = (info_window.winfo_screenwidth() - wid) // 2, (info_window.winfo_screenheight() - hei) // 2
    info_window.geometry(f"{wid}x{hei}+{lef}+{top}")
    textbox = Text(info_window)
    textbox.pack(anchor=NW, fill=BOTH, padx=1, pady=1, expand=True)
    textbox.insert(END, "О программе... \nПрограмма визуализации файловой базы данных "
                        "\nБаза данных представляет собой папку с файлами "
                        "\n\nКоманды программы:\nF1 - Вызов справки \nАвторские права: \n(c)Kurilenko, Moscow, 2024 ")
    textbox.config(state=DISABLED)
fond.add_command(label="Открыть", command=open_db)
fond.add_command(label="Галерея", command=lambda: gallery.create_gallery(form, way))
fond.add_command(label="Закрыть", command=close)
fond.add_separator()
fond.add_command(label="Выход", command=lambda: form.destroy())
info.add_command(label="Содержание", command=lambda title_="Содержание", text_="Программа визуализации файловой базы "
                                                                               "данных: "
                                "\n'Парки Москвы'  \nСпасибо моим родителям, Куриленко Сергею Николаевичу и Куриленко "
                                                                               "Ирине Викторовне за все! "
                                "\n\n(c)Kurilenko, Moscow, 2024": messagebox.showinfo(title=title_, message=text_))
info.add_separator()
info.add_command(label="О программе", command=info_window)
menu.add_cascade(label="Фонд", menu=fond)
menu.add_cascade(label="Справка", menu=info)
form.config(menu=menu)
main_pw = PanedWindow(orient=HORIZONTAL)
select_file = PanedWindow(master=main_pw, width=form.winfo_screenwidth()//5)
info_file = PanedWindow(master=main_pw, orient=VERTICAL)
main_pw.add(select_file)
main_pw.add(info_file)
frame = Frame()
main_pw.pack(fill=BOTH, expand=1)
info_text = ScrolledText(master=info_file)
files_ls = Listbox(master=frame)
listscroll = Scrollbar(frame, orient=VERTICAL)
image = Label(master=info_file, height=form.winfo_screenheight()//8*5, bg="white")
form.bind("<F1>", lambda event: info_window())
files_ls.pack(side=LEFT, fill=BOTH, expand=1)
listscroll.pack(side=LEFT, fill=Y)
initialization()
form.mainloop()
