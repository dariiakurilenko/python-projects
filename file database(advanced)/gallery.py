from tkinter import *
from tkinter import filedialog, messagebox
from configparser import ConfigParser
import webbrowser
import os
def create_gallery(main_window, initial_path):
    def choose_folder():
        nonlocal initial_path
        initial_path = filedialog.askdirectory(initialdir=initial_path)
        path_label.config(text=initial_path)
        gallery_window.lift()
    def generate_gallery():
        if "index.ini" not in os.listdir(initial_path):
            messagebox.showerror("Ошибка", "Выбрана неверная папка")
            return
        config = ConfigParser()
        config.read(initial_path + "/index.ini", encoding='utf-8')
        files = [x for x in config.sections()]
        files.insert(0, "index")
        if len(files) > 1:
            with open(initial_path + "/index.html", "w", encoding="utf-8") as index_file:
                index_file.write(f'<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>Галерея</title></head><body bgcolor="#FF7518"><p align="center"><font size="30"><b>Галерея</b></font></p><p align="center"><font size="40" color="#FDE910"><b>Парки Москвы</b></font></p><p align="center"><font size="20"><a href="{initial_path + "/" + files[1]}.html">Начать просмотр</a></font></p></body></html>')
            for i in range(1, len(files) - 1):
                with open(initial_path + "/" + files[i] + ".html", "w", encoding="utf-8") as file:
                    with open(initial_path + "/" + config[config.sections()[i - 1]]["info"], "r", encoding="utf-8") as info_file:
                        text = ''.join(info_file.readlines())
                    photo_width, photo_height = PhotoImage(file=initial_path + "/" + config[config.sections()[i - 1]]["image"]).width(), PhotoImage(file=initial_path + "/" + config[config.sections()[i - 1]]["image"]).height()
                    file.write(f'<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>{files[i]}</title></head><body bgcolor="#66FF00"><p align="center"><font size="40"><b>{files[i]}</b></font></p><p align="center"><img src="{initial_path + "/" + config[config.sections()[i - 1]]["image"]}" width="800" height="{photo_height // (photo_width / 800)}"></p><p align="left">{text}</p><p align="center"><font size="18"><a href="{initial_path + "/" + files[i - 1]}.html">Назад</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="{initial_path + "/" + files[i + 1]}.html">Вперед</a></font></p></body></html>')
            with open(initial_path + "/" + files[-1] + ".html", "w", encoding="utf-8") as file:
                with open(initial_path + "/" + config[config.sections()[-1]]["info"], "r", encoding="utf-8") as info_file:
                    text = ''.join(info_file.readlines())
                photo_width, photo_height = PhotoImage(file=initial_path + "/" + config[config.sections()[-1]]["image"]).width(), PhotoImage(file=initial_path + "/" + config[config.sections()[i - 1]]["image"]).height()
                file.write(f'<!DOCTYPE html><html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><title>{files[i]}</title></head><body bgcolor="#CCFF99"> <p align="center"><font size="40"><b>{files[-1]}</b></font></p><p align="center"><img src="{initial_path + "/" + config[config.sections()[-1]]["image"]}" width="800" height="{photo_height // (photo_width / 800)}"></p><p align="left">{text}</p><p align="center"><font size="18"><a href="{initial_path + "/" + files[-2]}.html">Назад</a>&nbsp;&nbsp;&nbsp;&nbsp;<a href="{initial_path + "/" + files[0]}.html">В начало галереи</a></font></p></body></html>')
            if open_browser_var.get():
                webbrowser.open(initial_path + "/index.html")
            gallery_window.destroy()
        else:
            messagebox.showerror("Ошибка", "В базе данных нет элементов")
    initial_path = os.path.abspath(initial_path)
    gallery_window = Toplevel(master=main_window)
    gallery_window.title("Создание галереи")
    gallery_window.geometry(f"{main_window.winfo_screenwidth() // 2}x{main_window.winfo_screenheight() // 2}+{main_window.winfo_screenwidth() // 4}+{main_window.winfo_screenheight() // 4}")
    for i in range(3):
        gallery_window.columnconfigure(index=i, weight=1)
    for j in range(3):
        gallery_window.rowconfigure(index=j, weight=1)
    path_label = Label(gallery_window, text=initial_path)
    path_label.grid(column=0, row=0, columnspan=3)
    choose_folder_button = Button(master=gallery_window, text="...", command=choose_folder)
    choose_folder_button.grid(column=2, row=0)
    open_browser_var = BooleanVar()
    open_browser_checkbox = Checkbutton(master=gallery_window, text="Открыть в браузере", variable=open_browser_var)
    open_browser_checkbox.grid(column=0, row=2)
    create_button = Button(master=gallery_window, text="Создать галерею", command=generate_gallery)
    create_button.grid(column=1, row=2)
    close_button = Button(master=gallery_window, text="Закрыть", command=lambda: gallery_window.destroy())
    close_button.grid(column=2, row=2)