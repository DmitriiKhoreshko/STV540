import customtkinter
from customtkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
import os
from PIL import Image
import re
import shutil
import json
import copy
from PyQt5.QtCore import *  
from PyQt5.QtWidgets import *
from pyqtgraph import *
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import *
import sys
from collections import Counter
#------------------Меню---------------------
# Глобальные переменные 
windowsize=[1600,900]     
globalfolderpage=19
globalresearchespage=19
foldersfilter="filter-off"
researchesfilter="filter-off"
pagetype="folders"
compare=0
comparelist=[]

# Изображения 
image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "images")
logo_image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo.png")),size=(100,100))
logo_menu_image=customtkinter.CTkImage(Image.open(os.path.join(image_path, "logo_menu.png")),size=(172,71))
load_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "download.png")),size=(100,100))
compare_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "compare.png")),size=(130,130))
cross_image= customtkinter.CTkImage(Image.open(os.path.join(image_path, "cross.png")),size=(15,15))
folder_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "papka.png")),size=(50,50))
delete_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "trash.png")),size=(50,50))
exit_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "exit.png")),size=(50,50))
filter_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "filter.png")),size=(50,50))
toleft_image= customtkinter.CTkImage(Image.open(os.path.join(image_path, "toleft.png")),size=(30,30))
toright_image= customtkinter.CTkImage(Image.open(os.path.join(image_path, "toright.png")),size=(30,30))
tostart_image= customtkinter.CTkImage(Image.open(os.path.join(image_path, "tostart.png")),size=(30,30))
empty_image = customtkinter.CTkImage(Image.new("RGBA", (512, 512),(255, 255, 255, 0)),size=(15,15))
# Цвета 
fg_grey_color="#DBDBDB"
fg_darkgrey_color="#CFCFCF"
fg_green_color="#69AF63"
fg_red_color="#69AF63"
fg_yellow_color="#ffde00"

hover_grey_color="#BBBBBB"
hover_darkgrey_color="#BBBBBB"
hover_green_color="#039323"
hover_red_color="#039323"

disabled_color="#979797"

class MainMenu(customtkinter.CTkFrame): # главное меню
    def __init__(self, master, **kwargs):
        class LeftMenu(customtkinter.CTkFrame): # левый фрейм меню с настройками, загрузкой исследований и т.д.
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                def load_btn(): #кнопка загрузки исследований
                    files=filedialog.askopenfilenames()
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    for file in files:
                        shutil.copy(file, os.getcwd())
                        stats=[file]
                        app.frame_Menu.frame_RightMenu.json_add(stats)
                    os.chdir("../")
                    app.frame_Menu.frame_RightMenu.page_refresh(0)    
                
                self.grid_columnconfigure(0, weight=1, uniform="a")
                self.grid_rowconfigure((0,2), weight=1, uniform="a")
                self.grid_rowconfigure((1), weight=0, uniform="a")
                self.label540=customtkinter.CTkLabel(self, corner_radius=0, text="",image=logo_menu_image, text_color=fg_green_color)
                self.label540.grid(row=0, column=0,pady=(20,0),sticky="n" )
                self.button1=customtkinter.CTkButton(self, command=load_btn, image=load_image, height=150,width=150, text='', state="disabled", fg_color=disabled_color) #fg_color=("#00A825"), hover_color=("#039323")
                self.button1.grid(row=1, column=0,  pady=(0,0), padx=(40,40),sticky="n")
                self.label2=customtkinter.CTkLabel(self, text="ЗАГРУЗИТЬ \nИССЛЕДОВАНИЕ", font=("Arial", 18))
                self.label2.grid(row=1, column=0, pady=(160,0),sticky="n")
                self.button2=customtkinter.CTkButton(self, command=self.compare_btn, image=compare_image, height=150,width=150, text='', state="disabled", fg_color=disabled_color) #fg_color=("#0087FF"), hover_color=("#00548D")
                self.button2.grid(row=1, column=0, pady=(240,0),sticky="n")
                self.label3=customtkinter.CTkLabel(self, text="СРАВНИТЬ \nИССЛЕДОВАНИЯ", font=("Arial", 18))
                self.label3.grid(row=1, column=0, pady=(400,0),sticky="n")
                self.button3=customtkinter.CTkButton(self, command=self.compare_transit_btn, height=40,width=200, text='Сравнить', fg_color=disabled_color, hover_color=hover_green_color,text_color="Black", font=("Arial", 18, "bold"), state="disabled")
            
            def compare_btn(self): # кнопка включения режима выбора исследований для сравнения
                global compare
                compare=compare!=1
                if compare==1:
                    self.button1.configure(fg_color=disabled_color, state="disabled")
                    self.button2.configure(fg_color=hover_green_color)
                    self.button3.configure(fg_color=disabled_color, state="disabled")
                    self.button3.grid(row=2, column=0, pady=(0,20), sticky = "s")
                    app.frame_Menu.frame_RightMenu.frame_folders.wipe_all()
                    app.frame_Menu.frame_RightMenu.json_check()
                    app.frame_Menu.frame_RightMenu.page_refresh(0)
                if compare==0:
                    self.button1.configure(fg_color=fg_green_color, state="normal")
                    self.button2.configure(fg_color=fg_green_color)
                    self.button3.grid_forget()
                    comparelist.clear()
                    app.frame_Menu.frame_RightMenu.frame_folders.wipe_all()
                    app.frame_Menu.frame_RightMenu.json_check()
                    app.frame_Menu.frame_RightMenu.page_refresh(0)
            def compare_transit_btn(self): # кнопка перехода в модуль сравнения исследований
                datalist=[]
                comparelist.sort(key=lambda x: datetime.strptime(x.split(".")[0], '%Y_%m_%d_%H_%M_%S'), reverse=True)
                os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                for i in range(len(comparelist)):
                    with open(str(comparelist[i]), 'r+') as file:
                        data = json.load(file)
                        datalist.append(data)
                os.chdir("../")
                CompareSpace(datalist,app)

        class RightMenu(customtkinter.CTkFrame): # правый фрейм меню с выбором папок/исследований
            def __init__(self, master, **kwargs):
                if (str(os.getcwd()).split("\\")[-1]!="Researches"):
                    os.chdir("Researches")
                class custom_folder_btn(customtkinter.CTkButton): # кастомная кнопка, которая позволяет разместить на себе другие кнопки и разный текст
                            def __init__(self, master, filename="",date="",lastdate="",macadress="",**kwargs): # расставление виджетов внутри кастомной кнопки
                                super().__init__(master, **kwargs)
                                def res_btn(): #совершает переход в окно работы с исследованием после нажатия по исследованию из списка
                                    global pagetype, globalresearchespage, foldersfilter
                                    pagetype="researches"
                                    globalresearchespage=19
                                    if foldersfilter=="filter-on":
                                        app.frame_Menu.frame_RightMenu.filterbuttonreset.grid_forget()
                                    app.frame_Menu.frame_RightMenu.clear_selections()
                                    app.frame_Menu.frame_RightMenu.frame_folders.wipe_all()
                                    app.frame_Menu.frame_RightMenu.frame_folders.grid_forget()
                                    app.frame_Menu.frame_RightMenu.frame_researches.grid(row=1,column=0, padx=20, pady=(0,10), sticky="nsew")
                                    app.frame_Menu.frame_RightMenu.deletebutton.grid_forget()
                                    app.frame_Menu.frame_RightMenu.folderbutton.grid_forget()
                                    app.frame_Menu.frame_RightMenu.filterbutton.grid(row=0, column=0, pady=20, padx=(0,20),sticky="e")    
                                    app.frame_Menu.frame_RightMenu.exitbutton.grid(row=0, column=0, pady=20, padx=(20,0),sticky="w")                                    
                                    app.frame_Menu.frame_LeftMenu.button1.configure(fg_color=fg_green_color, hover_color=hover_green_color,state="normal")
                                    app.frame_Menu.frame_LeftMenu.button2.configure(fg_color=fg_green_color, hover_color=hover_green_color,state="normal")
                                    app.frame_Menu.frame_RightMenu.label.configure(text=filename)
                                    app.frame_Menu.frame_RightMenu.json_check()
                                    app.frame_Menu.frame_RightMenu.page_refresh(0)
                                    app.frame_Menu.frame_RightMenu.frame_researches._parent_canvas.yview_moveto(0.0)
                                self.configure(text="",command=res_btn, fg_color=fg_grey_color, hover_color=hover_grey_color, height=20)
                                self.grid_rowconfigure(0,weight=10,uniform="a")
                                def delete():
                                    if (str(os.getcwd()).split("\\")[-1]=="Researches"):
                                        class delete_folder_dialog(customtkinter.CTkToplevel): # подтверждение удаления папки
                                            def __init__(self, *args, **kwargs):
                                                x = app.winfo_x()+ ((app.winfo_width() / 2) - 170)
                                                y = app.winfo_y() + ((app.winfo_height() / 2) - 80)
                                                super().__init__(*args, **kwargs)
                                                def func():
                                                    os.chdir("../")
                                                    defaulticon=os.path.join("images", "logo.ico")
                                                    self.iconbitmap(defaulticon)
                                                    os.chdir("Researches")
                                                self.after(250, func)
                                                def yes():
                                                    shutil.rmtree(os.getcwd()+"\\"+filename)
                                                    app.frame_Menu.frame_RightMenu.json_delete(filename)
                                                    app.frame_Menu.frame_RightMenu.name_list_refresh()
                                                    app.frame_Menu.frame_RightMenu.page_refresh(0)
                                                    delete_btn()
                                                    top_levelwindow.destroy()  
                                                def no():
                                                    top_levelwindow.destroy() 
                                                self.title("Подтвердите удаление")
                                                self.geometry('%dx%d+%d+%d' % (340, 160, x, y))
                                                self.resizable(False, False)       
                                                self.grid_columnconfigure((0,1),weight=1, uniform="a")
                                                self.grid_rowconfigure((0),weight=1, uniform="a")
                                                self.configure(fg_color=fg_grey_color)
                                                self.label=customtkinter.CTkLabel(self, text="Вы точно хотите удалить папку?", font=("Arial", 18))
                                                self.label.grid(row=0, column=0, pady=(0,10),columnspan=2)
                                                self.button_yes = customtkinter.CTkButton(self, text="ДА",command=yes, fg_color=fg_red_color, hover_color=hover_red_color, text_color="Black", font=("Arial", 18))
                                                self.button_yes.grid(row=1,column=0,sticky="s", pady=(0,20))
                                                self.button_no = customtkinter.CTkButton(self, text="НЕТ",command=no, fg_color=fg_green_color,hover_color=hover_green_color, text_color="Black", font=("Arial", 18,"bold"))
                                                self.button_no.grid(row=1,column=1,sticky="s", pady=(0,20))
                                        top_levelwindow=delete_folder_dialog(master=self)
                                        top_levelwindow.grab_set()                       
                                self.label1 = customtkinter.CTkLabel(master=self, text=filename,corner_radius=0,fg_color=self._fg_color, font=("Arial", 18))
                                self.label1.grid(row=0, column=0,pady=(0,0))
                                self.label2 = customtkinter.CTkLabel(master=self, text=date,fg_color=self._fg_color, font=("Arial", 18))
                                self.label2.grid(row=0, column=1,pady=(0,0))
                                self.label3 = customtkinter.CTkLabel(master=self, text=lastdate,fg_color=self._fg_color, font=("Arial", 18))
                                self.label3.grid(row=0, column=2,pady=(0,0))
                                self.label4 = customtkinter.CTkLabel(master=self, text=macadress,fg_color=self._fg_color, font=("Arial", 18))
                                self.label4.grid(row=0, column=3,pady=(0,0)) 
                                self.label5 = customtkinter.CTkButton(master=self, text="",fg_color=self._fg_color,corner_radius=5, height=20, width=15, command=delete, state="disabled", image=empty_image)
                                self.label5.grid(row=0, column=4, sticky="e",pady=(4,0), padx=(0,3)) 
                                labels = [self.label1,self.label2,self.label3,self.label4, self.label5]
                                for label in labels:
                                    label.bind("<Enter>", self._on_enter)
                                    label.bind("<Leave>", self._on_leave)
                                    label.bind("<Button-1>", self._clicked)
                            def _on_enter(self, event=None):
                                super()._on_enter() # переопределение метода ввода мыши в зону виджета
                                labels = [self.label1,self.label2,self.label3,self.label4,self.label5]
                                if self._state!="disabled":
                                    for label in labels:
                                        label.configure(fg_color=self._apply_appearance_mode(self._hover_color),bg_color=self._apply_appearance_mode(self._hover_color))
                            def _on_leave(self, event=None): # переопределение метода увода мыши из зоны виджета
                                super()._on_leave()
                                labels = [self.label1,self.label2,self.label3,self.label4,self.label5]
                                if self._state!="disabled":
                                    for label in labels:
                                        label.configure(fg_color=self._apply_appearance_mode(self._fg_color),bg_color=self._apply_appearance_mode(self._fg_color))
                            def _create_grid(self): # переопределение метода формирования сетки расположения виджетов
                                super()._create_grid()
                                self.grid_columnconfigure((0,1,2,3,4), weight=0)
                                self.grid_columnconfigure((3), weight=1,uniform="a")
                                self.grid_columnconfigure((1,2), weight=1,uniform="a")
                                self.grid_columnconfigure((0), weight=2,uniform="a")
                class custom_research_btn(custom_folder_btn): # унаследовал кастомную кнопку папок для кнопки раздела исследований
                    def __init__(self, master,Date,Time,MacAdress,GestationalAge,name, **kwargs): # расставление виджетов внутри кастомной кнопки
                            def delete():
                                    class ToplevelWindow(customtkinter.CTkToplevel): # подтверждение удаления исследования
                                        def __init__(self, *args, **kwargs):
                                            x = app.winfo_x()+ ((app.winfo_width() / 2) - 170)
                                            y = app.winfo_y() + ((app.winfo_height() / 2) - 80)
                                            super().__init__(*args, **kwargs)
                                            def func():
                                                    os.chdir("../")
                                                    defaulticon=os.path.join("images", "logo.ico")
                                                    self.iconbitmap(defaulticon)
                                                    os.chdir("Researches")
                                            self.after(250, func)
                                            def yes():
                                                text1=app.frame_Menu.frame_RightMenu.label._text
                                                path=os.getcwd()+"\\"+text1+"\\"+name
                                                os.remove(path)
                                                app.frame_Menu.frame_RightMenu.json_delete(name)
                                                app.frame_Menu.frame_RightMenu.page_refresh(0)
                                                top_levelwindow.destroy()  
                                            def no():
                                                top_levelwindow.destroy() 
                                            self.title("Подтвердите удаление")
                                            self.geometry('%dx%d+%d+%d' % (340, 160, x, y))
                                            self.resizable(False, False)       
                                            self.grid_columnconfigure((0,1),weight=1, uniform="a")
                                            self.grid_rowconfigure((0,1),weight=1, uniform="a")
                                            self.label=customtkinter.CTkLabel(self, text="Вы точно хотите \nудалить исследование?", font=("Arial", 18))
                                            self.label.grid(row=0, column=0, pady=(0,10),columnspan=2)
                                            self.button_yes = customtkinter.CTkButton(self, text="ДА",command=yes, fg_color=fg_red_color,hover_color=hover_red_color, text_color="Black", font=("Arial", 18))
                                            self.button_yes.grid(row=1,column=0)
                                            self.button_no = customtkinter.CTkButton(self, text="НЕТ",command=no, fg_color=fg_green_color,hover_color=hover_green_color, text_color="Black", font=("Arial", 18,"bold"))
                                            self.button_no.grid(row=1,column=1)
                                    top_levelwindow=ToplevelWindow(app)
                                    top_levelwindow.grab_set()
                                    top_levelwindow.geometry()
                            super().__init__(master, **kwargs)
                            if compare==1:
                                try:
                                    comparelist.index(name)
                                    self.configure(fg_color=hover_grey_color)
                                    self.label1.configure(fg_color=hover_grey_color)
                                    self.label2.configure(fg_color=hover_grey_color)
                                    self.label3.configure(fg_color=hover_grey_color)
                                    self.label4.configure(fg_color=hover_grey_color)
                                except:   
                                    self.configure(fg_color=fg_grey_color)
                                    self.label1.configure(fg_color=fg_grey_color)
                                    self.label2.configure(fg_color=fg_grey_color)
                                    self.label3.configure(fg_color=fg_grey_color)
                                    self.label4.configure(fg_color=fg_grey_color)
                                self.label5.configure(text="",fg_color=self._fg_color, hover_color=self._hover_color, height=20, width=29,corner_radius=0, state="disabled",image=empty_image)
                            else:
                                self.label5.configure(state="normal",bg_color=self._apply_appearance_mode(self._fg_color), fg_color=fg_red_color, hover_color=hover_red_color,command=delete, image=cross_image,border_width=2,border_color="Black" )
                                self.label5.unbind("<Enter>")
                                self.label5.unbind("<Leave>")
                                self.label5.unbind("<Button-1>")
                            self.label1.configure(text=Date)
                            self.label2.configure(text=Time)
                            self.label3.configure(text=GestationalAge)
                            self.label4.configure(text=MacAdress)
                            self.label6=name
                            def result():
                                if compare!=1:
                                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                                    with open(name, 'r+') as file:
                                        data = json.load(file)
                                    os.chdir("../")
                                    WorkSpace(data,app)
                                else:
                                    try:
                                        comparelist.index(name)
                                        comparelist.remove(name)
                                        self.configure(fg_color=fg_grey_color)
                                        self.label1.configure(fg_color=fg_grey_color)
                                        self.label2.configure(fg_color=fg_grey_color)
                                        self.label3.configure(fg_color=fg_grey_color)
                                        self.label4.configure(fg_color=fg_grey_color)
                                        self.label5.configure(fg_color=fg_grey_color, bg_color=fg_grey_color)
                                        if len(comparelist)<2:
                                            app.frame_Menu.frame_LeftMenu.button3.configure(fg_color=disabled_color,state="disabled")
                                        else:
                                            app.frame_Menu.frame_LeftMenu.button3.configure(fg_color=fg_green_color,state="normal")
                                    except:   
                                        comparelist.append(name)
                                        self.configure(fg_color=hover_grey_color)
                                        self.label1.configure(fg_color=hover_grey_color)
                                        self.label2.configure(fg_color=hover_grey_color)
                                        self.label3.configure(fg_color=hover_grey_color)
                                        self.label4.configure(fg_color=hover_grey_color)
                                        self.label5.configure(fg_color=hover_grey_color, bg_color=hover_grey_color)
                                        if len(comparelist)<2:
                                            app.frame_Menu.frame_LeftMenu.button3.configure(fg_color=disabled_color,state="disabled")
                                        else:
                                            app.frame_Menu.frame_LeftMenu.button3.configure(fg_color=fg_green_color,state="normal")
                            self.configure(command=result)
                    def _on_enter(self, event=None):
                        super()._on_enter() # переопределение метода ввода мыши в зону виджета
                        if self._state!="disabled":
                            if compare!=1:
                                self.label5.configure(fg_color=self._apply_appearance_mode(fg_red_color),bg_color=self._apply_appearance_mode(self._hover_color))
                    def _on_leave(self, event=None): # переопределение метода увода мыши из зоны виджета
                        super()._on_leave()
                        if self._state!="disabled":
                            if compare!=1:
                                self.label5.configure(fg_color=self._apply_appearance_mode(fg_red_color),bg_color=self._apply_appearance_mode(self._fg_color))
                    def _create_grid(self): # переопределение метода формирования сетки расположения виджетов
                            super()._create_grid()
                            self.grid_columnconfigure((0,1,2,3,4), weight=0)
                            self.grid_columnconfigure((3), weight=2,uniform="a")
                            self.grid_columnconfigure((2), weight=1,uniform="a")
                            self.grid_columnconfigure((0,1), weight=1,uniform="a")  
                class folder_label(customtkinter.CTkLabel): # Кастомный заголовок для раздела папок
                            def __init__(self, master, **kwargs): # расставление виджетов внутри заголовка папок
                                super().__init__(master, **kwargs)
                                self.label1 = customtkinter.CTkButton(master=self,command=lambda:app.frame_Menu.frame_RightMenu.json_sort("filename"), text=" Название",fg_color=fg_darkgrey_color, font=("Arial", 18,"bold"), text_color="Black",hover_color=hover_darkgrey_color, height=60)
                                self.label1.grid(row=0, column=0,pady=(15,0),sticky="ew",padx=(4,0))
                                self.label2 = customtkinter.CTkButton(master=self,command=lambda:app.frame_Menu.frame_RightMenu.json_sort("Date"), text=" Дата\n создания",fg_color=fg_darkgrey_color, font=("Arial", 18,"bold"), text_color="Black",hover_color=hover_darkgrey_color, height=60)
                                self.label2.grid(row=0, column=1,pady=(15,0),sticky="ew")
                                self.label3 = customtkinter.CTkButton(master=self,command=lambda:app.frame_Menu.frame_RightMenu.json_sort("LastDate"), text=" Дата последнего\n исследования",fg_color=fg_darkgrey_color, font=("Arial", 18,"bold"),hover_color=hover_darkgrey_color, text_color="Black", height=60)
                                self.label3.grid(row=0, column=2,pady=(15,0),sticky="ew")
                                self.label4 = customtkinter.CTkButton(master=self,command=lambda:app.frame_Menu.frame_RightMenu.json_sort("MacAdress"), text=" Прибор,\n MAC-адресс",fg_color=fg_darkgrey_color, font=("Arial", 18,"bold"),hover_color=hover_darkgrey_color, text_color="Black", height=60)
                                self.label4.grid(row=0, column=3,pady=(15,0),sticky="ew")  
                                self.label5 = customtkinter.CTkButton(master=self, text="",fg_color=self._fg_color,corner_radius=0, height=20, width=29, state="disabled",image=empty_image)
                                self.label5.grid(row=0, column=4, sticky="e", padx=(0,18))
                            def _create_grid(self): # переопределение метода формирования сетки расположения виджетов
                                super()._create_grid()
                                self.grid_columnconfigure((0,1,2,3,4), weight=0)
                                self.grid_columnconfigure((3), weight=1,uniform="a")
                                self.grid_columnconfigure((1,2), weight=1,uniform="a")
                                self.grid_columnconfigure((0), weight=2,uniform="a")
                class researches_label(folder_label): # Кастомный заголовок для раздела исследований, унаследован от заголовка папок
                            def __init__(self, master, **kwargs): # расставление виджетов внутри заголовка исследований
                                super().__init__(master, **kwargs)
                                self.label1.configure(text=" Дата")
                                self.label2.configure(text=" Время начала\n исследования") 
                                self.label3.configure(text=" Срок,\n недель")
                            def _create_grid(self): # переопределение метода формирования сетки расположения виджетов
                                super()._create_grid()
                                self.grid_columnconfigure((0,1,2,3,4), weight=0)
                                self.grid_columnconfigure((3), weight=2,uniform="a")
                                self.grid_columnconfigure((2), weight=1,uniform="a")
                                self.grid_columnconfigure((0,1), weight=1,uniform="a")                              
                class frame_folders(customtkinter.CTkScrollableFrame):   # список папок    
                    def __init__(self, master,label=folder_label ,**kwargs):
                        super().__init__(master, **kwargs)
                        label=label(self._parent_frame)
                        self._label=label
                        self.configure(label_text=" ")
                        self.grid_columnconfigure(0, weight=1)
                        self.item_list = []
                    def add_item(self,name,date,lastdate,macadress): # добавить элемент в список папок
                        item = custom_folder_btn(self,name,date,lastdate,macadress)
                        item.grid(row=len(self.item_list),pady=(5,0), padx=5, sticky="ew")
                        self.item_list.append(item)
                    def wipe_all(self): #очистить recycler view
                        for item in self.item_list[::-1]:
                            if item!=self._label:
                                self.item_list.remove(item)
                                item.destroy()
                    def next_page(self): # переход на следующую страницу
                        app.frame_Menu.frame_RightMenu.frame_folders._parent_canvas.yview_moveto(0.0)
                        app.frame_Menu.frame_RightMenu.page_refresh(19)
                    def prev_page(self):# переход на предыдущую страницу
                        app.frame_Menu.frame_RightMenu.frame_folders._parent_canvas.yview_moveto(0.0)
                        app.frame_Menu.frame_RightMenu.page_refresh(-19)                                
                class frame_researches(frame_folders):   # список исследований, унаследован от списка папок
                    def __init__(self, master, **kwargs):
                        super().__init__(master,label=researches_label, **kwargs)
                    def add_item(self,Date,Time,MacAdress,GestationalAge,name): # добавить элемент в список исследований
                        item = custom_research_btn(self,Date,Time,MacAdress,GestationalAge,name)
                        item.grid(row=len(self.item_list),pady=(5,0), padx=5, sticky="ew")
                        self.item_list.append(item)
                class dialog_filter(customtkinter.CTkToplevel): # диалог фильтра
                    class FolderSettings(customtkinter.CTkFrame): # фрейм фильтра папок
                            def __init__(self, master, **kwargs):
                                super().__init__(master, **kwargs)
                                def reset():
                                    self.cal_entry.delete(0,"end")
                                    self.cal1_entry.delete(0,"end")
                                    self.name_entry.delete(0,"end")
                                    self.MAC_entry.delete(0,"end")
                                    self.from_entry.delete(0,"end")
                                    self.to_entry.delete(0,"end")
                                def find():
                                    app.frame_Menu.frame_RightMenu.clear_selections()
                                    filter=[self.name_entry.get(), self.cal_entry.get(),self.cal1_entry.get(),self.MAC_entry.get(),self.from_entry.get(),self.to_entry.get()]
                                    if filter!=["","","","","",""]:
                                        global foldersfilter, globalfolderpage
                                        globalfolderpage = 19 
                                        foldersfilter= "filter-on"
                                        app.frame_Menu.frame_RightMenu.filterbuttonreset.grid(row=0, column=0, pady=20, padx=(20,0),sticky="w")
                                        app.frame_Menu.frame_RightMenu.filter_json_sort(filter)
                                        app.frame_Menu.frame_RightMenu.page_refresh(0)
                                        master.destroy()
                                self.grid_columnconfigure((0,1,2),weight=1,uniform="a")
                                self.grid_rowconfigure((0,2),weight=1,uniform="a")
                                self.grid_rowconfigure((1,3),weight=0)
                                self.configure(fg_color=fg_darkgrey_color)
                                self.name=customtkinter.CTkLabel(master=self, text="Название", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6, height=100)
                                self.name.grid(row=0, column=0,sticky="nsew",padx=(10,5),pady=(10,0))
                                self.name_entry = customtkinter.CTkEntry(master=self, placeholder_text="",border_width=1, border_color="#7a7a7a", corner_radius=0,fg_color="#FFFFFF")
                                self.name_entry.grid(row=1,column=0,sticky="new",padx=(10,5),pady=(10))
                                self.cal=customtkinter.CTkLabel(master=self, text="Дата создания", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.cal.grid(row=0, column=1,sticky="nsew",pady=(10,0),padx=(5,5))
                                self.cal_entry = DateEntry(master=self, date_pattern="dd.mm.yyyy",locale="ru",cursor="")
                                self.cal_entry.delete(0,"end")
                                self.cal_entry.grid(row=1,column=1,sticky="nsew",padx=(5,5),pady=(10))
                                self.cal1=customtkinter.CTkLabel(master=self, text="Дата последнего\nисследования", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.cal1.grid(row=0, column=2,sticky="nsew",pady=(10,0),padx=(5,10))
                                self.cal1_entry = DateEntry(master=self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.cal1_entry.delete(0,"end")
                                self.cal1_entry.grid(row=1,column=2,sticky="nsew",padx=(5,10),pady=(10))
                                self.from_to=customtkinter.CTkLabel(master=self, text="Период мониторинга", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.from_to.grid(row=2, column=1,columnspan=2,sticky="nsew",padx=(5,10),pady=(0,10))
                                self.from_entry=DateEntry(self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.from_entry.grid(row=3,column=1,sticky="nsew",padx=(5,5),pady=(0,10))
                                self.from_entry.delete(0,"end")
                                self.to_entry=DateEntry(master=self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.to_entry.grid(row=3,column=2,sticky="nsew",padx=(5,10),pady=(0,10))
                                self.to_entry.delete(0,"end")
                                self.MAC=customtkinter.CTkLabel(master=self, text="Прибор,\n MAC-адресс", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.MAC.grid(row=2, column=0,sticky="nsew",padx=(10,5),pady=(0,10))
                                self.MAC_entry = customtkinter.CTkEntry(master=self, placeholder_text="",border_width=1, border_color="#7a7a7a", corner_radius=0,fg_color="#FFFFFF")
                                self.MAC_entry.grid(row=3,column=0,sticky="new",padx=(10,5),pady=(0,10))
                                self.button_find = customtkinter.CTkButton(master, text="Поиск",command=find, fg_color=fg_green_color, hover_color=hover_green_color,text_color="Black", font=("Arial", 18))
                                self.button_find.grid(row=2,column=0,sticky="e",padx=10,pady=(10,10))
                                self.button_reset = customtkinter.CTkButton(master, text="Cбросить",command=reset, fg_color=fg_grey_color, hover_color=hover_grey_color,text_color="Black", font=("Arial", 18))
                                self.button_reset.grid(row=2,column=1,sticky="w",padx=10,pady=(10,10))
                    class ResearchesSettings(customtkinter.CTkFrame): # фрейм фильтра исследований
                            def __init__(self, master, **kwargs):
                                super().__init__(master, **kwargs)
                                def reset():
                                    self.cal_entry.delete(0,"end")
                                    self.cal1_entry.delete(0,"end")
                                    self.name_entry.delete(0,"end")
                                    self.MAC_entry.delete(0,"end")
                                    self.from_entry.delete(0,"end")
                                    self.to_entry.delete(0,"end")
                                def find():
                                    app.frame_Menu.frame_RightMenu.clear_selections()
                                    filter=[self.name_entry.get(), self.MAC_entry.get(),self.from_entry.get(),self.to_entry.get(),self.cal_entry.get(),self.cal1_entry.get()]
                                    if filter!=["","","","","",""]:
                                        global researchesfilter, globalresearchespage
                                        globalresearchespage = 19 
                                        researchesfilter = "filter-on"
                                        app.frame_Menu.frame_RightMenu.filterbuttonreset.grid(row=2, column=0, pady=(0,10), padx=(20,0),sticky="w")
                                        app.frame_Menu.frame_RightMenu.filter_json_sort(filter)
                                        app.frame_Menu.frame_RightMenu.page_refresh(0)
                                        master.destroy()
                                self.grid_columnconfigure((0,1,2),weight=1,uniform="a")
                                self.grid_rowconfigure((0,2),weight=1,uniform="a")
                                self.grid_rowconfigure((1,3),weight=0)
                                self.configure(fg_color=fg_darkgrey_color)
                                self.name=customtkinter.CTkLabel(master=self, text="Дата", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6, height=100)
                                self.name.grid(row=0, column=0,sticky="nsew",padx=(10,5),pady=(10,0))
                                self.name_entry = DateEntry(master=self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.name_entry.grid(row=1,column=0,sticky="nsew",padx=(10,5),pady=(10))
                                self.name_entry.delete(0,"end")
                                self.cal=customtkinter.CTkLabel(master=self, text="Период беременности, недель", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.cal.grid(row=0, column=1,columnspan=2,sticky="nsew",pady=(10,0),padx=(5,10))
                                self.cal_entry = customtkinter.CTkEntry(master=self, placeholder_text="",border_width=1, border_color="#7a7a7a", corner_radius=0,fg_color="#FFFFFF")
                                self.cal_entry.grid(row=1,column=1,sticky="nsew",padx=(5,5),pady=(10))
                                self.cal1_entry = customtkinter.CTkEntry(master=self, placeholder_text="",border_width=1, border_color="#7a7a7a", corner_radius=0,fg_color="#FFFFFF")
                                self.cal1_entry.grid(row=1,column=2,sticky="nsew",padx=(5,10),pady=(10))
                                self.from_to=customtkinter.CTkLabel(master=self, text="Период мониторинга", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.from_to.grid(row=2, column=1,columnspan=2,sticky="nsew",padx=(5,10),pady=(0,10))
                                self.from_entry=DateEntry(self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.from_entry.grid(row=3,column=1,sticky="nsew",padx=(5,5),pady=(0,10))
                                self.from_entry.delete(0,"end")
                                self.to_entry=DateEntry(master=self, date_pattern="dd.mm.yyyy",locale="ru")
                                self.to_entry.grid(row=3,column=2,sticky="nsew",padx=(5,10),pady=(0,10))
                                self.to_entry.delete(0,"end")
                                self.MAC=customtkinter.CTkLabel(master=self, text="Прибор,\n MAC-адресс", font=("Arial", 18),fg_color=fg_grey_color, corner_radius=6)
                                self.MAC.grid(row=2, column=0,sticky="nsew",padx=(10,5),pady=(0,10))
                                self.MAC_entry = customtkinter.CTkEntry(master=self, placeholder_text="",border_width=1, border_color="#7a7a7a", corner_radius=0,fg_color="#FFFFFF")
                                self.MAC_entry.grid(row=3,column=0,sticky="new",padx=(10,5),pady=(0,10))
                                self.button_find = customtkinter.CTkButton(master, text="Поиск",command=find, fg_color=fg_green_color, hover_color=hover_green_color,text_color="Black", font=("Arial", 18))
                                self.button_find.grid(row=2,column=0,sticky="e",padx=10,pady=(10,10))
                                self.button_reset = customtkinter.CTkButton(master, text="Cбросить",command=reset, fg_color=fg_grey_color, hover_color=hover_grey_color,text_color="Black", font=("Arial", 18))
                                self.button_reset.grid(row=2,column=1,sticky="w",padx=10,pady=(10,10))
                    def __init__(self, *args, **kwargs):
                        x = app.winfo_x()+ ((app.winfo_width() / 2) - 350)
                        y = app.winfo_y() + ((app.winfo_height() / 2) - 150)
                        super().__init__(*args, **kwargs)
                        self.protocol("WM_DELETE_WINDOW", self._on_closing)
                        def func():
                            os.chdir("../")
                            defaulticon=os.path.join("images", "logo.ico")
                            self.iconbitmap(defaulticon)
                            os.chdir("Researches")
                        self.after(250, func)
                        self.title("Фильтр")
                        self.configure(fg_color=fg_grey_color)
                        self.geometry('%dx%d+%d+%d' % (700, 320, x, y))
                        self.resizable(False, False)       
                        self.grid_columnconfigure((0,1),weight=1, uniform="a")
                        self.grid_rowconfigure((0,2,3),weight=0)
                        self.grid_rowconfigure((1),weight=1, uniform="a")
                        self.label=customtkinter.CTkLabel(master=self, text="Задайте параметры фильтрации", font=("Arial", 30))
                        self.label.grid(row=0, column=0,columnspan=2,pady=10)
                        if pagetype=="folders":
                            self.settings_frame=self.FolderSettings(master=self)
                        else: self.settings_frame=self.ResearchesSettings(master=self)
                        self.settings_frame.grid(row=1,column=0,columnspan=2,sticky="EW",padx=20)
                        self.grab_set()
                    def _on_closing(self):
                        self.grab_release()
                        self.destroy()
                def folder_create_btn(): #выполнение действий после нажатия по кнопке "создать папку"
                    class dialog(customtkinter.CTkInputDialog):
                        def __init__(self):
                            super().__init__()
                            def func():
                                os.chdir("../")
                                defaulticon=os.path.join("images", "logo.ico")
                                self.iconbitmap(defaulticon)
                                os.chdir("Researches")
                            self.after(250, func)
                            x = app.winfo_x()+ ((app.winfo_width() / 2) - 170)
                            y = app.winfo_y() + ((app.winfo_height() / 2) - 80)
                            self.geometry('%dx%d+%d+%d' % (340, 160, x, y))
                            self.configure(fg_color=fg_grey_color)
                            self._font=("Arial", 18)
                            self._text="Введите название папки:"
                            self.title("Создать папку")
                        def _create_widgets(self):
                            super()._create_widgets()
                            self._ok_button.configure(text="Создать",fg_color=fg_green_color, hover_color=hover_green_color, font=("Arial", 18),text_color="Black")
                            self._cancel_button.configure(text="Отмена",fg_color=fg_green_color, hover_color=hover_green_color, font=("Arial", 18),text_color="Black")
                    folderdialog=dialog()
                    if (str(os.getcwd()).split("\\")[-1]!="Researches"):
                        os.chdir("Researches")
                    foldername=folderdialog.get_input()
                    if ((foldername!=None) and ((re.compile("[a-zA-Zа-яА-ЯёЁ0-9]+").search(foldername) is not None)==True)):
                        os.mkdir(foldername)
                        Date=datetime.fromtimestamp(os.path.getctime(foldername)).strftime("%d.%m.%Y")
                        stats=[foldername,Date]
                        self.json_add(stats)
                        app.frame_Menu.frame_RightMenu.page_refresh(0)
                def delete_btn(): #выполнение действий после нажатия по кнопке "удалить папку"
                    if self.deletebutton._fg_color==fg_grey_color:
                        self.deletebutton.configure(fg_color=hover_grey_color)
                    else: self.deletebutton.configure(fg_color=fg_grey_color)
                        
                    for name in self.frame_folders.item_list:
                        if name._state=="normal":
                            name.configure(state="disabled", fg_color=disabled_color)
                            name.label1.configure(fg_color=disabled_color,bg_color=disabled_color)
                            name.label2.configure(fg_color=disabled_color,bg_color=disabled_color)
                            name.label3.configure(fg_color=disabled_color,bg_color=disabled_color)
                            name.label4.configure(fg_color=disabled_color,bg_color=disabled_color)
                            name.label5.configure(state="normal",bg_color=disabled_color, fg_color=fg_red_color, hover_color=hover_red_color, image=cross_image,border_color="Black",border_width=2 )
                        else:
                            name.configure(state="normal", fg_color=fg_grey_color)
                            name.label1.configure(fg_color=name._fg_color,bg_color=name._fg_color)
                            name.label2.configure(fg_color=name._fg_color,bg_color=name._fg_color)
                            name.label3.configure(fg_color=name._fg_color,bg_color=name._fg_color)
                            name.label4.configure(fg_color=name._fg_color,bg_color=name._fg_color)
                            name.label5.configure(state="disabled",bg_color=name._fg_color, fg_color=name._fg_color, hover_color="", image = empty_image,border_color="",border_width=0 )
                def exit_btn(): #вернуться в фрейм выбора папки
                    global pagetype,researchesfilter
                    if compare==1:
                        app.frame_Menu.frame_LeftMenu.compare_btn()
                    pagetype="folders"
                    if researchesfilter=="filter-on":
                        researchesfilter="filter-off"
                        app.frame_Menu.frame_RightMenu.filterbuttonreset.grid_forget()
                    if foldersfilter=="filter-on":
                        app.frame_Menu.frame_RightMenu.filterbuttonreset.grid(row=0, column=0, pady=20, padx=(20,0),sticky="w")   
                    app.frame_Menu.frame_RightMenu.frame_folders.grid(row=1,column=0, padx=20, pady=(0,10), sticky="nsew")
                    app.frame_Menu.frame_RightMenu.frame_researches.wipe_all()
                    app.frame_Menu.frame_RightMenu.frame_researches.grid_forget()
                    self.folderbutton=customtkinter.CTkButton(self, command=folder_create_btn, height=60,width=60, text='', fg_color=fg_grey_color, hover_color=hover_grey_color, image=folder_image)
                    self.folderbutton.grid(row=0, column=0, pady=20, padx=(0,20),sticky="e")
                    self.deletebutton.grid(row=0, column=0, pady=20, padx=(0,170),sticky="e")
                    self.filterbutton.grid_forget()
                    self.filterbutton.grid(row=0, column=0, pady=20, padx=(0,95),sticky="e")
                    app.frame_Menu.frame_RightMenu.exitbutton.grid_forget()
                    app.frame_Menu.frame_LeftMenu.button1.configure(fg_color=("#979797"),state="disabled")
                    app.frame_Menu.frame_LeftMenu.button2.configure(fg_color=("#979797"),state="disabled")
                    self.label.configure(text="Выберите папку")
                    app.frame_Menu.frame_RightMenu.json_check()
                    self.page_refresh(0) 
                def filter_btn():
                    top_levelwindow=dialog_filter()
                def reset_filter_btn():
                    global pagetype
                    if pagetype=="folders":
                        global foldersfilter, globalfolderpage
                        globalfolderpage=19
                        foldersfilter="filter-off"
                        self.clear_selections()
                        self.filterbuttonreset.grid_forget()
                        self.page_refresh(0)
                    else:
                        global researchesfilter, globalresearchespage
                        globalresearchespage=19
                        researchesfilter="filter-off"
                        self.clear_selections()
                        self.filterbuttonreset.grid_forget()
                        self.page_refresh(0)
                def to_start():
                    if pagetype=="folders":
                        global globalfolderpage
                        globalfolderpage=19
                    else:
                        global globalresearchespage
                        globalresearchespage=19
                    self.page_refresh(0)
                super().__init__(master, **kwargs)                       
                self.grid_columnconfigure(0, weight=1, uniform="a")
                self.grid_rowconfigure(1, weight=13, uniform="a")
                self.grid_rowconfigure((0,2,3,4,5), weight=0)
                self.label=customtkinter.CTkLabel(self, text="Выберите папку",font=("Arial", 30))
                self.label.grid(row=0, column=0, padx=0, sticky="ew")
                self.folderbutton=customtkinter.CTkButton(self, command=folder_create_btn, height=60,width=60, text='', fg_color=fg_grey_color, hover_color=hover_grey_color, image=folder_image)
                self.folderbutton.grid(row=0, column=0, pady=20, padx=(0,20),sticky="e")
                self.deletebutton=customtkinter.CTkButton(self, command=delete_btn, height=60,width=60, text='', fg_color=fg_grey_color, hover_color=hover_grey_color, image=delete_image)
                self.deletebutton.grid(row=0, column=0, pady=20, padx=(0,170),sticky="e")
                self.filterbutton=customtkinter.CTkButton(self, command=filter_btn, height=60,width=60, text='', image=filter_image, fg_color=fg_grey_color, hover_color=hover_grey_color)
                self.filterbutton.grid(row=0, column=0, pady=20, padx=(0,95),sticky="e")
                self.filterbuttonreset=customtkinter.CTkButton(self, command=reset_filter_btn, height=50,width=50, text='Сбросить фильтр',  fg_color=fg_red_color, hover_color=hover_red_color, font=("Arial", 18, "bold"), text_color="Black")
                self.exitbutton=customtkinter.CTkButton(self, command=exit_btn, height=60,width=60, text='', fg_color=fg_grey_color, hover_color=hover_grey_color, image=exit_image)
                self.frame_folders=frame_folders(master=self)
                self.frame_folders.grid(row=1,column=0, padx=20, pady=(0,10), sticky="nsew")
                self.frame_researches=frame_researches(master=self)
                self.next_btn=customtkinter.CTkButton(self, command=self.frame_folders.next_page, height=50,width=50,image=toright_image, text='', font=("Arial", 18), text_color="Black",fg_color=fg_grey_color, hover_color=hover_grey_color)
                self.next_btn.grid(row=2,padx=(160,0),pady=(0,10), column=0,sticky="s")
                self.back_btn=customtkinter.CTkButton(self, command=self.frame_folders.prev_page, height=50,width=50,image=toleft_image, text='', font=("Arial", 18), text_color="Black",fg_color=fg_grey_color, hover_color=hover_grey_color)
                self.back_btn.grid(row=2,padx=(0,160),pady=(0,10), column=0,sticky="s")
                self.tostart_btn=customtkinter.CTkButton(self, command=to_start, height=50,width=50, text='',image=tostart_image, font=("Arial", 18), text_color="Black",fg_color=fg_grey_color, hover_color=hover_grey_color)
                self.tostart_btn.grid(row=2,padx=(0,300),pady=(0,10), column=0,sticky="s")
                self.page_info=customtkinter.CTkLabel(self, text="(Ошибка)",font=("Arial", 18,"bold"))
                self.page_info.grid(row=2, column=0, padx=20,pady=(0,20),sticky="s")
                self.json_check()
                self.page_refresh(0)
            def json_check(self): # Проверка количества существующих папок/исследований и записанных в json
                if pagetype=="folders":
                    name_list=self.name_list_refresh()
                    size=len(os.listdir())
                    if os.path.isfile("foldersinfo.json"):
                        size-=1
                    if os.path.isfile("foldersfilter.json"):
                        size-=1
                                
                    if len(name_list)!=size:
                        self.json_refresh("folders")
                elif pagetype=="researches":
                    name_list=self.name_list_refresh("filesinfo.json")
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    size=len(os.listdir())
                    if os.path.isfile("filesinfo.json"):
                        size-=1
                    if os.path.isfile("filesfilter.json"):
                        size-=1
                    os.chdir("../")       
                    if len(name_list)!=size:
                        self.json_refresh()        
            def json_add(self, params): 
                global pagetype
                def exist(date1, name):
                    result=0
                    for exist in date1:
                        if exist["filename"]==name:
                            result=1
                            break
                    return result 
                   
                def write(data, name="foldersinfo.json"):
                    data=json.dumps(data)
                    data=json.loads(str(data))
                    with open(name,'w+', encoding="utf-8") as file:
                        json.dump(data,file,indent=3)
                        
                if pagetype=="folders":
                    if os.path.isfile("foldersinfo.json"):
                        with open("foldersinfo.json", 'r+') as file:
                            data = json.load(file)
                        if exist(data["folders"],params[0])==False:
                            data["folders"].append({
                                            "filename" : params[0],
                                            "Date" : params[1],
                                            "LastDate": "---",
                                            "MacAdress" : "---"
                                        })
                            write(data)
                            self.page_refresh(0)
                    else: self.json_refresh("folders")
                elif pagetype=="researches":
                    if os.path.isfile("filesinfo.json")==False:
                        data10= {
                        "files" : [],
                        "LastDate" : "---",
                        "MacAdress" : "---"
                        }         
                        with open("filesinfo.json",'w+', encoding="utf-8") as file:
                            json.dump(data10,file,indent=3)
                    with open("filesinfo.json", 'r+') as file:
                        data = json.load(file)
                    if exist(data["files"],str(params[0].split('/')[-1]))==False:
                        with open(params[0], 'r+') as file:
                                    data2 = json.load(file)
                                    Date = data2['DateTimeStart'].partition(' ')[0]
                                    Time=data2['DateTimeStart'].partition(' ')[2]
                                    MacAdress=data2['MacAdress']
                                    GestationalAge=str(data2['GestationalAge'])
                                    data["files"].append({
                                        "filename" : str(params[0].split('/')[-1]),
                                        "Date" : Date,
                                        "Time": Time,
                                        "MacAdress" : MacAdress,
                                        "GestationalAge" : GestationalAge
                                    })
                        if data["LastDate"]=="---" or datetime.strptime(data["LastDate"], '%d.%m.%Y')<datetime.strptime(data2['DateTimeStart'].partition(' ')[0], '%d.%m.%Y'):
                            data["LastDate"]=data2['DateTimeStart'].partition(' ')[0]
                            data["MacAdress"]=data2['MacAdress']
                        os.chdir("../")
                        with open('foldersinfo.json', 'r+') as file:
                                    data3 = json.load(file)
                        for name in data3["folders"]:           
                            if name["filename"]==app.frame_Menu.frame_RightMenu.label._text:
                                if (name["LastDate"]=="---"or datetime.strptime(name["LastDate"], '%d.%m.%Y')< datetime.strptime(data["LastDate"], '%d.%m.%Y')):
                                    name["LastDate"]=data["LastDate"]
                                    name["MacAdress"]=data["MacAdress"]
                                    write(data3,"foldersinfo.json")
                        os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                        write(data,"filesinfo.json")      
            def json_delete(self,params):
                global pagetype
                def position(date1, name):
                    result=0
                    for exist in date1:
                        if exist["filename"]==name:
                            break
                        result+=1
                    return result 
                   
                def write(data, name="foldersinfo.json"):
                    data=json.dumps(data)
                    data=json.loads(str(data))
                    with open(name,'w+', encoding="utf-8") as file:
                        json.dump(data,file,indent=3)
                        
                if pagetype=="folders":
                    if os.path.isfile("foldersinfo.json"):
                        with open("foldersinfo.json", 'r+') as file:
                            data = json.load(file)
                        del data["folders"][position(data["folders"],params)]
                        write(data,"foldersinfo.json")
                    if foldersfilter=="filter-on":    
                        if os.path.isfile("foldersfilter.json"):
                            with open("foldersfilter.json", 'r+') as file:
                                data = json.load(file)
                            del data["folders"][position(data["folders"],params)]
                            write(data,"foldersfilter.json")
                    self.page_refresh(0)
                elif pagetype=="researches":
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    if os.path.isfile("filesinfo.json"):
                        with open("filesinfo.json", 'r+') as file:
                            data = json.load(file)
                        del data["files"][position(data["files"],params)]   
                        write(data,"filesinfo.json") 
                    if researchesfilter=="filter-on":
                        if os.path.isfile("filesfilter.json"):
                            with open("filesfilter.json", 'r+') as file:
                                data = json.load(file)
                            del data["files"][position(data["files"],params)]   
                            write(data,"filesfilter.json") 
                    os.chdir("../")
                    self.page_refresh(0)               
            def json_refresh(self, type="researches"): # Обновление json файла, хранящего в себе информацию о файлах или папках
                def write(data, name="filesinfo.json"):
                    data=json.dumps(data)
                    data=json.loads(str(data))
                    with open(name,'w+', encoding="utf-8") as file:
                        json.dump(data,file,indent=3)    
                if type == "researches":
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)                         
                    data2= {
                        "files" : [],
                        "LastDate" : "LastDate",
                        "MacAdress" : "MacAdress"
                    }         
                    for name in os.listdir():
                        if (name!="filesinfo.json") and (name!="filesfilter.json") :
                            with open(name, 'r+') as file:
                                    data = json.load(file)
                                    Date = data['DateTimeStart'].partition(' ')[0]
                                    Time=data['DateTimeStart'].partition(' ')[2]
                                    MacAdress=data['MacAdress']
                                    GestationalAge=str(data['GestationalAge'])
                                    data2["files"].append({
                                        "filename" : name,
                                        "Date" : Date,
                                        "Time": Time,
                                        "MacAdress" : MacAdress,
                                        "GestationalAge" : GestationalAge
                                    })
                    data2["files"].sort(key=lambda x: datetime.strptime(x.get("Date"), '%d.%m.%Y'),reverse=True)
                    if len(data2["files"])>=1:
                        data2["LastDate"]=data2["files"][0]["Date"]
                        data2["MacAdress"]=data2["files"][0]["MacAdress"]
                    write(data2)
                    os.chdir("../") 
                elif type=="folders":
                    data2= {
                        "folders" : []
                    } 
                    for name in os.listdir():
                        LastDate="---"
                        MacAdress="---"
                        if (name!="foldersinfo.json") and (name!="foldersfilter.json"):
                            os.chdir(name)
                            if os.path.isfile("filesinfo.json"):
                                with open("filesinfo.json", 'r+') as file:
                                    data = json.load(file)
                                    if data["LastDate"]!="LastDate":
                                        LastDate=data["LastDate"]
                                        MacAdress=data["MacAdress"]
                            os.chdir("../")
                            Date=datetime.fromtimestamp(os.path.getctime(name)).strftime("%d.%m.%Y")
                            data2["folders"].append({
                                "filename" : name,
                                "Date" : Date,
                                "LastDate": LastDate,
                                "MacAdress" : MacAdress,
                            })    
                    write(data2,"foldersinfo.json")
            def clear_selections(self):
                global pagetype
                if pagetype=="folders":
                    path=app.frame_Menu.frame_RightMenu.frame_folders._label
                    path.label1.configure(text=" Название")
                    path.label2.configure(text=" Дата создания")
                    path.label3.configure(text=" Дата последнего\n исследования")
                    path.label4.configure(text=" Прибор,\n MAC-адресс")
                elif pagetype=="researches":
                    path=app.frame_Menu.frame_RightMenu.frame_researches._label
                    path.label1.configure(text=" Дата")
                    path.label2.configure(text=" Время начала\n исследования")
                    path.label3.configure(text=" Срок,\n недель")
                    path.label4.configure(text=" Прибор,\n MAC-адресс")           
            def json_sort(self,sorttype="filename"): # Сортировка json по заголовкам
                global pagetype
                if pagetype=="folders":
                    if foldersfilter=="filter-off":
                        sorting="foldersinfo.json" 
                    elif foldersfilter=="filter-on":
                        sorting="foldersfilter.json"
                    if os.path.isfile(sorting):
                        with open(sorting, 'r+') as file:
                            data= json.load(file)
                            temp=copy.deepcopy(data)
                            self.clear_selections()
                elif pagetype=="researches":
                    if researchesfilter=="filter-off":
                        sorting="filesinfo.json"
                    elif researchesfilter=="filter-on":
                        sorting="filesfilter.json"
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    if os.path.isfile(sorting):
                        with open(sorting, 'r+') as file:
                            data= json.load(file)
                            temp=copy.deepcopy(data)
                            self.clear_selections()
                    os.chdir("../") 
                def write(data, name=sorting):
                    data=json.dumps(data)
                    data=json.loads(str(data))
                    with open(name,'w+', encoding="utf-8") as file:
                        json.dump(data,file,indent=3)
                if pagetype=="folders":
                    path=app.frame_Menu.frame_RightMenu.frame_folders._label
                    if sorttype=="Date" or sorttype=="LastDate":
                        temp["folders"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'),reverse=True)
                    else: temp["folders"].sort(key=lambda x: x.get(sorttype))
                    if temp["folders"]!=data["folders"]:
                        if sorttype=="Date" or sorttype=="LastDate":
                            data["folders"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'),reverse=True)
                        else: data["folders"].sort(key=lambda x: x.get(sorttype))
                        match sorttype:
                            case "filename":
                                path.label1.configure(text=" Название ↓")
                            case "Date":
                                path.label2.configure(text=" Дата создания ↓")
                            case "LastDate":
                                path.label3.configure(text=" Дата последнего\n исследования ↓")
                            case "MacAdress":
                                path.label4.configure(text=" Прибор,\n MAC-адресс ↓")     
                    else:
                        if sorttype=="Date" or sorttype=="LastDate":
                            data["folders"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'))
                        else: data["folders"].sort(key=lambda x: x.get(sorttype),reverse=True)
                        match sorttype:
                            case "filename":
                                path.label1.configure(text=" Название ↑")
                            case "Date":
                                path.label2.configure(text=" Дата создания ↑")
                            case "LastDate":
                                path.label3.configure(text=" Дата последнего\n исследования ↑")
                            case "MacAdress":
                                path.label4.configure(text=" Прибор,\n MAC-адресс ↑")
                    write(data)
                elif pagetype=="researches":
                    match sorttype:
                        case "filename": sorttype="Date"
                        case "Date": sorttype="Time"
                        case "LastDate": sorttype="GestationalAge"
                        case "MacAdress": sorttype="MacAdress"
                    path=app.frame_Menu.frame_RightMenu.frame_researches._label
                    if sorttype=="Date":
                        temp["files"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'),reverse=True)
                    else: temp["files"].sort(key=lambda x: x.get(sorttype))
                    if temp["files"]!=data["files"]:
                        if sorttype=="Date" or sorttype=="LastDate":
                            data["files"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'),reverse=True)
                        else: data["files"].sort(key=lambda x: x.get(sorttype))
                        match sorttype:
                            case "Date":
                                path.label1.configure(text=" Дата ↓")
                            case "Time":
                                path.label2.configure(text=" Время начала\n исследования ↓")
                            case "GestationalAge":
                                path.label3.configure(text=" Срок,\n недель ↓")
                            case "MacAdress":
                                path.label4.configure(text=" Прибор,\n MAC-адресс ↓")     
                    else:
                        if sorttype=="Date":
                            data["files"].sort(key=lambda x: datetime.strptime(x.get(sorttype), '%d.%m.%Y'))
                        else: data["files"].sort(key=lambda x: x.get(sorttype),reverse=True)
                        match sorttype:
                            case "Date":
                                path.label1.configure(text=" Дата ↑")
                            case "Time":
                                path.label2.configure(text=" Время начала\n исследования ↑")
                            case "GestationalAge":
                                path.label3.configure(text=" Срок,\n недель ↑")
                            case "MacAdress":
                                path.label4.configure(text=" Прибор,\n MAC-адресс ↑")
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    write(data)          
                    os.chdir("../")
                app.frame_Menu.frame_RightMenu.page_refresh(0)           
            def filter_json_sort(self,filter=["","","","","",""]): #Фильтрация копии json информации о папках
                if pagetype=="folders":
                    def write(data, name="foldersfilter.json"):
                        data=json.dumps(data)
                        data=json.loads(str(data))
                        with open(name,'w+', encoding="utf-8") as file:
                            json.dump(data,file,indent=3)    
                    if os.path.isfile("foldersinfo.json"):
                        with open("foldersinfo.json", 'r+') as file:
                            data = json.load(file)
                    write(data)
                    name_list= {
                            "folders" : []
                        }                           
                    if os.path.isfile("foldersfilter.json"):
                        with open("foldersfilter.json", 'r+') as file:
                            data = json.load(file)
                            for name in data["folders"]:
                                if (((name["filename"]==filter[0])or (name["Date"]==filter[1]) or (name["LastDate"]==filter[2]) or (name["MacAdress"]==filter[3]))or(filter[4]!=""and filter[5]!="" and (datetime.strptime(name["LastDate"], '%d.%m.%Y')>=datetime.strptime(filter[4], '%d.%m.%Y'))and(datetime.strptime(name["LastDate"], '%d.%m.%Y')<=datetime.strptime(filter[5], '%d.%m.%Y')))):
                                    data2={"filename":"","Date":"", "LastDate":"","MacAdress":""}
                                    data2["filename"]=name['filename']
                                    data2["Date"]=name['Date']
                                    data2["LastDate"]=name['LastDate']
                                    data2["MacAdress"]=name['MacAdress']
                                    name_list["folders"].append(data2)          
                    write(name_list)
                elif pagetype=="researches":
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    def write(data, name="filesfilter.json"):
                        data=json.dumps(data)
                        data=json.loads(str(data))
                        with open(name,'w+', encoding="utf-8") as file:
                            json.dump(data,file,indent=3)    
                    if os.path.isfile("filesinfo.json"):
                        with open("filesinfo.json", 'r+') as file:
                            data = json.load(file)
                    write(data)
                    name_list= {
                            "files" : []
                        }                           
                    if os.path.isfile("filesfilter.json"):
                        with open("filesfilter.json", 'r+') as file:
                            data = json.load(file)
                            for name in data["files"]:
                                if ((((filter[0]!="" and datetime.strptime(name["Date"], '%d.%m.%Y')==datetime.strptime(filter[0], '%d.%m.%Y')) ) or (name["MacAdress"]==filter[1])) or (filter[2]!=""and filter[3]!="" and (datetime.strptime(name["Date"], '%d.%m.%Y')>=datetime.strptime(filter[2], '%d.%m.%Y'))and(datetime.strptime(name["Date"], '%d.%m.%Y')<=datetime.strptime(filter[3], '%d.%m.%Y')))or(filter[4]!=""and filter[5]!="" and (int(name["GestationalAge"])>=int(filter[4]))and(int(name["GestationalAge"])<=int(filter[5])))):   
                                    data2={"filename":"","Date":"", "Time":"","MacAdress":"","GestationalAge":""}
                                    data2["filename"]=name['filename']
                                    data2["Date"]=name['Date']
                                    data2["Time"]=name['Time']
                                    data2["MacAdress"]=name['MacAdress']
                                    data2["GestationalAge"]=name["GestationalAge"]
                                    name_list["files"].append(data2)          
                    write(name_list)
                    os.chdir("../")                
            def name_list_refresh(self, refreshlist="foldersinfo.json"): # обновление локальной библиотеки, которая подгружается из json файла
                name_list=[]
                if (refreshlist=="filesinfo.json") or (refreshlist=="filesfilter.json"):
                    os.chdir(app.frame_Menu.frame_RightMenu.label._text)
                    if os.path.isfile(refreshlist):
                        with open(refreshlist, 'r+') as file:
                            data = json.load(file)
                            for file in data["files"]:
                                data2={"filename":"","Date":"","Time":"", "GestationalAge":"","MacAdress":""}
                                data2["filename"]=file['filename']
                                data2["Date"]=file['Date']
                                data2["Time"]=file['Time']
                                data2["MacAdress"]=file['MacAdress']
                                data2["GestationalAge"]=file['GestationalAge']
                                name_list.append(data2)
                    os.chdir("../")
                    return name_list
                else:
                    if os.path.isfile(refreshlist):
                        with open(refreshlist, 'r+') as file:
                            data = json.load(file)
                            for file in data["folders"]:
                                data2={"Name":"","Date":"", "Time":"","MacAdress":""}
                                data2["filename"]=file['filename']
                                data2["Date"]=file['Date']
                                data2["LastDate"]=file['LastDate']
                                data2["MacAdress"]=file['MacAdress']
                                name_list.append(data2)
                    return name_list            
            def page_refresh(self,walk=0): # загрузить список папок
                realpage=19
                global globalfolderpage, globalresearchespage
                if self.deletebutton._fg_color==hover_grey_color:
                    self.deletebutton.configure(fg_color=fg_grey_color)
                if pagetype=="folders":
                    realpage=globalfolderpage
                    if foldersfilter=="filter-off":
                        name_list=self.name_list_refresh()
                    elif foldersfilter=="filter-on":
                        name_list=self.name_list_refresh("foldersfilter.json")
                    self.frame_folders.wipe_all()
                elif pagetype=="researches":
                    realpage=globalresearchespage
                    if researchesfilter=="filter-off":
                        name_list=self.name_list_refresh("filesinfo.json")
                    elif researchesfilter=="filter-on":
                        name_list=self.name_list_refresh("filesfilter.json")
                    self.frame_researches.wipe_all()
                def set_page(realpage=0):
                    if len(name_list)%19==0:
                        pages=len(name_list)//19
                        if pages==0: pages=1
                    else:
                        pages=len(name_list)//19+1
                    if realpage<=19:
                        page=1
                    else:
                        if realpage%19==0:
                            page=realpage//19
                        else:
                            page=(realpage//19)+1
                    stats=[page,pages]
                    return stats
               
                def restrictions(realpage): # активация/деакцтивация кнопки перелистывания страницы в зависимости от условий
                    if realpage>=len(name_list):
                        self.next_btn.configure(state="disabled", fg_color=disabled_color)
                    elif (self.next_btn._state=="disabled"):
                        self.next_btn.configure(state="normal", fg_color=fg_grey_color, hover_color=hover_grey_color)
                    if len(name_list)==realpage:
                        self.next_btn.configure(state="disabled", fg_color=disabled_color)
                    if realpage<=19:
                        self.tostart_btn.configure(state="disabled", fg_color=disabled_color)
                        self.back_btn.configure(state="disabled", fg_color=disabled_color)
                    if (self.back_btn._state=="disabled" and realpage>19): 
                        self.tostart_btn.configure(state="normal", fg_color=fg_grey_color)
                        self.back_btn.configure(state="normal", fg_color=fg_grey_color, hover_color=hover_grey_color)       
               
                def refresh(start,stop): #заполнение recycler view из выгруженного json 
                            for name in name_list[start:stop:]:
                                if pagetype=="folders":
                                    self.frame_folders.add_item(name["filename"],name["Date"],name["LastDate"],name["MacAdress"])
                                elif pagetype=="researches":
                                    self.frame_researches.add_item(name["Date"],name["Time"],name["MacAdress"],name["GestationalAge"],name["filename"])
                
                 
                if walk==19:
                    realpage+=19
                    if realpage>len(name_list):
                        realpage=len(name_list)
                    if realpage%19==0:
                        refresh(realpage-19,realpage)
                    else:
                        x=realpage//19
                        refresh(realpage-(realpage-19*x),realpage)
                elif (walk==-19):
                    if (realpage%19==0):
                        realpage-=19
                    else:
                        x=realpage//19
                        realpage-=(realpage-19*x)
                    refresh(realpage-19,realpage)
                elif(walk==0):
                    if realpage%19==0:
                        refresh(realpage-19,realpage)
                    else:
                        x=realpage//19
                        refresh(realpage-(realpage-19*x),realpage)
                
                restrictions(realpage)
                page_stats=set_page(realpage)    
                self.page_info.configure(text=str(page_stats[0])+" / "+str(page_stats[1]))
                
                if pagetype=="folders":
                    globalfolderpage=realpage
                elif pagetype=="researches":
                    globalresearchespage=realpage
                                        
        super().__init__(master, **kwargs) # главный фрейм меню
        self.grid_rowconfigure(0, weight=1,uniform="a")
        self.grid_columnconfigure(0, weight=0,uniform="a")
        self.grid_columnconfigure(1, weight=4,uniform="a")
        self.frame_LeftMenu=LeftMenu(master=self)
        self.frame_LeftMenu.grid(row=0,column=0, padx=(20,10), pady=20, sticky="ns")
        self.frame_RightMenu=RightMenu(master=self)
        self.frame_RightMenu.grid(row=0,column=1, padx=(10,20), pady=20, sticky="NSEW")

mMouseAction = 0 # Вариант взаимодействия с графиком
allocationGraph=0 #Элемент выделения
allocationSTVLTV=0 #Элемент выделения на графике STVLTV
ruler=0 # Переключатель линейки
ruleritem=0 # Объект линейки
firsttime=0 # Индикатор для перерасчета параметров на выделенном участке ( чтобы при первом выделении не перерасчитывалось 4 раза)
momcheck=1 # Опция отрисовки графика мамы
accelcheck=1 # Опция отрисовки меток акцелерации
decelcheck=1 # Опция отрисовки меток децелерации
cursorcheck=1 # Опция отрисовки подписи курсора
cursorsignal=1 # Параметр, позволяющий следить
        
def WorkSpace(data, app1): # рабочая область исследования
    app1.withdraw()
    class Ui_DialogGraphicOptions(object):
        def setupUi(self, DialogGraphicOptions):
            DialogGraphicOptions.setObjectName("DialogGraphicOptions")
            DialogGraphicOptions.resize(392, 177)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(DialogGraphicOptions.sizePolicy().hasHeightForWidth())
            DialogGraphicOptions.setSizePolicy(sizePolicy)
            DialogGraphicOptions.setMinimumSize(QtCore.QSize(392, 177))
            DialogGraphicOptions.setMaximumSize(QtCore.QSize(392, 185))
            #DialogGraphicOptions.setModal(True)
            self.DialogGridLayout = QtWidgets.QGridLayout(DialogGraphicOptions)
            self.DialogGridLayout.setContentsMargins(4, 4, 4, 4)
            self.DialogGridLayout.setObjectName("DialogGridLayout")
            self.DialogGraphicOptions_frameGlobal = QtWidgets.QFrame(DialogGraphicOptions)
            self.DialogGraphicOptions_frameGlobal.setStyleSheet("QFrame{\n"
    "    background-color: rgb(219, 219, 219);\n"
    "    border-radius:8px\n"
    "}")
            self.DialogGraphicOptions_frameGlobal.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.DialogGraphicOptions_frameGlobal.setFrameShadow(QtWidgets.QFrame.Raised)
            self.DialogGraphicOptions_frameGlobal.setObjectName("DialogGraphicOptions_frameGlobal")
            self.DialogGridLayout_Global = QtWidgets.QGridLayout(self.DialogGraphicOptions_frameGlobal)
            self.DialogGridLayout_Global.setObjectName("DialogGridLayout_Global")
            self.label = QtWidgets.QLabel(self.DialogGraphicOptions_frameGlobal)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(18)
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("label")
            self.DialogGridLayout_Global.addWidget(self.label, 0, 0, 1, 1)
            self.DialogGraphicOptions_frameLocal = QtWidgets.QFrame(self.DialogGraphicOptions_frameGlobal)
            self.DialogGraphicOptions_frameLocal.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    \n"
    "    background-color: rgb(207, 207, 207);\n"
    "}\n"
    "")
            self.DialogGraphicOptions_frameLocal.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.DialogGraphicOptions_frameLocal.setFrameShadow(QtWidgets.QFrame.Raised)
            self.DialogGraphicOptions_frameLocal.setObjectName("DialogGraphicOptions_frameLocal")
            self.DialogGridLayout_Local = QtWidgets.QGridLayout(self.DialogGraphicOptions_frameLocal)
            self.DialogGridLayout_Local.setObjectName("DialogGridLayout_Local")
            self.AccelMarksOption = QtWidgets.QCheckBox(self.DialogGraphicOptions_frameLocal)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.AccelMarksOption.setFont(font)
            if accelcheck==1:
                self.AccelMarksOption.setChecked(True)
            self.AccelMarksOption.setObjectName("AccelMarksOption")
            self.DialogGridLayout_Local.addWidget(self.AccelMarksOption, 2, 0, 1, 1)
            self.AccelMarksOption.stateChanged.connect(self.statechanged)
            self.CHSSMamaOption = QtWidgets.QCheckBox(self.DialogGraphicOptions_frameLocal)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.CHSSMamaOption.setFont(font)
            if momcheck==1:
                self.CHSSMamaOption.setChecked(True)
            self.CHSSMamaOption.setTristate(False)
            self.CHSSMamaOption.setObjectName("CHSSMamaOption")
            self.DialogGridLayout_Local.addWidget(self.CHSSMamaOption, 0, 0, 1, 1)
            self.CHSSMamaOption.stateChanged.connect(self.statechanged)
            self.DecelMarksOption = QtWidgets.QCheckBox(self.DialogGraphicOptions_frameLocal)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.DecelMarksOption.setFont(font)
            if decelcheck==1:
                self.DecelMarksOption.setChecked(True)
            self.DecelMarksOption.setObjectName("DecelMarksOption")
            self.DialogGridLayout_Local.addWidget(self.DecelMarksOption, 1, 0, 1, 1)
            self.DecelMarksOption.stateChanged.connect(self.statechanged)
            self.CursorInfoOption = QtWidgets.QCheckBox(self.DialogGraphicOptions_frameLocal)
            font = QtGui.QFont()
            font.setPointSize(12)
            self.CursorInfoOption.setFont(font)
            if cursorcheck==1:
                self.CursorInfoOption.setChecked(True)
            self.CursorInfoOption.setObjectName("CursorInfoOption")
            self.DialogGridLayout_Local.addWidget(self.CursorInfoOption, 3, 0, 1, 1)
            self.CursorInfoOption.stateChanged.connect(self.statechanged)
            self.CursorInfoOption.raise_()
            self.CHSSMamaOption.raise_()
            self.DecelMarksOption.raise_()
            self.AccelMarksOption.raise_()
            self.DialogGridLayout_Global.addWidget(self.DialogGraphicOptions_frameLocal, 1, 0, 1, 1)
            self.DialogGridLayout_Global.setRowStretch(0, 1)
            self.DialogGridLayout_Global.setRowStretch(1, 5)
            self.DialogGridLayout.addWidget(self.DialogGraphicOptions_frameGlobal, 0, 0, 1, 1)
            self.retranslateUi(DialogGraphicOptions)
            QtCore.QMetaObject.connectSlotsByName(DialogGraphicOptions)
        
        def statechanged(self):
            ui.graphicsView_Graph.getPlotItem().clear()
            ui.graphicsView_STVLTV.getPlotItem().clear()
            global accelcheck, decelcheck, momcheck, cursorcheck,cursorsignal
            accelcheck=self.AccelMarksOption.isChecked()
            decelcheck=self.DecelMarksOption.isChecked()
            momcheck=self.CHSSMamaOption.isChecked()
            cursorcheck=self.CursorInfoOption.isChecked()
            if cursorcheck==0 and cursorsignal==1:
                CVB.scene().sigMouseMoved.disconnect(ui.mouseMoved)
                cursorsignal=0
            ui.fillgraph()
            
        def retranslateUi(self, DialogGraphicOptions):
            _translate = QtCore.QCoreApplication.translate
            DialogGraphicOptions.setWindowIcon(QtGui.QIcon(os.path.join(image_path, "logo.ico")))
            DialogGraphicOptions.setWindowTitle(_translate("DialogGraphicOptions", "Настройки"))
            self.label.setText(_translate("DialogGraphicOptions", "Настройки графика"))
            self.AccelMarksOption.setText(_translate("DialogGraphicOptions", "Метки акцелерации"))
            self.CHSSMamaOption.setText(_translate("DialogGraphicOptions", "График ЧСС матери"))
            self.DecelMarksOption.setText(_translate("DialogGraphicOptions", "Метки децелерации"))
            self.CursorInfoOption.setText(_translate("DialogGraphicOptions", "Значения графика в позиции курсора"))
    
    class RectItem(QGraphicsItem):
                def __init__(self, rect,line,brush, parent=None,line_width=2):
                    super().__init__(parent)
                    self.setCacheMode(2)
                    self._rect = rect
                    self.picture = QtGui.QPicture()
                    self._generate_picture(line,brush,line_width)
                @property
                
                def rect(self):
                    return self._rect

                def _generate_picture(self,line,brush,line_width):
                    painter = QtGui.QPainter(self.picture)
                    painter.setPen(pg.mkPen(line,width=line_width))
                    painter.setBrush(pg.mkBrush(brush))
                    painter.drawRect(self.rect)
                    painter.end()

                def paint(self, painter, option, widget=None):
                    painter.drawPicture(0, 0, self.picture)
                
                def boundingRect(self):
                    return QtCore.QRectF(self.picture.boundingRect())
                
    class CustomViewBox(pg.ViewBox):    
        def __init__(self, *args, **kwds):
            pg.ViewBox.__init__(self, *args, **kwds)
            self.setMouseMode(self.PanMode)
        def mouseClickEvent(self, ev):
            global mMouseAction
            if ev.button() == QtCore.Qt.RightButton:
                self.setMouseMode(self.PanMode)
            elif ev.button() == QtCore.Qt.LeftButton:
                self.setMouseMode(self.PanMode)
        def mouseDragEvent(self, ev):
            global mMouseAction, mRange, allocationGraph, allocationSTVLTV
            if mMouseAction ==0:
                pg.ViewBox.mouseDragEvent(self, ev)
                ev.accept()
                mRange = Plot1.plotItem.viewRange()
            elif mMouseAction == 1:
                lastview=CVB.viewRange()
                pg.ViewBox.mouseDragEvent(self, ev)
                ev.accept()
                mRange = Plot1.plotItem.viewRange()
                CVB.suggestPadding = lambda *_: 0.0
                if ev.isFinish():
                    ui.button_segment.setStyleSheet("QPushButton{\n"
                    "    border-radius:8px;\n"
                    f"    background-color: {fg_grey_color};\n"
                    "}"
                    "QPushButton:hover{\n"
                    "    border-radius:8px;\n"
                    f"    background-color: {hover_grey_color};\n"
                    "}")
                    CVB.setMouseMode(CVB.PanMode)
                    mMouseAction=0
                    CVB.setYRange(50, 230,padding=0)
                    if CVB.viewRange()[0][0]<0:
                        x=0
                    else:
                        x=CVB.viewRange()[0][0]
                    rect_item = RectItem(QtCore.QRectF(x, 0, CVB.viewRange()[0][1]-x, 300),"#0078d7","#0078d7", line_width=0)
                    rect_item.setOpacity(0.3)
                    allocationGraph=rect_item
                    Plot1.addItem(rect_item)
                    rect_item = RectItem(QtCore.QRectF(x, -5, CVB.viewRange()[0][1]-x, 20),"#0078d7","#0078d7", line_width=0)
                    rect_item.setOpacity(0.3)
                    allocationSTVLTV=rect_item
                    Plot2.addItem(rect_item)
                    ui.spinBox_start_min.setValue(int(allocationGraph._rect.getRect()[0]//1))
                    ui.doubleSpinBox_start_sec.setValue(round((allocationGraph._rect.getRect()[0]%1)*60,3))
                    ui.spinBox_end_min.setValue(int((allocationGraph._rect.getRect()[0]+allocationGraph._rect.getRect()[2])//1))
                    ui.doubleSpinBox_end_sec.setValue(round((allocationGraph._rect.getRect()[0]+allocationGraph._rect.getRect()[2])%1*60,3))
                    CVB.setXRange(lastview[0][0], lastview[0][1], padding=0)
    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            global Plot1, Plot2,CVB,scatter, windowsize
            windowsize[0]=app1.winfo_width()
            windowsize[1]=app1.winfo_height()
            MainWindow.setObjectName("MainWindow")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            MainWindow.setMinimumSize(QtCore.QSize(843, 400))
            MainWindow.setBaseSize(QtCore.QSize(1280, 720))
            MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
            if app1.winfo_screenwidth()!=windowsize[0] and app1.winfo_screenheight()!=windowsize[1]:
                MainWindow.resize(windowsize[0], windowsize[1])
            else:
                MainWindow.showMaximized() 
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout_centralwidget = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout_centralwidget.setContentsMargins(-1, 0, -1, -1)
            self.gridLayout_centralwidget.setHorizontalSpacing(0)
            self.gridLayout_centralwidget.setVerticalSpacing(3)
            self.gridLayout_centralwidget.setObjectName("gridLayout_centralwidget")
            self.frame_header = QtWidgets.QFrame(self.centralwidget)
            self.frame_header.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_header.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_header.setObjectName("frame_header")
            self.gridLayout_frame_header = QtWidgets.QGridLayout(self.frame_header)
            self.gridLayout_frame_header.setContentsMargins(0, 3, 0, 0)
            self.gridLayout_frame_header.setHorizontalSpacing(6)
            self.gridLayout_frame_header.setVerticalSpacing(0)
            self.gridLayout_frame_header.setObjectName("gridLayout_frame_header")
            self.frame_header_right = QtWidgets.QFrame(self.frame_header)
            self.frame_header_right.setMinimumSize(QtCore.QSize(0, 80))
            self.frame_header_right.setMaximumSize(QtCore.QSize(16777215, 80))
            self.frame_header_right.setStyleSheet("QFrame{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(219, 219, 219);\n"
            "}")
            self.frame_header_right.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_header_right.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_header_right.setObjectName("frame_header_right")
            self.gridLayout_frame_header_right = QtWidgets.QGridLayout(self.frame_header_right)
            self.gridLayout_frame_header_right.setContentsMargins(18, 0, 18, 0)
            self.gridLayout_frame_header_right.setHorizontalSpacing(10)
            self.gridLayout_frame_header_right.setVerticalSpacing(6)
            self.gridLayout_frame_header_right.setObjectName("gridLayout_frame_header_right")
            self.button_file = QtWidgets.QPushButton(self.frame_header_right)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.button_file.sizePolicy().hasHeightForWidth())
            self.button_file.setSizePolicy(sizePolicy)
            self.button_file.setMinimumSize(QtCore.QSize(60, 60))
            self.button_file.setMaximumSize(QtCore.QSize(60, 60))
            self.button_file.setAutoFillBackground(False)
            self.button_file.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            f"    background-color: {disabled_color};\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"   background-color: {disabled_color};\n"
            "}")
            self.button_file.setIcon(QtGui.QIcon(os.path.join(image_path, "file.png")))
            self.button_file.setText("")
            self.button_file.setIconSize(QtCore.QSize(50, 50))
            self.button_file.setObjectName("button_file")
            self.gridLayout_frame_header_right.addWidget(self.button_file, 1, 4, 1, 1)
            self.button_print = QtWidgets.QPushButton(self.frame_header_right)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.button_print.sizePolicy().hasHeightForWidth())
            self.button_print.setSizePolicy(sizePolicy)
            self.button_print.setMinimumSize(QtCore.QSize(60, 60))
            self.button_print.setMaximumSize(QtCore.QSize(60, 60))
            self.button_print.setMouseTracking(False)
            self.button_print.setAutoFillBackground(False)
            self.button_print.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            f"    background-color: {disabled_color};\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"   background-color: {disabled_color};\n"
            "}")
            self.button_print.setIcon(QtGui.QIcon(os.path.join(image_path, "print.png")))
            self.button_print.setText("")
            self.button_print.setIconSize(QtCore.QSize(50, 50))
            self.button_print.setObjectName("button_print")
            self.gridLayout_frame_header_right.addWidget(self.button_print, 1, 5, 1, 1)
            self.button_segment = QtWidgets.QPushButton(self.frame_header_right)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.button_segment.sizePolicy().hasHeightForWidth())
            self.button_segment.setSizePolicy(sizePolicy)
            self.button_segment.setMinimumSize(QtCore.QSize(60, 60))
            self.button_segment.setMaximumSize(QtCore.QSize(60, 60))
            self.button_segment.setAutoFillBackground(False)
            self.button_segment.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            f"    background-color: {fg_grey_color};\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_grey_color};\n"
            "}")
            self.button_segment.setIcon(QtGui.QIcon(os.path.join(image_path, "segment.png")))
            self.button_segment.clicked.connect(self.event_select)
            self.button_segment.setText("")
            self.button_segment.setIconSize(QtCore.QSize(50, 50))
            self.button_segment.setObjectName("button_segment")
            self.gridLayout_frame_header_right.addWidget(self.button_segment, 1, 3, 1, 1)
            self.button_ruler = QtWidgets.QPushButton(self.frame_header_right)
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(self.button_ruler.sizePolicy().hasHeightForWidth())
            self.button_ruler.setSizePolicy(sizePolicy)
            self.button_ruler.setMinimumSize(QtCore.QSize(60, 60))
            self.button_ruler.setMaximumSize(QtCore.QSize(60, 60))
            self.button_ruler.setAutoFillBackground(False)
            self.button_ruler.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            f"    background-color: {fg_grey_color};\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_grey_color};\n"
            "}")
            self.button_ruler.clicked.connect(self.event_ruler)
            self.button_ruler.setIcon(QtGui.QIcon(os.path.join(image_path, "ruler.png")))
            self.button_ruler.setText("")
            self.button_ruler.setIconSize(QtCore.QSize(50, 50))
            self.button_ruler.setObjectName("button_ruler")
            self.gridLayout_frame_header_right.addWidget(self.button_ruler, 1, 2, 1, 1)
            self.label = QtWidgets.QLabel(self.frame_header_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(20)
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("label")
            self.gridLayout_frame_header_right.addWidget(self.label, 1, 6, 1, 1)
            self.button_exit = QtWidgets.QPushButton(self.frame_header_right)
            self.button_exit.setMinimumSize(QtCore.QSize(60, 60))
            self.button_exit.setMaximumSize(QtCore.QSize(60, 60))
            self.button_exit.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(105, 175, 99);\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_green_color};\n"
            "}")
            self.button_exit.setIconSize(QtCore.QSize(50, 50))
            self.button_exit.setIcon(QtGui.QIcon(os.path.join(image_path, "exit.png")))
            self.button_exit.clicked.connect(self.event_exit_btn)
            self.button_exit.setText("")
            self.button_exit.setObjectName("button_exit")
            self.gridLayout_frame_header_right.addWidget(self.button_exit, 1, 1, 1, 1)
            self.button_options = QtWidgets.QPushButton(self.frame_header_right)
            self.button_options.setMinimumSize(QtCore.QSize(60, 60))
            self.button_options.setMaximumSize(QtCore.QSize(60, 60))
            self.button_options.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            f"    background-color: {fg_grey_color};\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_grey_color};\n"
            "}")
            self.button_options.setIconSize(QtCore.QSize(50, 50))
            self.button_options.setIcon(QtGui.QIcon(os.path.join(image_path, "options.png")))
            self.button_options.setText("")
            self.button_options.setObjectName("button_options")
            self.button_options.clicked.connect(self.event_optionsdialog)
            self.gridLayout_frame_header_right.addWidget(self.button_options, 1, 7, 1, 1)
            self.gridLayout_frame_header.addWidget(self.frame_header_right, 0, 0, 1, 2)
            self.gridLayout_frame_header.setColumnStretch(0, 1)
            self.gridLayout_centralwidget.addWidget(self.frame_header, 0, 0, 1, 2)
            self.frame_main = QtWidgets.QFrame(self.centralwidget)
            self.frame_main.setStyleSheet("")
            self.frame_main.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_main.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_main.setObjectName("frame_main")
            self.gridLayout_frame_main = QtWidgets.QGridLayout(self.frame_main)
            self.gridLayout_frame_main.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_frame_main.setObjectName("gridLayout_frame_main")
            self.splitter_vertical = QtWidgets.QSplitter(self.frame_main)
            self.splitter_vertical.setOrientation(QtCore.Qt.Horizontal)
            self.splitter_vertical.setObjectName("splitter_vertical")
            self.frame_main_left = QtWidgets.QFrame(self.splitter_vertical)
            self.frame_main_left.setMinimumSize(QtCore.QSize(290, 0))
            self.frame_main_left.setMaximumSize(QtCore.QSize(460, 16777215))
            self.frame_main_left.setStyleSheet("QFrame{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(219, 219, 219);\n"
            "}")
            self.frame_main_left.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_main_left.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_main_left.setObjectName("frame_main_left")
            self.gridLayout_frame_main_left = QtWidgets.QGridLayout(self.frame_main_left)
            self.gridLayout_frame_main_left.setContentsMargins(-1, 0, -1, 0)
            self.gridLayout_frame_main_left.setObjectName("gridLayout_frame_main_left")
            self.splitter_horizontal_left = QtWidgets.QSplitter(self.frame_main_left)
            self.splitter_horizontal_left.setOrientation(QtCore.Qt.Vertical)
            self.splitter_horizontal_left.setObjectName("splitter_horizontal_left")
            self.frame_params = QtWidgets.QFrame(self.splitter_horizontal_left)
            self.frame_params.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_params.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_params.setObjectName("frame_params")
            self.gridLayout_frame_params = QtWidgets.QGridLayout(self.frame_params)
            self.gridLayout_frame_params.setObjectName("gridLayout_frame_params")
            self.label_params = QtWidgets.QLabel(self.frame_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params.setFont(font)
            self.label_params.setScaledContents(True)
            self.label_params.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params.setWordWrap(True)
            self.label_params.setObjectName("label_params")
            self.gridLayout_frame_params.addWidget(self.label_params, 0, 0, 1, 1)
            self.scrollArea_params = QtWidgets.QScrollArea(self.frame_params)
            self.scrollArea_params.setStyleSheet("")
            self.scrollArea_params.setWidgetResizable(True)
            self.scrollArea_params.setObjectName("scrollArea_params")
            self.scrollAreaWidgetContents_params = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_params.setGeometry(QtCore.QRect(0, 0, 424, 572))
            self.scrollAreaWidgetContents_params.setStyleSheet("QWidget{\n"
            "    border-radius: 8px;\n"
            "    background-color: rgb(207, 207, 207);\n"
            "}\n"
            "")
            self.scrollAreaWidgetContents_params.setObjectName("scrollAreaWidgetContents_params")
            self.gridLayout_scrollAreaWidgetContents_params = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_params)
            self.gridLayout_scrollAreaWidgetContents_params.setContentsMargins(9, 9, 9, 9)
            self.gridLayout_scrollAreaWidgetContents_params.setHorizontalSpacing(0)
            self.gridLayout_scrollAreaWidgetContents_params.setVerticalSpacing(3)
            self.gridLayout_scrollAreaWidgetContents_params.setObjectName("gridLayout_scrollAreaWidgetContents_params")
            self.label_params_akcel = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_akcel.setFont(font)
            self.label_params_akcel.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_akcel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_akcel.setWordWrap(True)
            self.label_params_akcel.setObjectName("label_params_akcel")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_akcel, 3, 1, 1, 1)
            self.label_bazal = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_bazal.setFont(font)
            self.label_bazal.setWordWrap(True)
            self.label_bazal.setObjectName("label_bazal")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_bazal, 2, 0, 1, 1)
            self.label_params_fricoscil = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_fricoscil.setFont(font)
            self.label_params_fricoscil.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_fricoscil.setWordWrap(True)
            self.label_params_fricoscil.setObjectName("label_params_fricoscil")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_fricoscil, 6, 1, 1, 1)
            self.label_params_bazal = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_bazal.setFont(font)
            self.label_params_bazal.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_bazal.setWordWrap(True)
            self.label_params_bazal.setObjectName("label_params_bazal")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_bazal, 2, 1, 1, 1)
            self.label_akcel = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_akcel.setFont(font)
            self.label_akcel.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_akcel.setWordWrap(True)
            self.label_akcel.setObjectName("label_akcel")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_akcel, 3, 0, 1, 1)
            self.label_oscil = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_oscil.setFont(font)
            self.label_oscil.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_oscil.setWordWrap(True)
            self.label_oscil.setObjectName("label_oscil")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_oscil, 5, 0, 1, 1)
            self.label_params_oscil = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_oscil.setFont(font)
            self.label_params_oscil.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_oscil.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_oscil.setWordWrap(True)
            self.label_params_oscil.setObjectName("label_params_oscil")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_oscil, 5, 1, 1, 1)
            self.label_pokazatel = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            self.label_pokazatel.setFont(font)
            self.label_pokazatel.setObjectName("label_pokazatel")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_pokazatel, 0, 0, 1, 1)
            self.label_fisher = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_fisher.setFont(font)
            self.label_fisher.setStyleSheet("QLabel{\n"
            "    \n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}\n"
            "")
            self.label_fisher.setWordWrap(True)
            self.label_fisher.setObjectName("label_fisher")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_fisher, 1, 0, 1, 1)
            self.label_params_fisher = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_fisher.setFont(font)
            self.label_params_fisher.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_fisher.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_fisher.setWordWrap(True)
            self.label_params_fisher.setObjectName("label_params_fisher")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_fisher, 1, 1, 1, 1)
            self.label_params_decel = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_decel.setFont(font)
            self.label_params_decel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_decel.setWordWrap(True)
            self.label_params_decel.setObjectName("label_params_decel")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_decel, 4, 1, 1, 1)
            self.label_znachenie = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            self.label_znachenie.setFont(font)
            self.label_znachenie.setAlignment(QtCore.Qt.AlignCenter)
            self.label_znachenie.setWordWrap(True)
            self.label_znachenie.setObjectName("label_znachenie")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_znachenie, 0, 1, 1, 1)
            self.label_FC = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_FC.setFont(font)
            self.label_FC.setWordWrap(True)
            self.label_FC.setObjectName("label_FC")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_FC, 16, 0, 1, 1)
            self.label_fricoscil = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_fricoscil.setFont(font)
            self.label_fricoscil.setWordWrap(True)
            self.label_fricoscil.setObjectName("label_fricoscil")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_fricoscil, 6, 0, 1, 1)
            self.label_STV = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_STV.setFont(font)
            self.label_STV.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_STV.setWordWrap(True)
            self.label_STV.setObjectName("label_STV")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_STV, 7, 0, 1, 1)
            self.label_LTV = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LTV.setFont(font)
            self.label_LTV.setWordWrap(True)
            self.label_LTV.setObjectName("label_LTV")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_LTV, 8, 0, 1, 1)
            self.label_LowEp = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LowEp.setFont(font)
            self.label_LowEp.setWordWrap(True)
            self.label_LowEp.setObjectName("label_LowEp")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_LowEp, 10, 0, 1, 1)
            self.label_LossPercent = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LossPercent.setFont(font)
            self.label_LossPercent.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_LossPercent.setWordWrap(True)
            self.label_LossPercent.setObjectName("label_LossPercent")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_LossPercent, 11, 0, 1, 1)
            self.label_LengthSignal = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LengthSignal.setFont(font)
            self.label_LengthSignal.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_LengthSignal.setWordWrap(True)
            self.label_LengthSignal.setObjectName("label_LengthSignal")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_LengthSignal, 13, 0, 1, 1)
            self.label_LengthRecord = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LengthRecord.setFont(font)
            self.label_LengthRecord.setWordWrap(True)
            self.label_LengthRecord.setObjectName("label_LengthRecord")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_LengthRecord, 12, 0, 1, 1)
            self.label_CHSSMama = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_CHSSMama.setFont(font)
            self.label_CHSSMama.setWordWrap(True)
            self.label_CHSSMama.setObjectName("label_CHSSMama")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_CHSSMama, 14, 0, 1, 1)
            self.label_douz = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_douz.setFont(font)
            self.label_douz.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_douz.setWordWrap(True)
            self.label_douz.setObjectName("label_douz")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_douz, 15, 0, 1, 1)
            self.label_razmahCHSS = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_razmahCHSS.setFont(font)
            self.label_razmahCHSS.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_razmahCHSS.setWordWrap(True)
            self.label_razmahCHSS.setObjectName("label_razmahCHSS")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_razmahCHSS, 17, 0, 1, 1)
            self.label_HighEp = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_HighEp.setFont(font)
            self.label_HighEp.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_HighEp.setWordWrap(True)
            self.label_HighEp.setObjectName("label_HighEp")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_HighEp, 9, 0, 1, 1)
            self.label_decel = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_decel.setFont(font)
            self.label_decel.setWordWrap(True)
            self.label_decel.setObjectName("label_decel")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_decel, 4, 0, 1, 1)
            self.label_params_STV = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_STV.setFont(font)
            self.label_params_STV.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_STV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_STV.setWordWrap(True)
            self.label_params_STV.setObjectName("label_params_STV")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_STV, 7, 1, 1, 1)
            self.label_params_LTV = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LTV.setFont(font)
            self.label_params_LTV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LTV.setWordWrap(True)
            self.label_params_LTV.setObjectName("label_params_LTV")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_LTV, 8, 1, 1, 1)
            self.label_params_HighEp = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_HighEp.setFont(font)
            self.label_params_HighEp.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_HighEp.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_HighEp.setWordWrap(True)
            self.label_params_HighEp.setObjectName("label_params_HighEp")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_HighEp, 9, 1, 1, 1)
            self.label_params_LowEp = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LowEp.setFont(font)
            self.label_params_LowEp.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LowEp.setWordWrap(True)
            self.label_params_LowEp.setObjectName("label_params_LowEp")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_LowEp, 10, 1, 1, 1)
            self.label_params_LossPercent = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LossPercent.setFont(font)
            self.label_params_LossPercent.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_LossPercent.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LossPercent.setWordWrap(True)
            self.label_params_LossPercent.setObjectName("label_params_LossPercent")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_LossPercent, 11, 1, 1, 1)
            self.label_params_LengthRecord = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LengthRecord.setFont(font)
            self.label_params_LengthRecord.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LengthRecord.setWordWrap(True)
            self.label_params_LengthRecord.setObjectName("label_params_LengthRecord")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_LengthRecord, 12, 1, 1, 1)
            self.label_params_LengthSignal = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LengthSignal.setFont(font)
            self.label_params_LengthSignal.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_LengthSignal.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LengthSignal.setWordWrap(True)
            self.label_params_LengthSignal.setObjectName("label_params_LengthSignal")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_LengthSignal, 13, 1, 1, 1)
            self.label_params_CHSSMama = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_CHSSMama.setFont(font)
            self.label_params_CHSSMama.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_CHSSMama.setWordWrap(True)
            self.label_params_CHSSMama.setObjectName("label_params_CHSSMama")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_CHSSMama, 14, 1, 1, 1)
            self.label_params_douz = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_douz.setFont(font)
            self.label_params_douz.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_douz.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_douz.setWordWrap(True)
            self.label_params_douz.setObjectName("label_params_douz")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_douz, 15, 1, 1, 1)
            self.label_params_FC = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_FC.setFont(font)
            self.label_params_FC.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_FC.setWordWrap(True)
            self.label_params_FC.setObjectName("label_params_FC")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_FC, 16, 1, 1, 1)
            self.label_params_razmahCHSS = QtWidgets.QLabel(self.scrollAreaWidgetContents_params)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_razmahCHSS.setFont(font)
            self.label_params_razmahCHSS.setStyleSheet("QLabel{\n"
            "    background-color: rgb(219, 219, 219);\n"
            "    border-radius:0px;\n"
            "}")
            self.label_params_razmahCHSS.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_razmahCHSS.setWordWrap(True)
            self.label_params_razmahCHSS.setObjectName("label_params_razmahCHSS")
            self.gridLayout_scrollAreaWidgetContents_params.addWidget(self.label_params_razmahCHSS, 17, 1, 1, 1)
            self.gridLayout_scrollAreaWidgetContents_params.setColumnStretch(0, 1)
            self.gridLayout_scrollAreaWidgetContents_params.setColumnStretch(1, 1)
            self.scrollArea_params.setWidget(self.scrollAreaWidgetContents_params)
            self.gridLayout_frame_params.addWidget(self.scrollArea_params, 1, 0, 1, 1)
            self.frame_additional = QtWidgets.QFrame(self.splitter_horizontal_left)
            self.frame_additional.setMinimumSize(QtCore.QSize(0, 170))
            self.frame_additional.setMaximumSize(QtCore.QSize(16777215, 170))
            self.frame_additional.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_additional.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_additional.setObjectName("frame_additional")
            self.gridLayout_frame_additional = QtWidgets.QGridLayout(self.frame_additional)
            self.gridLayout_frame_additional.setObjectName("gridLayout_frame_additional")
            self.scrollArea_additional = QtWidgets.QScrollArea(self.frame_additional)
            self.scrollArea_additional.setStyleSheet("")
            self.scrollArea_additional.setWidgetResizable(True)
            self.scrollArea_additional.setObjectName("scrollArea_additional")
            self.scrollAreaWidgetContents_additional = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_additional.setGeometry(QtCore.QRect(0, 0, 424, 128))
            self.scrollAreaWidgetContents_additional.setStyleSheet("QWidget{\n"
            "    border-radius: 8px;\n"
            "    background-color: rgb(207, 207, 207);\n"
            "}\n"
            "")
            self.scrollAreaWidgetContents_additional.setObjectName("scrollAreaWidgetContents_additional")
            self.gridLayout_scrollAreaWidgetContents_additional = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_additional)
            self.gridLayout_scrollAreaWidgetContents_additional.setObjectName("gridLayout_scrollAreaWidgetContents_additional")
            self.frame_start = QtWidgets.QFrame(self.scrollAreaWidgetContents_additional)
            self.frame_start.setMinimumSize(QtCore.QSize(0, 70))
            self.frame_start.setMaximumSize(QtCore.QSize(16777215, 70))
            self.frame_start.setStyleSheet("QFrame{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(219, 219, 219);\n"
            "}")
            self.frame_start.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_start.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_start.setObjectName("frame_start")
            self.gridLayout_frame_start = QtWidgets.QGridLayout(self.frame_start)
            self.gridLayout_frame_start.setObjectName("gridLayout_frame_start")
            self.label_start_min = QtWidgets.QLabel(self.frame_start)
            self.label_start_min.setMinimumSize(QtCore.QSize(12, 0))
            self.label_start_min.setMaximumSize(QtCore.QSize(12, 16777215))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_start_min.setFont(font)
            self.label_start_min.setObjectName("label_start_min")
            self.gridLayout_frame_start.addWidget(self.label_start_min, 4, 1, 1, 1)
            self.spinBox_start_min = QtWidgets.QSpinBox(self.frame_start)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.spinBox_start_min.setFont(font)
            self.spinBox_start_min.setAlignment(QtCore.Qt.AlignCenter)
            self.spinBox_start_min.setObjectName("spinBox_start_min")
            self.spinBox_start_min.valueChanged.connect(lambda: self.event_spinbox(self.spinBox_start_min.value(),"start_min"))
            self.gridLayout_frame_start.addWidget(self.spinBox_start_min, 4, 0, 1, 1)
            self.doubleSpinBox_start_sec = QtWidgets.QDoubleSpinBox(self.frame_start)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.doubleSpinBox_start_sec.setFont(font)
            self.doubleSpinBox_start_sec.setAlignment(QtCore.Qt.AlignCenter)
            self.doubleSpinBox_start_sec.setDecimals(3)
            self.doubleSpinBox_start_sec.setMaximum(59.999)
            self.doubleSpinBox_start_sec.setSingleStep(1.0)
            self.doubleSpinBox_start_sec.setObjectName("doubleSpinBox_start_sec")
            self.doubleSpinBox_start_sec.valueChanged.connect(lambda: self.event_spinbox(self.doubleSpinBox_start_sec.value(),"start_sec"))
            self.gridLayout_frame_start.addWidget(self.doubleSpinBox_start_sec, 4, 2, 1, 1)
            self.label_start_sec = QtWidgets.QLabel(self.frame_start)
            self.label_start_sec.setMinimumSize(QtCore.QSize(12, 0))
            self.label_start_sec.setMaximumSize(QtCore.QSize(12, 16777215))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_start_sec.setFont(font)
            self.label_start_sec.setObjectName("label_start_sec")
            self.gridLayout_frame_start.addWidget(self.label_start_sec, 4, 3, 1, 1)
            self.label_start = QtWidgets.QLabel(self.frame_start)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_start.setFont(font)
            self.label_start.setAlignment(QtCore.Qt.AlignCenter)
            self.label_start.setObjectName("label_start")
            self.gridLayout_frame_start.addWidget(self.label_start, 1, 0, 1, 4)
            self.gridLayout_frame_start.setRowMinimumHeight(0, 3)
            self.gridLayout_frame_start.setRowMinimumHeight(1, 1)
            self.gridLayout_frame_start.setRowMinimumHeight(2, 3)
            self.gridLayout_frame_start.setRowMinimumHeight(3, 1)
            self.gridLayout_scrollAreaWidgetContents_additional.addWidget(self.frame_start, 1, 0, 1, 1)
            self.frame_end = QtWidgets.QFrame(self.scrollAreaWidgetContents_additional)
            self.frame_end.setMinimumSize(QtCore.QSize(0, 70))
            self.frame_end.setMaximumSize(QtCore.QSize(16777215, 70))
            self.frame_end.setStyleSheet("QFrame{\n"
            "    border-radius:8px;\n"
            "    \n"
            "    background-color: rgb(219, 219, 219);\n"
            "}")
            self.frame_end.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_end.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_end.setObjectName("frame_end")
            self.gridLayout_frame_end = QtWidgets.QGridLayout(self.frame_end)
            self.gridLayout_frame_end.setObjectName("gridLayout_frame_end")
            self.spinBox_end_min = QtWidgets.QSpinBox(self.frame_end)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.spinBox_end_min.setFont(font)
            self.spinBox_end_min.setAlignment(QtCore.Qt.AlignCenter)
            self.spinBox_end_min.setObjectName("spinBox_end_min")
            self.spinBox_end_min.valueChanged.connect(lambda: self.event_spinbox(self.spinBox_end_min.value(),"end_min"))
            self.gridLayout_frame_end.addWidget(self.spinBox_end_min, 3, 0, 1, 1)
            self.label_endmin = QtWidgets.QLabel(self.frame_end)
            self.label_endmin.setMinimumSize(QtCore.QSize(12, 0))
            self.label_endmin.setMaximumSize(QtCore.QSize(12, 16777215))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_endmin.setFont(font)
            self.label_endmin.setObjectName("label_endmin")
            self.gridLayout_frame_end.addWidget(self.label_endmin, 3, 1, 1, 1)
            self.doubleSpinBox_end_sec = QtWidgets.QDoubleSpinBox(self.frame_end)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.doubleSpinBox_end_sec.setFont(font)
            self.doubleSpinBox_end_sec.setAlignment(QtCore.Qt.AlignCenter)
            self.doubleSpinBox_end_sec.setDecimals(3)
            self.doubleSpinBox_end_sec.setMaximum(59.999)
            self.doubleSpinBox_end_sec.setObjectName("doubleSpinBox_end_sec")
            self.doubleSpinBox_end_sec.valueChanged.connect(lambda: self.event_spinbox(self.doubleSpinBox_end_sec.value(),"end_sec"))
            self.gridLayout_frame_end.addWidget(self.doubleSpinBox_end_sec, 3, 2, 1, 1)
            self.label_endsec = QtWidgets.QLabel(self.frame_end)
            self.label_endsec.setMinimumSize(QtCore.QSize(12, 0))
            self.label_endsec.setMaximumSize(QtCore.QSize(12, 16777215))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_endsec.setFont(font)
            self.label_endsec.setObjectName("label_endsec")
            self.gridLayout_frame_end.addWidget(self.label_endsec, 3, 3, 1, 1)
            self.label_end = QtWidgets.QLabel(self.frame_end)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_end.setFont(font)
            self.label_end.setAlignment(QtCore.Qt.AlignCenter)
            self.label_end.setObjectName("label_end")
            self.gridLayout_frame_end.addWidget(self.label_end, 0, 0, 1, 4)
            self.gridLayout_scrollAreaWidgetContents_additional.addWidget(self.frame_end, 1, 1, 1, 1)
            self.pushButton_additional_reset = QtWidgets.QPushButton(self.scrollAreaWidgetContents_additional)
            self.pushButton_additional_reset.setMinimumSize(QtCore.QSize(0, 30))
            self.pushButton_additional_reset.setMaximumSize(QtCore.QSize(16777215, 30))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.pushButton_additional_reset.setFont(font)
            self.pushButton_additional_reset.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(105, 175, 99);\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_green_color};\n"
            "}")
            self.pushButton_additional_reset.clicked.connect(self.event_reset_selection)
            self.pushButton_additional_reset.setObjectName("pushButton_additional_reset")
            self.gridLayout_scrollAreaWidgetContents_additional.addWidget(self.pushButton_additional_reset, 2, 0, 1, 2)
            self.scrollArea_additional.setWidget(self.scrollAreaWidgetContents_additional)
            self.gridLayout_frame_additional.addWidget(self.scrollArea_additional, 1, 0, 1, 1)
            self.label_additional = QtWidgets.QLabel(self.frame_additional)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_additional.setFont(font)
            self.label_additional.setScaledContents(True)
            self.label_additional.setAlignment(QtCore.Qt.AlignCenter)
            self.label_additional.setWordWrap(True)
            self.label_additional.setObjectName("label_additional")
            self.gridLayout_frame_additional.addWidget(self.label_additional, 0, 0, 1, 1)
            self.gridLayout_frame_main_left.addWidget(self.splitter_horizontal_left, 0, 1, 1, 1)
            self.splitter_horizontal_right = QtWidgets.QSplitter(self.splitter_vertical)
            self.splitter_horizontal_right.setOrientation(QtCore.Qt.Vertical)
            self.splitter_horizontal_right.setObjectName("splitter_horizontal_right")
            CVB=CustomViewBox()
            scatter = pg.ScatterPlotItem(pen=pg.mkPen(width=5, color=fg_green_color), symbol='s', size=2, hoverable=True)
            scatter.setData(tip= 'Амплитуда: {data[0]} уд/мин\nДлительность: {data[1]} сек'.format)
            Plot1=PlotWidget(self.splitter_horizontal_right, viewBox=CVB)
            self.graphicsView_Graph = Plot1
            self.graphicsView_Graph.setObjectName("graphicsView_Graph")
            Plot2=PlotWidget(self.splitter_horizontal_right)
            self.graphicsView_STVLTV = Plot2
            self.graphicsView_STVLTV.setMinimumSize(QtCore.QSize(0, 135))
            self.graphicsView_STVLTV.setMaximumSize(QtCore.QSize(16777215, 135))
            self.graphicsView_STVLTV.setObjectName("graphicsView_STVLTV")
            self.gridLayout_frame_main.addWidget(self.splitter_vertical, 0, 0, 1, 1)
            self.gridLayout_centralwidget.addWidget(self.frame_main, 1, 0, 1, 2)
            self.gridLayout_centralwidget.setColumnStretch(0, 1)
            self.gridLayout_centralwidget.setColumnStretch(1, 1)
            self.gridLayout_centralwidget.setRowStretch(0, 1)
            self.gridLayout_centralwidget.setRowStretch(1, 1000)
            MainWindow.setCentralWidget(self.centralwidget)
            self.fillgraph()
            self.splitter_horizontal_left.setStretchFactor(12, 1)
            self.splitter_horizontal_left.setSizes([1200,100])
            self.splitter_vertical.setStretchFactor(2, 1)
            self.splitter_vertical.setSizes([100,200])
            self.splitter_horizontal_right.setStretchFactor(10, 3)
            self.splitter_horizontal_right.setSizes([1000,300])
            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
            self.graphicsView_Graph.setXRange(-2, 43,padding=0)
        
        def mouseMoved(self,evt): #Захват мыши, отрисовка показаний в зависимости от положения курсора
            pos = evt
            if self.graphicsView_Graph.sceneBoundingRect().contains(pos):
                mousePoint = CVB.mapSceneToView(pos)
                if mousePoint.x() > 0 and mousePoint.x()*60 < data["xFetusHeartRateGraphic"][-1]:
                    
                    try:
                        x=data["xFetusHeartRateGraphic"].index(round(mousePoint.x()*60))
                    except:
                        self.Xcoord=copy.deepcopy(data["xFetusHeartRateGraphic"])
                        self.Xcoord.append(round(mousePoint.x()*60))
                        self.Xcoord.sort()
                        Xindex=self.Xcoord.index(round(mousePoint.x()*60))
                        if data["isBreakFetusHeartRateGraphic"][Xindex]==1:
                            newY=(data["yFetusHeartRateGraphic"][Xindex-1]+data["yFetusHeartRateGraphic"][Xindex+1])/2
                            x=-1
                        else: x=-2 
                    self.mouseXInfo.setPos(mousePoint.x(), mousePoint.y())
                    if x!=-1 and x!=-2:
                        self.mouseXInfo.setText(str(data["yFetusHeartRateGraphic"][x])+" уд/мин\n"+str(round(mousePoint.x(),1))+" мин")
                    elif x==-1:
                        self.mouseXInfo.setText(str(round(newY,2))+" уд/мин\n"+str(round(mousePoint.x(),1))+" мин")
                    elif x==-2:
                        self.mouseXInfo.setText("0 уд/мин\n"+str(round(mousePoint.x(),1))+" мин")
        
        def event_optionsdialog(self): #Диалог настроек
            global Dialog
            try:
                Dialog.close()
                Dialog=QtWidgets.QDialog()
            except:
                Dialog=QtWidgets.QDialog()
            ui=Ui_DialogGraphicOptions()
            ui.setupUi(Dialog)
            Dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
            Dialog.show()
            Dialog.exec_()
        
        def event_spinbox(self, result,type): #Логика спинбоксов, чтобы изменялся размер выделения в зависисмости от значений спинбокса
            
            global allocationGraph,allocationSTVLTV, firsttime

            if allocationGraph!=0:
                OldRectGraph=allocationGraph._rect.getRect()
                OldRectSTVLTV=allocationSTVLTV._rect.getRect()
                self.graphicsView_Graph.removeItem(allocationGraph)
                self.graphicsView_STVLTV.removeItem(allocationSTVLTV)
                if (self.spinBox_start_min.value()<self.spinBox_end_min.value())or((self.spinBox_start_min.value()==self.spinBox_end_min.value())and(self.doubleSpinBox_start_sec.value()<self.doubleSpinBox_end_sec.value())):
                    if type=="start_min" and result!=int(OldRectGraph[0]//1):
                            rect_item = RectItem(QtCore.QRectF(result+OldRectGraph[0]%1,OldRectGraph[1],OldRectGraph[2]+(OldRectGraph[0]//1-result),OldRectGraph[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationGraph=rect_item
                            rect_item = RectItem(QtCore.QRectF(result+OldRectGraph[0]%1,OldRectGraph[1],OldRectGraph[2]+(OldRectGraph[0]//1-result),OldRectGraph[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationSTVLTV=rect_item
                    elif type=="start_sec":
                            rect_item = RectItem(QtCore.QRectF(OldRectGraph[0]//1+result/60,OldRectGraph[1],OldRectGraph[2]+(OldRectGraph[0]%1-result/60),OldRectGraph[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationGraph=rect_item
                            rect_item = RectItem(QtCore.QRectF(OldRectSTVLTV[0]//1+result/60,OldRectSTVLTV[1],OldRectSTVLTV[2]+(OldRectGraph[0]%1-result/60),OldRectSTVLTV[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationSTVLTV=rect_item         
                    elif type=="end_min":
                            rect_item = RectItem(QtCore.QRectF(OldRectGraph[0],OldRectGraph[1],result+(OldRectGraph[2]+OldRectGraph[0])%1-OldRectGraph[0],OldRectGraph[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationGraph=rect_item
                            rect_item = RectItem(QtCore.QRectF(OldRectSTVLTV[0],OldRectSTVLTV[1],result+(OldRectSTVLTV[2]+OldRectSTVLTV[0])%1-OldRectSTVLTV[0],OldRectSTVLTV[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationSTVLTV=rect_item
                    elif type=="end_sec":
                            rect_item = RectItem(QtCore.QRectF(OldRectGraph[0],OldRectGraph[1],OldRectGraph[2]+(result/60-(OldRectGraph[2]+OldRectGraph[0])%1),OldRectGraph[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationGraph=rect_item
                            rect_item = RectItem(QtCore.QRectF(OldRectSTVLTV[0],OldRectSTVLTV[1],OldRectGraph[2]+(result/60-(OldRectGraph[2]+OldRectGraph[0])%1),OldRectSTVLTV[3]),"#0078d7","#0078d7", line_width=0)
                            rect_item.setOpacity(0.3)
                            allocationSTVLTV=rect_item
                            if firsttime==0:
                                firsttime=1
                self.graphicsView_Graph.addItem(allocationGraph)
                self.graphicsView_STVLTV.addItem(allocationSTVLTV)
                if firsttime==1:
                    self.selection_params()
        
        def event_ruler(self): #Линейка
            
            global ruler, ruleritem
            
            if ruler==0:
                ruler=1
                self.button_ruler.setStyleSheet("QPushButton{\n"
                "    border-radius:8px;\n"
                f"    background-color: {hover_grey_color};\n"
                "}"
                "QPushButton:hover{\n"
                "    border-radius:8px;\n"
                f"    background-color: {hover_grey_color};\n"
                "}")
                x1=CVB.viewRange()[0][0]+(CVB.viewRange()[0][1]-CVB.viewRange()[0][0])/3
                x2=(CVB.viewRange()[0][1]-CVB.viewRange()[0][0])/3
                y1=CVB.viewRange()[1][0]+(CVB.viewRange()[1][1]-CVB.viewRange()[1][0])/3
                y2=(CVB.viewRange()[1][1]-CVB.viewRange()[1][0])/3
                ruleritem= pg.ROI([x1,y1], [x2,y2], pen="g")
                r3a=ruleritem 
                CVB.addItem(r3a)
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setBold(True)
                font.setPointSize(10)
                
                ## handles scaling horizontally around center
                r3a.addScaleHandle([1, 0.5], [0, 0.5])
                r3a.addScaleHandle([0, 0.5], [1, 0.5])

                ## handles scaling vertically from opposite edge
                r3a.addScaleHandle([0.5, 0], [0.5, 1])
                r3a.addScaleHandle([0.5, 1], [0.5, 0])

                ## handles scaling both vertically and horizontally
                r3a.addScaleHandle([1, 1], [0, 0])
                r3a.addScaleHandle([0, 0], [1, 1])
                
                high=pg.TextItem(text=str(round(r3a.size()[1],3))+" уд/мин",color=fg_yellow_color,anchor=(0,0))
                high.setFont(font)
                high.setParentItem(r3a)
                width=pg.TextItem(text=str(round(r3a.size()[0]//1))+" мин " + str(round(r3a.size()[0]%1*60))+" сек",color=fg_yellow_color,anchor=(0,-1))
                width.setParentItem(r3a)
                width.setFont(font)
                width.setPos(0,2)
                def regionupdated(item):
                    high.setText(str(round(item.size()[1],3))+" уд/мин")
                    width.setText(str(round(r3a.size()[0]//1))+" мин " + str(round(r3a.size()[0]%1*60))+" сек")
                r3a.sigRegionChanged.connect(regionupdated)
            else:
                ruler=0
                self.button_ruler.setStyleSheet("QPushButton{\n"
                "    border-radius:8px;\n"
                f"    background-color: {fg_grey_color};\n"
                "}"
                "QPushButton:hover{\n"
                "    border-radius:8px;\n"
                f"    background-color: {hover_grey_color};\n"
                "}")
                CVB.removeItem(ruleritem)
                ruleritem=0
                
        def metkiacc(self): #Отрисовка меток акцелераций
            global scatter
            spot=[]
            xInMinutesAccel=[]
            for second in data["indexXFetusAccelerationsGraphic"]:
                 xInMinutesAccel.append(data["xFetusHeartRateGraphic"][second]/60)
                 
            for i in range(len(xInMinutesAccel)):
                spot.append({'pos': [xInMinutesAccel[i],data["yAccelerationsGraphic"][i]+4], 'data': [data["ampAccelerationsGraphic"][i],data["lenAccelerationsGraphic"][i]]})
            scatter.addPoints(spot)
        
        def metkidec(self): #Отрисовка меток децелераций
            global scatter
            spot=[]
            xInMinutesDecel=[]
            for second in data["indexXFetusDecelerationsGraphic"]:
                 xInMinutesDecel.append(data["xFetusHeartRateGraphic"][second]/60)
            for i in range(len(xInMinutesDecel)):
                spot.append({'pos': [xInMinutesDecel[i],data["yDecelerationsGraphic"][i]-4], 'data': [data["ampDecelerationsGraphic"][i],data["lenDecelerationsGraphic"][i]]})
            scatter.addPoints(spot)
       
        def new_params(self):#Перерасчет параметров после выделения
            
            #----------------------- Базальный и Размах, Базальный матери
            roundeddata=[]
            roundeddataMama=[]
            gistogramm=[]
            gistogrammMama=[]
            RectGraph=allocationGraph._rect.getRect()
            
            try:
                x1=data["xFetusHeartRateGraphic"].index(round(RectGraph[0]*60))
            except ValueError:
                templist=copy.deepcopy(data["xFetusHeartRateGraphic"])
                templist.append(round(RectGraph[0]*60))
                templist.sort()
                x1=templist.index(round(RectGraph[0]*60))+1
            try:
                x2=data["xFetusHeartRateGraphic"].index(round((RectGraph[0]+RectGraph[2])*60))
            except ValueError:
                templist=copy.deepcopy(data["xFetusHeartRateGraphic"])
                templist.append(round((RectGraph[0]+RectGraph[2])*60))
                templist.sort()
                x2=templist.index(round((RectGraph[0]+RectGraph[2])*60))-1

            if x2>data["xFetusHeartRateGraphic"][-1]: x2=data["xFetusHeartRateGraphic"].index(data["xFetusHeartRateGraphic"][-1])
            
            for i in range(50,180,3):
                gistogramm.append([i,0])
                gistogrammMama.append([i,0])
                
            for i in range(x1,x2,1):
                number=round(data["yFetusBasalRateGraphic"][i])
                roundeddata.append(number)  
                  
            if len(data["xMomeHeartRateGraphic"])!=0:
                
                try:
                    x1Mom=data["xMomeHeartRateGraphic"].index(round(RectGraph[0]*60))
                except ValueError:
                    templist=copy.deepcopy(data["xMomeHeartRateGraphic"])
                    templist.append(round(RectGraph[0]*60))
                    templist.sort()
                    x1Mom=templist.index(round(RectGraph[0]*60))+1
                try:
                    x2Mom=data["xMomeHeartRateGraphic"].index(round((RectGraph[0]+RectGraph[2])*60))
                except ValueError:
                    templist=copy.deepcopy(data["xMomeHeartRateGraphic"])
                    templist.append(round((RectGraph[0]+RectGraph[2])*60))
                    templist.sort()
                    x2Mom=templist.index(round((RectGraph[0]+RectGraph[2])*60))-1
                
                if x2Mom>data["xMomeHeartRateGraphic"][-1]: x2Mom=data["xMomeHeartRateGraphic"].index(data["xMomeHeartRateGraphic"][-1])
                
                for i in range(x1Mom,x2Mom,1):
                    number=round(data["yMomBasalRateGraphic"][i])
                    roundeddataMama.append(number)
                
                countedMama=Counter(roundeddataMama)
                
                for key, value in countedMama.items():
                    if (key-50%3)==0:
                        gistogrammMama[(key-50)//3][1]+=value
                    elif ((number-49)%3)==0:
                        gistogrammMama[(key-49)//3][1]+=value
                    else:
                        gistogrammMama[(key-51)//3][1]+=value
                
            counted=Counter(roundeddata)
                
            for key, value in counted.items():
                if (key-50%3)==0:
                    gistogramm[(key-50)//3][1]+=value
                elif ((number-49)%3)==0:
                    gistogramm[(key-49)//3][1]+=value
                else:
                    gistogramm[(key-51)//3][1]+=value
                    
            if len(roundeddata)==0:
                maximum = 0
                minimum = 0
                iMax=-1
                countAccel=0
                countDecel=0
                countDecel30=0
                iMaxMama=-1
            else: 
                maximum = max(roundeddata)
                minimum = min(roundeddata)
                
                localmax=0
                iMax=0
                localmaxMama=0
                iMaxMama=0
                
                for i in (gistogramm):
                    if i[1]>localmax:
                        localmax=i[1]
                        iMax=i[0]
                        
                if len(data["xMomeHeartRateGraphic"])!=0:
                    for i in (gistogrammMama):
                        if i[1]>localmaxMama:
                            localmaxMama=i[1]
                            iMaxMama=i[0]
                            
                if iMax!=0:
                    iMax+=1
                if iMaxMama!=0:
                    iMaxMama+=1
                #----------------------- Количество акцелераций и децелераций (>30c), амплитуда и частота осциляций
                
                countAccel=0
                countDecel=0
                countDecel30=0
                
                
                
                for x in (data["indexXFetusAccelerationsGraphic"]): #количество акцелераций в диапазоне
                    if data["xFetusHeartRateGraphic"][x]>=data["xFetusHeartRateGraphic"][x1] and data["xFetusHeartRateGraphic"][x]<=data["xFetusHeartRateGraphic"][x2]:
                        countAccel+=1
                
                DecelDouzMark=0
                
                step=0     
                for x in (data["indexXFetusDecelerationsGraphic"]): #количество децелераций в диапазоне
                    if data["xFetusHeartRateGraphic"][x]>=data["xFetusHeartRateGraphic"][x1] and data["xFetusHeartRateGraphic"][x]<=data["xFetusHeartRateGraphic"][x2]:
                        countDecel+=1
                        if data["lenDecelerationsGraphic"][step]>=30 and data["ampDecelerationsGraphic"][step]>=25:
                            DecelDouzMark=1
                        if data["lenDecelerationsGraphic"][step]>=30:
                            countDecel30+=1
                    step+=1
                    
                oscAmplitude=0
                oscFrequency=0
                
                count=0
                for x in (data["xOscillationPivotTable"]): #количество осциляций в диапазоне, средняя аплитуда и частота
                    if data["xFetusHeartRateGraphic"][x]>=data["xFetusHeartRateGraphic"][x1] and data["xFetusHeartRateGraphic"][x]<=data["xFetusHeartRateGraphic"][x2]:
                        oscAmplitude+=data["MedianOscillationAmplitudePivotTable"][data["xOscillationPivotTable"].index(x)]
                        oscFrequency+=data["OscillationFrequencyPivotTable"][data["xOscillationPivotTable"].index(x)]
                    count+=1
                oscAmplitude=oscAmplitude/count
                oscFrequency=oscFrequency/count
                #----------------------- Высокие и низкие эпизоды, STV и LTV----
                
                    
                def findindex():
                    
                    global isHigh,isLow, STVLTVinminutes
                    
                    
                    X1=RectGraph[0]
                    X2=RectGraph[0]+RectGraph[2]
                    ListCopy=copy.deepcopy(STVLTVinminutes)
                    if X1 in ListCopy:
                        ListCopy.append(X1+0.00000000001)
                        ListCopy.sort()
                        x1=ListCopy.index(X1+0.00000000001)
                    else:  
                        ListCopy.append(X1)
                        ListCopy.sort()
                        x1=ListCopy.index(X1)
                    
                    if X2 in ListCopy:
                        ListCopy.append(X2+0.00000000001)
                        ListCopy.sort()
                        x2=ListCopy.index(X2+0.00000000001)
                    else:  
                        ListCopy.append(X2)
                        ListCopy.sort()
                        x2=ListCopy.index(X2)
                    
                    part1=0
                    startindex=0
                    part2=0
                    endindex=0
                    startres=["Nothing",0]
                    endres=["Nothing",0]
                    
                    if x1!=0 and x1<len(ListCopy):
                        if ListCopy[x1]-ListCopy[x1-1]<1.066:
                            if isHigh[x1-1]==1:
                                part1=(1-(ListCopy[x1]-ListCopy[x1-1])/1.0666666666666667)
                                startindex=x1-1
                                startres=["High",data["LTVPivotTable"][startindex]*part1]
                            elif isLow[x1-1]==1:
                                part1=(1-(ListCopy[x1]-ListCopy[x1-1])/1.0666666666666667)
                                startindex=x1-1
                                startres=["Low",data["LTVPivotTable"][startindex]*part1]
                            else:
                                part1=(1-(ListCopy[x1]-ListCopy[x1-1])/1.0666666666666667)
                                startindex=x1-1
                                startres=["Nothing",data["LTVPivotTable"][startindex]*part1]
                        else:
                            if isHigh[x1]==1:
                                part1=1
                                startindex=x1
                                startres=["High",data["LTVPivotTable"][startindex]*part1]
                            elif isLow[x1]==1:
                                part1=1
                                startindex=x1
                                startres=["Low",data["LTVPivotTable"][startindex]*part1]
                            else:
                                part1=1
                                startindex=x1
                                startres=["Nothing",data["LTVPivotTable"][startindex]*part1]
                    
                    if x2!=0 and x2<=len(ListCopy):
                        if ListCopy[x2-1]!=ListCopy[x1]:
                            a=ListCopy[x2-1]
                        else:
                            a=ListCopy[x2-2]
                        if ListCopy[x2]-a<1.066:
                            if isHigh[x2-2]==1:
                                part2=(ListCopy[x2]-a)/1.0666666666666667
                                endindex=x2-2
                                endres=["High",data["LTVPivotTable"][endindex]*part2]
                            elif isLow[x2-2]==1:
                                part2=(ListCopy[x2]-a)/1.0666666666666667
                                endindex=x2-2
                                endres=["Low",data["LTVPivotTable"][endindex]*part2]
                            else:
                                part2=(ListCopy[x2]-a)/1.0666666666666667
                                endindex=x2-2
                                endres=["Nothing",data["LTVPivotTable"][endindex]*part2]
                        else:
                            if isHigh[x2-2]==1:
                                part2=1
                                endindex=x2-2
                                endres=["High",data["LTVPivotTable"][endindex]*part2]
                            elif isLow[x2-2]==1:
                                part2=1
                                endindex=x2-2
                                endres=["Low",data["LTVPivotTable"][endindex]*part2]
                            else:
                                part2=1
                                endindex=x2-2
                                endres=["Nothing",data["LTVPivotTable"][endindex]*part2]   
                    STV=[0,0]
                    LTV=[0,0]
                    STVMEDIAN=[]
                    
                    if startindex < endindex:
                        
                        if part1>=0.5:
                            STV[0]+=data["STVPivotTable"][startindex]
                            STVMEDIAN.append(data["STVPivotTable"][startindex])
                            STV[1]+=1 
                            LTV[0]+=startres[1]
                            LTV[1]+=part1
                        if part2>=0.5:
                            STV[0]+=data["STVPivotTable"][endindex]
                            STVMEDIAN.append(data["STVPivotTable"][endindex])
                            STV[1]+=1
                            LTV[0]+=endres[1]
                            LTV[1]+=part2
                        HighNums=[0,0]
                        LowNums=[0,0]
                        
                        if startres[0]=="High":
                            HighNums[0]+=startres[1]
                            HighNums[1]+=part1
                        elif startres[0]=="Low":
                            LowNums[0]+=startres[1]
                            LowNums[1]+=part1
                        
                        if endres[0]=="High":
                            HighNums[0]+=endres[1]
                            HighNums[1]+=part2
                        elif endres[0]=="Low":
                            LowNums[0]+=endres[1]
                            LowNums[1]+=part2

                        for i in range (startindex+1,endindex):
                            if isHigh[i]==1:
                                HighNums[0]+=data["LTVPivotTable"][i]
                                HighNums[1]+=1
                            elif isLow[i]==1:
                                LowNums[0]+=data["LTVPivotTable"][i]
                                LowNums[1]+=1
                            STV[0]+=data["STVPivotTable"][i]
                            STV[1]+=1
                            LTV[0]+=data["LTVPivotTable"][i]
                            LTV[1]+=1
                            STVMEDIAN.append(data["STVPivotTable"][i])
                                
                        if HighNums[1]!=0:
                            HighRes=[HighNums[0]/HighNums[1],HighNums[1]]
                        else: HighRes=[0,0]
                        
                        if LowNums[1]!=0:
                            LowRes=[LowNums[0]/LowNums[1],LowNums[1]]
                        else: LowRes=[0,0]
                        
                        STVMEDIAN.sort()
                        
                        if (endindex-startindex+1)%2==0 and (endindex-startindex+1>=5):
                            z1=(len(STVMEDIAN)//2)-1
                            z2=z1+1
                            STV[0]=(STVMEDIAN[z1]+STVMEDIAN[z2])/2
                            STV[1]=1
                        elif (endindex-startindex+1)%2!=0 and (endindex-startindex+1>=5):
                            z1=(len(STVMEDIAN)//2)
                            STV[0]=STVMEDIAN[z1]
                            STV[1]=1  
                    
                    elif startindex==endindex:
                        
                        STV[0]+=data["STVPivotTable"][startindex]
                        STV[1]+=1
                        LTV[0]+=data["LTVPivotTable"][startindex]
                        LTV[1]+=1
                        
                        HighNums=[0,0]
                        LowNums=[0,0]
                        if startres[0]=="High":
                            HighNums[0]=startres[1]
                            HighNums[1]+=part1
                        elif startres[0]=="Low":
                            LowNums[0]=startres[1]
                            LowNums[1]+=part1
                        
                        if endres[0]=="High":
                            HighNums[1]-=(1-part2)
                        elif endres[0]=="Low":
                            LowNums[1]-=(1-part2)
                        HighRes=[HighNums[0],HighNums[1]]
                        LowRes=[LowNums[0],LowNums[1]]
                        
                    else:
                        HighRes=[0,0]
                        LowRes=[0,0]
                    
                    if STV[1]!=0:
                        STV=STV[0]/STV[1]
                    else:
                        STV=0
                    if LTV[1]!=0:
                        LTV=LTV[0]/LTV[1]
                    else:
                        LTV=0
                    return(HighRes,LowRes,STV,LTV)
                
                HighRes,LowRes,STV,LTV=findindex()
                #---------------------------------Длительность сигнала
                SignalMinLength=0
                part1=0
                part2=0
                mainpart=0
                
                step1=data["xFetusHeartRateGraphic"][x1]//60
                step2=data["xFetusHeartRateGraphic"][x2]//60
                minute=step1+1
                
                for i in range(x1,x2-1):
                    if data["xFetusHeartRateGraphic"][i]//60==step1:
                        if data["xFetusHeartRateGraphic"][i+1]-data["xFetusHeartRateGraphic"][i]==1:
                            part1+=1
                        else:
                            part1+=1
                    if data["xFetusHeartRateGraphic"][i]//60==step2:
                        if data["xFetusHeartRateGraphic"][i+1]-data["xFetusHeartRateGraphic"][i]==1:
                            part2+=1
                        else:
                            part2+=1
                    if minute<data["xFetusHeartRateGraphic"][i]//60:
                        mainpart+=signalmap[minute][1]
                        minute=data["xFetusHeartRateGraphic"][i]//60
                if data["xFetusHeartRateGraphic"][x1]//60==data["xFetusHeartRateGraphic"][x2]//60:
                    part2=0
                SignalMinLength=round((part1+part2+mainpart)/60,1)  
                #----------------------------------Потеря сигнала---
                recordlength=allocationGraph._rect.getRect()[2]
                signalpercentLoss=round((1-(SignalMinLength/recordlength))*100,1)
                #--------------------Критерий Доуза-Рендальфа ------
                DRC=True
                if SignalMinLength>12:
                    reason="Причины не соблюдения критерия:"
                    if STV<3:
                        DRC=False
                        reason+="\n• Показатель STV <3 мс"
                    if iMax<115 or iMax>160:
                        DRC=False
                        reason+="\n• Базальный ритм <115 или >160 уд/мин "+str(iMax)+"\n"
                    if HighRes[1] < 5:
                        DRC=False
                        reason+="\n• На интервале <5 мин высоких эпизодов"
                    if countAccel<3:
                        DRC=False
                        reason+="\n• На интервале <3 акцелераций"
                    if DecelDouzMark==1:
                        DRC=False
                        reason+="\n• Есть децелерация >=25 уд/мин и >=30 с"
                    if DRC==True:
                        DRCresult="Соблюдены"
                        self.label_params_douz.setToolTip(None) 
                    else:
                        DRCresult="Не соблюдены 🛈"
                        self.label_params_douz.setToolTip(reason)      
                else:
                    DRCresult="Сигнал <12 мин"
                    self.label_params_douz.setToolTip(None) 
                  
                #---------------------------------------------------
            
            result=[str(iMax),str(minimum),str(maximum),str(countAccel),str(countDecel), str(countDecel30), HighRes,LowRes,str(round(STV,1)),str(round(LTV,1)),str(round(oscAmplitude)),str(round(oscFrequency)),str(iMaxMama),str(SignalMinLength),str(signalpercentLoss),DRCresult]    
            #[ базальный - 0 , минимальный баз - 1, максимальный баз - 2 , количество акцелераций - 3 , количество децелераций - 4 , количество децелераций >=30 c - 5, высокие эпизоды - 6, низкие эпизоды - 7, STV - 8, LTV - 9, амплитуда осциляций - 10, частота осциляций - 11, базальный Мама - 12, длина сигнала - 13, потеря сигнала - 14, Доуз - 15]
            return result
            
        def selection_params(self): #Переименование параметров после выделения диапазона
            _translate = QtCore.QCoreApplication.translate
            global allocationGraph
            if allocationGraph!=0: # Если есть выделение
                result=self.new_params()
                self.label_params.setText(_translate("MainWindow", "Параметры выбранного участка"))
                self.label_params_akcel.setText(_translate("MainWindow", result[3]))
                self.label_params_fricoscil.setText(_translate("MainWindow", result[11]+" шт./мин"))
                self.label_params_bazal.setText(_translate("MainWindow", result[0]+" уд/мин"))
                self.label_params_oscil.setText(_translate("MainWindow", result[10]+" уд/мин"))
                self.label_params_fisher.setText(_translate("MainWindow", "---"))
                self.label_params_decel.setText(_translate("MainWindow", result[4]+" (" + result[5] +")"))
                self.label_params_STV.setText(_translate("MainWindow", result[8]+" мс"))
                self.label_params_LTV.setText(_translate("MainWindow", result[9]+" мс"))
                self.label_params_HighEp.setText(_translate("MainWindow", str(round(result[6][0],1))+" мс, "+str(round(result[6][1],1))+" мин"))
                self.label_params_LowEp.setText(_translate("MainWindow", str(round(result[7][0],1))+" мс, "+str(round(result[7][1],1))+" мин"))
                self.label_params_LossPercent.setText(_translate("MainWindow", result[14]+" %" ))
                self.label_params_LengthRecord.setText(_translate("MainWindow", str(round(allocationGraph._rect.getRect()[2]//1))+" мин " + str(round(allocationGraph._rect.getRect()[2]%1*60))+" сек"))
                self.label_params_LengthSignal.setText(_translate("MainWindow", result[13]+" мин"))
                self.label_params_CHSSMama.setText(_translate("MainWindow", result[12] +" уд/мин"))
                self.label_params_FC.setText(_translate("MainWindow",  "---"))
                self.label_params_razmahCHSS.setText(_translate("MainWindow", str(result[1])+" - "+str(result[2])+" уд/мин"))
                self.label_params_douz.setText(_translate("MainWindow",  result[15]))
        
        def event_reset_selection(self): #Сброс выделения графика
            global allocationGraph, firsttime
            if allocationGraph!=0:
                self.graphicsView_Graph.removeItem(allocationGraph)
                self.graphicsView_STVLTV.removeItem(allocationSTVLTV)
            allocationGraph=0
            self.spinBox_start_min.setValue(0)
            self.doubleSpinBox_start_sec.setValue(0)
            self.spinBox_end_min.setValue(0)
            self.doubleSpinBox_end_sec.setValue(0)
            self.retranslateUi(MainWindow)
            self.label_params_douz.setToolTip(None)
            firsttime=0
        def event_exit_btn(self): #Выход из рабочего окна после нажатия по соответствующей кнопке
            if MainWindow.isMaximized()!=1:
                width = MainWindow.frameGeometry().width()
                height = MainWindow.frameGeometry().height()
                global windowsize
                windowsize=[width,height]
            QCoreApplication.quit()
        
        def event_select(self): #Ивент выбора сегмента графика мышью
            global CVB, mMouseAction,allocationGraph, firsttime
            self.label_params_douz.setToolTip(None)
            self.button_segment.setStyleSheet("QPushButton{\n"
                "    border-radius:8px;\n"
                f"    background-color: {hover_grey_color};\n"
                "}"
                "QPushButton:hover{\n"
                "    border-radius:8px;\n"
                f"    background-color: {hover_grey_color};\n"
                "}")
            if allocationGraph!=0:
                firsttime=0
                self.graphicsView_Graph.removeItem(allocationGraph)
                self.graphicsView_STVLTV.removeItem(allocationSTVLTV)
                allocationGraph=0
                self.spinBox_start_min.setValue(0)
                self.doubleSpinBox_start_sec.setValue(0)
                self.spinBox_end_min.setValue(0)
                self.doubleSpinBox_end_sec.setValue(0)
                self.retranslateUi(MainWindow)
            mMouseAction=1
            CVB.setMouseMode(CVB.RectMode)
        
        def retranslateUi(self, MainWindow): 
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(image_path, "logo.ico")))
            MainWindow.setWindowTitle(_translate("MainWindow", "STV540"))
            self.label.setText(_translate("MainWindow", data["DateTimeStart"]))
            self.label_params.setText(_translate("MainWindow", "Параметры исследования"))
            self.label_params_akcel.setText(_translate("MainWindow", str(data["AccelerationsCount"])))
            self.label_bazal.setText(_translate("MainWindow", "Базальный ритм"))
            self.label_params_fricoscil.setText(_translate("MainWindow", str(data["OscillationFrequency"])+" шт./мин"))
            self.label_params_bazal.setText(_translate("MainWindow", str(data["BasalHeartRate"])+" уд/мин"))
            self.label_akcel.setText(_translate("MainWindow", "Количество акцелераций"))
            self.label_oscil.setText(_translate("MainWindow", "Амплитуда осцилляций"))
            self.label_params_oscil.setText(_translate("MainWindow", str(data["OscillationAmplitude"])+" уд/мин"))
            self.label_pokazatel.setText(_translate("MainWindow", "Показатель"))
            self.label_fisher.setText(_translate("MainWindow", "Критерий Фишера"))
            self.label_params_fisher.setText(_translate("MainWindow", str(data["FisherScope"])))
            self.label_params_decel.setText(_translate("MainWindow", str(data["DecelerationsCount"])+" (" + str(data["LastDecelerationsCount"]) +")"))
            self.label_znachenie.setText(_translate("MainWindow", "Значение показателя"))
            self.label_FC.setText(_translate("MainWindow", "Критерий FC"))
            self.label_fricoscil.setText(_translate("MainWindow", "Частота осцилляций"))
            self.label_STV.setText(_translate("MainWindow", "STV"))
            self.label_LTV.setText(_translate("MainWindow", "LTV"))
            self.label_LowEp.setText(_translate("MainWindow", "Низкие эпизоды (мин)"))
            self.label_LossPercent.setText(_translate("MainWindow", "Потеря сигнала"))
            self.label_LengthSignal.setText(_translate("MainWindow", "Длительность сигнала"))
            self.label_LengthRecord.setText(_translate("MainWindow", "Длительность записи"))
            self.label_CHSSMama.setText(_translate("MainWindow", "ЧСС матери"))
            self.label_douz.setText(_translate("MainWindow", "Критерий Доуза-Редмана"))
            self.label_razmahCHSS.setText(_translate("MainWindow", "Размах ЧСС (макс)"))
            self.label_HighEp.setText(_translate("MainWindow", "Высокие эпизоды (мин)"))
            self.label_decel.setText(_translate("MainWindow", "Количество децелераций (из них ⩾30 с)"))
            self.label_params_STV.setText(_translate("MainWindow", str(data["MedianSTV"])+" мс"))
            self.label_params_LTV.setText(_translate("MainWindow", str(data["LTV"])+" мс"))
            self.label_params_HighEp.setText(_translate("MainWindow", str(data["LTVHighBPM"])+" уд/мин, " + str(data["LTVHigh"])+" мин"))
            self.label_params_LowEp.setText(_translate("MainWindow", str(data["LTVLowBPM"])+" уд/мин, " + str(data["LTVLow"])+" мин"))
            self.label_params_LossPercent.setText(_translate("MainWindow", str(data["LostSignalDurationInProcent"])+" %"))
            self.label_params_LengthRecord.setText(_translate("MainWindow", str(data["SignalDurationInMinutes"])+" мин"))
            self.label_params_LengthSignal.setText(_translate("MainWindow", str(data["HeartRateDurationInMinutes"])+" мин"))
            self.label_params_CHSSMama.setText(_translate("MainWindow", str(data["MomeHeartRate"])+" уд/мин"))
            if data["DRC"]==True:
                DRC="Соблюдены"
            else:
                DRC="Не соблюдены"
            self.label_params_douz.setText(_translate("MainWindow",  DRC))
            self.label_params_FC.setText(_translate("MainWindow",  str(data["FCScore"])+"%"))
            self.label_params_razmahCHSS.setText(_translate("MainWindow", str(data["MinBasalHeartRate"])+" - "+str(data["MaxBasalHeartRate"])+" уд/мин"))
            self.label_start_min.setText(_translate("MainWindow", "м"))
            self.label_start_sec.setText(_translate("MainWindow", "с"))
            self.label_start.setText(_translate("MainWindow", "Начало"))
            self.label_endmin.setText(_translate("MainWindow", "м"))
            self.label_endsec.setText(_translate("MainWindow", "с"))
            self.label_end.setText(_translate("MainWindow", "Конец"))
            self.pushButton_additional_reset.setText(_translate("MainWindow", "Сбросить"))
            self.label_additional.setText(_translate("MainWindow", "Выделение участка"))
        def mom(self): #Отрисовка графика мамы
            
            edgeslist=[]
            count=0
            for item in data["isBreakMomHeartRateGraphic"]: #преобразование в формат координат по оси x
                if item == 0:
                    edgeslist.append(count)
                count+=1
            edgeslist.append(len(data["isBreakFetusHeartRateGraphic"]))    
            count=-1
            
            datainminutesMom=[]
            for second in data["xMomeHeartRateGraphic"]:
                datainminutesMom.append(second/60)
            
            for edge in edgeslist: #заполнение графика
                if edgeslist[0]==edge:
                    self.graphicsView_Graph.plot(datainminutesMom[0:edge:1], data["yMomHeartRateGraphic"][0:edge:1],pen=fg_green_color)
                else:
                    self.graphicsView_Graph.plot(datainminutesMom[edgeslist[count]:edge:1], data["yMomHeartRateGraphic"][edgeslist[count]:edge:1],pen=fg_green_color)  
                count+=1         
                
                
        def fillgraph(self): #Отрисовка основного графика, базального и графика СТВ ЛТВ
            global STVLTVinminutes
            edgeslist=[]
            count=0
            for item in data["isBreakFetusHeartRateGraphic"]: #преобразование в формат координат по оси x
                if item == 0:
                    edgeslist.append(count)
                count+=1
            edgeslist.append(len(data["isBreakFetusHeartRateGraphic"]))    
            count=-1

            datainminutes=[] #перевод формата из секунд в минуты
            
            STVLTVinminutes=[]
            for second in data["xFetusHeartRateGraphic"]:
                datainminutes.append(second/60)
            
            for second in data["xSTVPivotTable"]:
                STVLTVinminutes.append(data["xFetusHeartRateGraphic"][second]/60)
            pen = pg.mkPen(color="r")
            for edge in edgeslist: #заполнение графика
                if edgeslist[0]==edge:
                    self.graphicsView_Graph.plot(datainminutes[0:edge:1], data["yFetusHeartRateGraphic"][0:edge:1])
                    self.graphicsView_Graph.plot(datainminutes[0:edge:1], data["yFetusBasalRateGraphic"][0:edge:1], pen=pen)
                else:
                    self.graphicsView_Graph.plot(datainminutes[edgeslist[count]:edge:1], data["yFetusHeartRateGraphic"][edgeslist[count]:edge:1])
                    self.graphicsView_Graph.plot(datainminutes[edgeslist[count]:edge:1], data["yFetusBasalRateGraphic"][edgeslist[count]:edge:1], pen=pen)    
                count+=1  
            if momcheck==1:   
                self.mom()
            if cursorcheck==1:
                global cursorsignal
                self.mouseXInfo=pg.TextItem(text=" ",color=fg_yellow_color,anchor=(0,-1))
                font = QtGui.QFont()
                font.setFamily("Arial")
                font.setBold(True)
                font.setPointSize(10)
                self.mouseXInfo.setFont(font)
                self.graphicsView_Graph.addItem(self.mouseXInfo)
                CVB.scene().sigMouseMoved.connect(self.mouseMoved)
                cursorsignal=1
            self.label_STV_Graph = pg.TextItem(text="STV", color=(255,255,255)) 
            self.label_STV_Graph.setPos(-1, 8)
            self.graphicsView_STVLTV.addItem(self.label_STV_Graph)
            self.label_LTV_Graph = pg.TextItem(text="LTV", color=(255,255,255))
            self.label_LTV_Graph.setPos(-1, 4)
            self.graphicsView_STVLTV.addItem(self.label_LTV_Graph)
            
            global isHigh, isLow
            
            isHigh = [0]*len(data["LTVPivotTable"])
            isLow= [0]*len(data["LTVPivotTable"])
            for i in range(0,len(data["LTVPivotTable"])):
                high = 0
                low = 0
                for j in range(0,6):
                    if(i+j>= len(data["LTVPivotTable"])):
                        break
                    if data["LTVPivotTable"][i+j]>=32:
                        high+=1
                    if data["LTVPivotTable"][i+j]<31:
                        low+=1
                if high>=5:
                    for j in range(0,6):
                        if i+j>=len(data["LTVPivotTable"]):
                            break
                        isHigh[i+j]=1
                if low>=5:
                    for j in range(0,6):
                        if i+j>=len(data["LTVPivotTable"]):
                            break
                        isLow[i+j]=1
            for i in range(0,len(data["LTVPivotTable"])):
                if (isHigh[i]==1 and isLow[i]==1):
                    isHigh[i]=0
            
            count=0
            tilelength=1.06
            
            for tile in STVLTVinminutes:#заполнение STV и LTV
                STVBrush = [fg_green_color,"w"]
                LTVBrush= [fg_green_color,"w"]
                if data["STVPivotTable"][count]<4.5:
                    STVBrush = ["r","w"]
                if isHigh[count]==0 and isLow[count]==0:
                    LTVBrush = ["black","w"]
                elif isHigh[count]==1 and isLow[count]==0:
                    LTVBrush = [fg_green_color,"w"]
                elif isHigh[count]==0 and isLow[count]==1:
                    LTVBrush = ["r","w"]
                    
                if (STVLTVinminutes[count]!=STVLTVinminutes[-1]) and ((STVLTVinminutes[count+1]-STVLTVinminutes[count])<1.0666666666666667):
                    newX=tile-(tilelength-(STVLTVinminutes[count+1]-STVLTVinminutes[count]))
                    #STV
                    rect_item = RectItem(QtCore.QRectF(newX, 2, tilelength, 2),LTVBrush[0],LTVBrush[1])
                    self.graphicsView_STVLTV.addItem(rect_item)
                    self.label_STV_Graph = pg.TextItem(text=str(data["LTVPivotTable"][count]), color=(0,0,0))
                    self.label_STV_Graph.setPos(newX,4)
                    self.graphicsView_STVLTV.addItem(self.label_STV_Graph)
                    #LTV
                    rect_item = RectItem(QtCore.QRectF(newX, 6, tilelength, 2),STVBrush[0],STVBrush[1])
                    self.graphicsView_STVLTV.addItem(rect_item)
                    self.label_LTV_Graph = pg.TextItem(text=str(data["STVPivotTable"][count]), color=(0,0,0))
                    self.label_LTV_Graph.setPos(newX,8)
                    self.graphicsView_STVLTV.addItem(self.label_LTV_Graph)
                else:
                    #STV
                    rect_item = RectItem(QtCore.QRectF(tile, 2, tilelength, 2),LTVBrush[0],LTVBrush[1])
                    self.graphicsView_STVLTV.addItem(rect_item)
                    self.label_STV_Graph = pg.TextItem(text=str(data["LTVPivotTable"][count]), color=(0,0,0))
                    self.label_STV_Graph.setPos(tile,4)
                    self.graphicsView_STVLTV.addItem(self.label_STV_Graph)
                    #LTV
                    rect_item = RectItem(QtCore.QRectF(tile, 6, tilelength, 2),STVBrush[0],STVBrush[1])
                    self.graphicsView_STVLTV.addItem(rect_item)
                    self.label_LTV_Graph = pg.TextItem(text=str(data["STVPivotTable"][count]), color=(0,0,0))
                    self.label_LTV_Graph.setPos(tile,8)
                    self.graphicsView_STVLTV.addItem(self.label_LTV_Graph)
                count+=1
                
                  
            self.graphicsView_Graph.setYRange(50, 230,padding=0)
            self.graphicsView_Graph.showGrid(True, True, 0.5)
            self.graphicsView_Graph.setMouseEnabled(x=True, y=False)
            axBottom = self.graphicsView_Graph.getAxis('bottom') #get x axis
            xTicks = [1, 2]
            axLeft = self.graphicsView_Graph.getAxis('left') #get y axis
            yTicks = [20, 40]
            axLeft.setTickSpacing(yTicks[0], yTicks[1])
            axBottom.setTickSpacing(xTicks[0], xTicks[1])
            self.graphicsView_STVLTV.plotItem.setXLink(self.graphicsView_Graph.plotItem)
            self.graphicsView_STVLTV.setYRange(0, 10,padding=0)
            self.graphicsView_STVLTV.showGrid(True, True, 0.5)
            self.graphicsView_STVLTV.setMouseEnabled(x=True, y=False)
            axBottom = self.graphicsView_STVLTV.getAxis('bottom') #get x axis
            xTicks = [1, 2]
            axLeft = self.graphicsView_STVLTV.getAxis('left') #get y axis
            yTicks = [1, 2]
            axLeft.setTickSpacing(yTicks[0], yTicks[1])
            axBottom.setTickSpacing(xTicks[0], xTicks[1])
            self.graphicsView_STVLTV.hideAxis('left')
            self.graphicsView_STVLTV.hideButtons()
            self.graphicsView_Graph.hideButtons()
            self.graphicsView_Graph.addItem(scatter)
            scatter.clear()
            if decelcheck==1:  
                self.metkidec()
            if accelcheck==1:  
                self.metkiacc()
            #---------------------Создание карты длительности сигнала
            
            def signallength():    
                global signalmap
                signalmap=[]
                step=0
                score=0
                x1=0
                x2=len(data["xFetusHeartRateGraphic"])
                for i in range(x1,x2-1):
                    if data["xFetusHeartRateGraphic"][i+1]-data["xFetusHeartRateGraphic"][i]==1:
                        score+=1
                    else:
                        score+=1
                    if data["xFetusHeartRateGraphic"][i+1]//60>step:
                        signalmap.append([step,score])
                        step+=data["xFetusHeartRateGraphic"][i+1]//60-step
                        score=0 
                    if (i==x2-2):
                        step=(data["xFetusHeartRateGraphic"][i+1]//60)
                        signalmap.append([step,score])
            signallength()    
            #---------------------    
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    app1.deiconify()
    if app1.winfo_screenwidth()!=windowsize[0] and app1.winfo_screenheight()!=windowsize[1]:
        x=app1.winfo_screenwidth()/2-windowsize[0]/2
        y=app1.winfo_screenheight()/2-windowsize[1]/2
        app1.geometry(f"{windowsize[0]}x{windowsize[1]}+{int(x)}+{int(y)}")
    else:
        app1.state('zoomed') 
    
def CompareSpace(data,app1): #Модуль сравнения исследований
    global windowsize
    windowsize[0]=app1.winfo_width()
    windowsize[1]=app1.winfo_height()
    app1.withdraw()
    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
            sizePolicy.setHorizontalStretch(0)
            sizePolicy.setVerticalStretch(0)
            sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
            MainWindow.setSizePolicy(sizePolicy)
            MainWindow.setMinimumSize(QtCore.QSize(843, 400))
            MainWindow.setBaseSize(QtCore.QSize(1280, 720))
            MainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
            if app1.winfo_screenwidth()!=windowsize[0] and app1.winfo_screenheight()!=windowsize[1]:
                MainWindow.resize(windowsize[0], windowsize[1])
            else:
                MainWindow.showMaximized() 
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.gridLayout_central = QtWidgets.QGridLayout(self.centralwidget)
            self.gridLayout_central.setObjectName("gridLayout_central")
            self.frame_label = QtWidgets.QFrame(self.centralwidget)
            self.frame_label.setMinimumSize(QtCore.QSize(0, 80))
            self.frame_label.setMaximumSize(QtCore.QSize(16777215, 80))
            self.frame_label.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}")
            self.frame_label.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.frame_label.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame_label.setObjectName("frame_label")
            self.gridLayout_frame_label = QtWidgets.QGridLayout(self.frame_label)
            self.gridLayout_frame_label.setObjectName("gridLayout_frame_label")
            self.exit_btn = QtWidgets.QPushButton(self.frame_label)
            self.exit_btn.setMinimumSize(QtCore.QSize(60, 60))
            self.exit_btn.setMaximumSize(QtCore.QSize(60, 60))
            self.exit_btn.setText("")
            self.exit_btn.setObjectName("exit_btn")
            self.exit_btn.clicked.connect(self.event_exit_btn)
            self.exit_btn.setStyleSheet("QPushButton{\n"
            "    border-radius:8px;\n"
            "    background-color: rgb(105, 175, 99);\n"
            "}"
            "QPushButton:hover{\n"
            "    border-radius:8px;\n"
            f"    background-color: {hover_green_color};\n"
            "}")
            self.exit_btn.setIconSize(QtCore.QSize(50, 50))
            self.exit_btn.setIcon(QtGui.QIcon(os.path.join(image_path, "exit.png")))
            self.gridLayout_frame_label.addWidget(self.exit_btn, 0, 0, 1, 1)
            self.label = QtWidgets.QLabel(self.frame_label)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(20)
            self.label.setFont(font)
            self.label.setAlignment(QtCore.Qt.AlignCenter)
            self.label.setObjectName("label")
            self.gridLayout_frame_label.addWidget(self.label, 0, 1, 1, 1)
            spacerItem = QtWidgets.QSpacerItem(66, 20, QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Minimum)
            self.gridLayout_frame_label.addItem(spacerItem, 0, 2, 1, 1)
            self.gridLayout_central.addWidget(self.frame_label, 0, 0, 1, 1)
            self.main_frame = QtWidgets.QFrame(self.centralwidget)
            self.main_frame.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}")
            self.main_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.main_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.main_frame.setObjectName("main_frame")
            self.gridLayout_main_frame = QtWidgets.QGridLayout(self.main_frame)
            self.gridLayout_main_frame.setObjectName("gridLayout_main_frame")
            self.main_splitter = QtWidgets.QSplitter(self.main_frame)
            self.main_splitter.setOrientation(QtCore.Qt.Horizontal)
            self.main_splitter.setObjectName("main_splitter")
            self.left_frame = QtWidgets.QFrame(self.main_splitter)
            self.left_frame.setMinimumSize(QtCore.QSize(260, 0))
            self.left_frame.setMaximumSize(QtCore.QSize(260, 16777215))
            self.left_frame.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    \n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.left_frame.setObjectName("left_frame")
            self.gridLayout_left_frame = QtWidgets.QGridLayout(self.left_frame)
            self.gridLayout_left_frame.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_left_frame.setSpacing(0)
            self.gridLayout_left_frame.setObjectName("gridLayout_left_frame")
            self.label_params = QtWidgets.QLabel(self.left_frame)
            self.label_params.setMinimumSize(QtCore.QSize(0, 55))
            self.label_params.setMaximumSize(QtCore.QSize(16777215, 55))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_params.setFont(font)
            self.label_params.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params.setWordWrap(True)
            self.label_params.setObjectName("label_params")
            self.gridLayout_left_frame.addWidget(self.label_params, 0, 0, 1, 1)
            self.params_scrollarea = QtWidgets.QScrollArea(self.left_frame)
            self.params_scrollarea.setStyleSheet("")
            self.params_scrollarea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.params_scrollarea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.params_scrollarea.setWidgetResizable(True)
            self.params_scrollarea.setObjectName("params_scrollarea")
            self.params_scrollarea_frame = QtWidgets.QWidget()
            self.params_scrollarea_frame.setEnabled(True)
            self.params_scrollarea_frame.setGeometry(QtCore.QRect(0, 0, 261, 629))
            self.params_scrollarea_frame.setStyleSheet("QWidget{\n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.params_scrollarea_frame.setObjectName("params_scrollarea_frame")
            self.gridLayout_params = QtWidgets.QGridLayout(self.params_scrollarea_frame)
            self.gridLayout_params.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_params.setSpacing(0)
            self.gridLayout_params.setObjectName("gridLayout_params")
            self.label_signal = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_signal.setFont(font)
            self.label_signal.setStyleSheet("")
            self.label_signal.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_signal.setObjectName("label_signal")
            self.label_signal.setMargin(5)
            self.gridLayout_params.addWidget(self.label_signal, 3, 0, 1, 1)
            self.label_time = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_time.setFont(font)
            self.label_time.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_time.setObjectName("label_time")
            self.label_time.setMargin(5)
            self.gridLayout_params.addWidget(self.label_time, 1, 0, 1, 1)
            self.label_accel = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_accel.setFont(font)
            self.label_accel.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_accel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_accel.setObjectName("label_accel")
            self.label_accel.setMargin(5)
            self.gridLayout_params.addWidget(self.label_accel, 4, 0, 1, 1)
            self.label_decel = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_decel.setFont(font)
            self.label_decel.setStyleSheet("")
            self.label_decel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_decel.setObjectName("label_decel")
            self.label_decel.setMargin(5)
            self.gridLayout_params.addWidget(self.label_decel, 5, 0, 1, 1)
            self.label_oscil_amplituda = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_oscil_amplituda.setFont(font)
            self.label_oscil_amplituda.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_oscil_amplituda.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_oscil_amplituda.setObjectName("label_oscil_amplituda")
            self.label_oscil_amplituda.setMargin(5)
            self.gridLayout_params.addWidget(self.label_oscil_amplituda, 6, 0, 1, 1)
            self.label_date = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_date.setFont(font)
            self.label_date.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_date.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_date.setObjectName("label_date")
            self.label_date.setMargin(5)
            self.gridLayout_params.addWidget(self.label_date, 0, 0, 1, 1)
            self.label_CHSS = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_CHSS.setFont(font)
            self.label_CHSS.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            self.label_CHSS.setObjectName("label_CHSS")
            self.label_CHSS.setMargin(5)
            self.gridLayout_params.addWidget(self.label_CHSS, 11, 0, 1, 1)
            self.label_LTV = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_LTV.setFont(font)
            self.label_LTV.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_LTV.setObjectName("label_LTV")
            self.label_LTV.setMargin(5)
            self.gridLayout_params.addWidget(self.label_LTV, 8, 0, 1, 1)
            self.label_douz = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_douz.setFont(font)
            self.label_douz.setObjectName("label_douz")
            self.label_douz.setMargin(5)
            self.gridLayout_params.addWidget(self.label_douz, 9, 0, 1, 1)
            self.label_STV = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_STV.setFont(font)
            self.label_STV.setObjectName("label_STV")
            self.label_STV.setMargin(5)
            self.gridLayout_params.addWidget(self.label_STV, 7, 0, 1, 1)
            self.label_srok = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_srok.setFont(font)
            self.label_srok.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_srok.setObjectName("label_srok")
            self.label_srok.setMargin(5)
            self.gridLayout_params.addWidget(self.label_srok, 2, 0, 1, 1)
            self.label_bazal = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_bazal.setFont(font)
            self.label_bazal.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_bazal.setObjectName("label_bazal")
            self.label_bazal.setMargin(5)
            self.gridLayout_params.addWidget(self.label_bazal, 12, 0, 1, 1)
            spacerItem1 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.gridLayout_params.addItem(spacerItem1, 13, 0, 1, 1)
            self.label_fisher = QtWidgets.QLabel(self.params_scrollarea_frame)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_fisher.setFont(font)
            self.label_fisher.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_fisher.setObjectName("label_fisher")
            self.label_fisher.setMargin(5)
            self.gridLayout_params.addWidget(self.label_fisher, 10, 0, 1, 1)
            self.params_scrollarea.setWidget(self.params_scrollarea_frame)
            self.gridLayout_left_frame.addWidget(self.params_scrollarea, 1, 0, 1, 1)
            self.middle_frame = QtWidgets.QFrame(self.main_splitter)
            self.middle_frame.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.middle_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.middle_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.middle_frame.setObjectName("middle_frame")
            self.gridLayout_middle_frame = QtWidgets.QGridLayout(self.middle_frame)
            self.gridLayout_middle_frame.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_middle_frame.setSpacing(0)
            self.gridLayout_middle_frame.setObjectName("gridLayout_middle_frame")
            self.label_middle = QtWidgets.QLabel(self.middle_frame)
            self.label_middle.setMinimumSize(QtCore.QSize(0, 55))
            self.label_middle.setMaximumSize(QtCore.QSize(16777215, 55))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_middle.setFont(font)
            self.label_middle.setAlignment(QtCore.Qt.AlignCenter)
            self.label_middle.setObjectName("label_middle")
            self.gridLayout_middle_frame.addWidget(self.label_middle, 0, 0, 1, 1)
            self.scrollArea_middle = QtWidgets.QScrollArea(self.middle_frame)
            self.scrollArea_middle.setStyleSheet("QWidget{\n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.scrollArea_middle.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
            self.scrollArea_middle.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
            self.scrollArea_middle.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
            self.scrollArea_middle.setWidgetResizable(True)
            self.scrollArea_middle.setObjectName("scrollArea_middle")
            self.scrollAreaWidgetContents_middle = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_middle.setGeometry(QtCore.QRect(0, 0, 600, 612))
            self.scrollAreaWidgetContents_middle.setObjectName("scrollAreaWidgetContents_middle")
            self.gridLayout_scroll_middle = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_middle)
            self.gridLayout_scroll_middle.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_scroll_middle.setSpacing(0)
            self.gridLayout_scroll_middle.setObjectName("gridLayout_scroll_middle")
            self.right_frame = QtWidgets.QFrame(self.main_splitter)
            self.right_frame.setMinimumSize(QtCore.QSize(260, 0))
            self.right_frame.setMaximumSize(QtCore.QSize(260, 16777215))
            self.right_frame.setStyleSheet("QFrame{\n"
    "    border-radius:8px;\n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
            self.right_frame.setObjectName("right_frame")
            self.gridLayout_right_frame = QtWidgets.QGridLayout(self.right_frame)
            self.gridLayout_right_frame.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_right_frame.setSpacing(0)
            self.gridLayout_right_frame.setObjectName("gridLayout_right_frame")
            self.scrollArea_right = QtWidgets.QScrollArea(self.right_frame)
            self.scrollArea_right.setStyleSheet("QWidget{\n"
    "    background-color: rgb(207, 207, 207);\n"
    "}")
            self.scrollArea_right.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scrollArea_right.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.scrollArea_right.setWidgetResizable(True)
            self.scrollArea_right.setObjectName("scrollArea_right")
            self.scrollAreaWidgetContents_right = QtWidgets.QWidget()
            self.scrollAreaWidgetContents_right.setGeometry(QtCore.QRect(0, 0, 260, 629))
            self.scrollAreaWidgetContents_right.setObjectName("scrollAreaWidgetContents_right")
            self.gridLayout_right = QtWidgets.QGridLayout(self.scrollAreaWidgetContents_right)
            self.gridLayout_right.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_right.setSpacing(0)
            self.gridLayout_right.setObjectName("gridLayout_right")
            self.label_max_params_date = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_date.setFont(font)
            self.label_max_params_date.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_date.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_date.setObjectName("label_max_params_date")
            self.label_max_params_date.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_date, 0, 0, 1, 1)
            self.label_max_params_time = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_time.setFont(font)
            self.label_max_params_time.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_time.setObjectName("label_max_params_time")
            self.label_max_params_time.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_time, 1, 0, 1, 1)
            self.label_max_params_signallength = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_signallength.setFont(font)
            self.label_max_params_signallength.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_signallength.setObjectName("label_max_params_signallength")
            self.label_max_params_signallength.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_signallength, 3, 0, 1, 1)
            self.label_max_params_srok = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_srok.setFont(font)
            self.label_max_params_srok.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_srok.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_srok.setObjectName("label_max_params_srok")
            self.label_max_params_srok.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_srok, 2, 0, 1, 1)
            self.label_max_params_accel = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_accel.setFont(font)
            self.label_max_params_accel.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_accel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_accel.setObjectName("label_max_params_accel")
            self.label_max_params_accel.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_accel, 4, 0, 1, 1)
            self.label_max_params_amp_osc = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_amp_osc.setFont(font)
            self.label_max_params_amp_osc.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_amp_osc.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_amp_osc.setObjectName("label_max_params_amp_osc")
            self.label_max_params_amp_osc.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_amp_osc, 6, 0, 1, 1)
            self.label_max_params_STV = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_STV.setFont(font)
            self.label_max_params_STV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_STV.setObjectName("label_max_params_STV")
            self.label_max_params_STV.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_STV, 7, 0, 1, 1)
            self.label_max_params_decel = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_decel.setFont(font)
            self.label_max_params_decel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_decel.setObjectName("label_max_params_decel")
            self.label_max_params_decel.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_decel, 5, 0, 1, 1)
            self.label_max_params_douz = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_douz.setFont(font)
            self.label_max_params_douz.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_douz.setObjectName("label_max_params_douz")
            self.label_max_params_douz.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_douz, 9, 0, 1, 1)
            self.label_max_params_LTV = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_LTV.setFont(font)
            self.label_max_params_LTV.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_LTV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_LTV.setObjectName("label_max_params_LTV")
            self.label_max_params_LTV.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_LTV, 8, 0, 1, 1)
            spacerItem2 = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
            self.gridLayout_right.addItem(spacerItem2, 13, 0, 1, 1)
            self.label_max_params_fisher = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_fisher.setFont(font)
            self.label_max_params_fisher.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_fisher.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_fisher.setObjectName("label_max_params_fisher")
            self.label_max_params_fisher.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_fisher, 10, 0, 1, 1)
            self.label_max_params_CHSS = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_CHSS.setFont(font)
            self.label_max_params_CHSS.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_CHSS.setObjectName("label_max_params_CHSS")
            self.label_max_params_CHSS.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_CHSS, 11, 0, 1, 1)
            self.label_max_params_bazal = QtWidgets.QLabel(self.scrollAreaWidgetContents_right)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_max_params_bazal.setFont(font)
            self.label_max_params_bazal.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_max_params_bazal.setAlignment(QtCore.Qt.AlignCenter)
            self.label_max_params_bazal.setObjectName("label_max_params_bazal")
            self.label_max_params_bazal.setMargin(5)
            self.gridLayout_right.addWidget(self.label_max_params_bazal, 12, 0, 1, 1)
            self.scrollArea_right.setWidget(self.scrollAreaWidgetContents_right)
            self.gridLayout_right_frame.addWidget(self.scrollArea_right, 1, 0, 1, 1)
            self.label_right = QtWidgets.QLabel(self.right_frame)
            self.label_right.setMinimumSize(QtCore.QSize(0, 55))
            self.label_right.setMaximumSize(QtCore.QSize(16777215, 55))
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.label_right.setFont(font)
            self.label_right.setAlignment(QtCore.Qt.AlignCenter)
            self.label_right.setWordWrap(True)
            self.label_right.setObjectName("label_right")
            self.gridLayout_right_frame.addWidget(self.label_right, 0, 0, 1, 1)
            self.gridLayout_main_frame.addWidget(self.main_splitter, 0, 0, 1, 1)
            self.gridLayout_central.addWidget(self.main_frame, 1, 0, 1, 1)
            MainWindow.setCentralWidget(self.centralwidget)
            self.retranslateUi(MainWindow)
            self.createresearchelist()
            self.scrollArea_middle.verticalScrollBar().valueChanged.connect(lambda value: self.scrollArea_right.verticalScrollBar().setValue(value))
            self.scrollArea_middle.verticalScrollBar().valueChanged.connect(lambda value: self.params_scrollarea.verticalScrollBar().setValue(value))
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
        def event_exit_btn(self): #Выход из рабочего окна после нажатия по соответствующей кнопке
            if MainWindow.isMaximized()!=1:
                width = MainWindow.frameGeometry().width()
                height = MainWindow.frameGeometry().height()
                global windowsize
                windowsize=[width,height]
            QCoreApplication.quit()
        
        def createresearchelist(self): #Проход по массиву поданных исследований, с выделением параметров и заполнением листа исследований
            averageparams={
                "amount":0,
                "accel":0,
                "decel":0,
                "osc":0,
                "STV":0,
                "LTV":0,
                "fisher":0,
                "CHSS":[0,0],
                "bazal":0,
                }
            for i in range(len(data)):
                params={
                    "pos":i,
                    "date":data[i]["DateTimeStart"].split(" ")[0],
                    "time":data[i]["DateTimeStart"].split(" ")[1],
                    "signallength":data[i]["HeartRateDurationInMinutes"],
                    "accel":data[i]["AccelerationsCount"],
                    "decel":data[i]["DecelerationsCount"],
                    "decel>30":data[i]["LastDecelerationsCount"],
                    "osc":data[i]["OscillationAmplitude"],
                    "STV":data[i]["MedianSTV"],
                    "LTV":data[i]["LTV"],
                    "douz":data[i]["DRC"],
                    "fisher":data[i]["FisherScope"],
                    "CHSS":[data[i]["MinBasalHeartRate"],data[i]["MaxBasalHeartRate"]],
                    "bazal":data[i]["BasalHeartRate"],
                    "srok":data[i]["GestationalAge"]
                }
                averageparams["amount"] +=1
                averageparams["accel"] = params["accel"]+averageparams["accel"]
                averageparams["decel"] = params["decel"]+averageparams["decel"]
                averageparams["osc"] = params["osc"]+averageparams["osc"]
                averageparams["STV"] = params["STV"]+averageparams["STV"]
                averageparams["LTV"] = params["LTV"]+averageparams["LTV"]
                averageparams["fisher"] = params["fisher"]+averageparams["fisher"]
                averageparams["CHSS"][0] = params["CHSS"][0]+averageparams["CHSS"][0]
                averageparams["CHSS"][1] = params["CHSS"][1]+averageparams["CHSS"][1]
                averageparams["bazal"] = params["bazal"]+averageparams["bazal"]
                if data[i]["DRC"]==True:
                    params["douz"]="Соблюдены"
                else: params["douz"]="Не соблюдены"
                def comparestats(type1,type2):
                    if i!=len(data)-1:
                        if data[i][type1]<data[i+1][type1]:
                            if type2!="bazal" and type2!="LTV":
                                    params[type2]="↓ "+str(params[type2])
                            elif (data[i+1][type1]-data[i][type1])>4:
                                params[type2]="↓ "+str(params[type2])
                        elif data[i][type1]>data[i+1][type1]:
                            if type2!="bazal" and type2!="LTV":
                                    params[type2]="↑ "+str(params[type2])
                            elif (data[i][type1]-data[i+1][type1])>4:
                                params[type2]="↑ "+str(params[type2])
                comparestats("MedianSTV","STV")
                comparestats("LTV","LTV")
                comparestats("BasalHeartRate","bazal")
                comparestats("FisherScope","fisher")
                comparestats("OscillationAmplitude","osc")
                comparestats("AccelerationsCount","accel")
                comparestats("DecelerationsCount","decel")
                self.addresearch(params) #Добавление исследования с выделенными параметрами
            
            #Установка средних значений
            _translate = QtCore.QCoreApplication.translate
            self.label_max_params_date.setText(_translate("MainWindow", "---"))
            self.label_max_params_time.setText(_translate("MainWindow", "---"))
            self.label_max_params_signallength.setText(_translate("MainWindow", "---"))
            self.label_max_params_srok.setText(_translate("MainWindow", "---"))
            self.label_max_params_accel.setText(_translate("MainWindow", str(round(averageparams["accel"]/averageparams["amount"]))))
            self.label_max_params_amp_osc.setText(_translate("MainWindow", str(round(averageparams["osc"]/averageparams["amount"]))+" уд/мин"))
            self.label_max_params_STV.setText(_translate("MainWindow", str(round(averageparams["STV"]/averageparams["amount"],2))+" мс"))
            self.label_max_params_decel.setText(_translate("MainWindow", str(round(averageparams["decel"]/averageparams["amount"]))))
            self.label_max_params_douz.setText(_translate("MainWindow", "---"))
            self.label_max_params_LTV.setText(_translate("MainWindow", str(round(averageparams["LTV"]/averageparams["amount"],2))+" мс"))
            self.label_max_params_fisher.setText(_translate("MainWindow", str(round(averageparams["fisher"]/averageparams["amount"]))))
            self.label_max_params_CHSS.setText(_translate("MainWindow", str(round(averageparams["CHSS"][0]/averageparams["amount"])) +" - "+str(round(averageparams["CHSS"][1]/averageparams["amount"]))+" уд/мин"))
            self.label_max_params_bazal.setText(_translate("MainWindow", str(round(averageparams["bazal"]/averageparams["amount"]))+" уд/мин"))               
        
        def addresearch(self, params): #Добавление исследования с выделенными параметрами
            self.example_frame_1 = QtWidgets.QFrame(self.scrollAreaWidgetContents_middle)
            self.example_frame_1.setMinimumSize(QtCore.QSize(200, 0))
            self.example_frame_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
            self.example_frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.example_frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
            self.example_frame_1.setObjectName("example_frame_1")
            self.gridLayout_example = QtWidgets.QGridLayout(self.example_frame_1)
            self.gridLayout_example.setContentsMargins(0, 0, 0, 0)
            self.gridLayout_example.setSpacing(0)
            self.gridLayout_example.setObjectName("gridLayout_example")
            self.label_params_signallength = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_signallength.setFont(font)
            self.label_params_signallength.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_signallength.setObjectName("label_params_signallength")
            self.label_params_signallength.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_signallength, 3, 0, 1, 1)
            self.label_params_accel = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_accel.setFont(font)
            self.label_params_accel.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_params_accel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_accel.setObjectName("label_params_accel")
            self.label_params_accel.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_accel, 4, 0, 1, 1)
            self.label_params_decel = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_decel.setFont(font)
            self.label_params_decel.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_decel.setObjectName("label_params_decel")
            self.label_params_decel.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_decel, 5, 0, 1, 1)
            self.label_params_date = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_date.setFont(font)
            self.label_params_date.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_params_date.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_date.setObjectName("label_params_date")
            self.label_params_date.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_date, 0, 0, 1, 1)
            self.label_params_time = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_time.setFont(font)
            self.label_params_time.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_time.setObjectName("label_params_time")
            self.label_params_time.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_time, 1, 0, 1, 1)
            self.label_params_srok = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_srok.setFont(font)
            self.label_params_srok.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_params_srok.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_srok.setObjectName("label_params_srok")
            self.label_params_srok.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_srok, 2, 0, 1, 1)
            self.label_params_amp_osc = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_amp_osc.setFont(font)
            self.label_params_amp_osc.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}\n"
    "")
            self.label_params_amp_osc.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_amp_osc.setObjectName("label_params_amp_osc")
            self.label_params_amp_osc.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_amp_osc, 6, 0, 1, 1)
            self.label_params_STV = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_STV.setFont(font)
            self.label_params_STV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_STV.setObjectName("label_params_STV")
            self.label_params_STV.setMargin(5)
            self.label_params_STV.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_STV, 7, 0, 1, 1)
            self.label_params_LTV = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_LTV.setFont(font)
            self.label_params_LTV.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}")
            self.label_params_LTV.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_LTV.setObjectName("label_params_LTV")
            self.label_params_LTV.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_LTV, 8, 0, 1, 1)
            self.label_params_fisher = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_fisher.setFont(font)
            self.label_params_fisher.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}")
            self.label_params_fisher.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_fisher.setObjectName("label_params_fisher")
            self.label_params_fisher.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_fisher, 10, 0, 1, 1)
            self.label_params_douz = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_douz.setFont(font)
            self.label_params_douz.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_douz.setObjectName("label_params_douz")
            self.label_params_douz.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_douz, 9, 0, 1, 1)
            self.label_params_CHSS = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_CHSS.setFont(font)
            self.label_params_CHSS.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_CHSS.setObjectName("label_params_CHSS")
            self.label_params_CHSS.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_CHSS, 11, 0, 1, 1)
            self.label_params_bazal = QtWidgets.QLabel(self.example_frame_1)
            font = QtGui.QFont()
            font.setFamily("Arial")
            font.setPointSize(12)
            self.label_params_bazal.setFont(font)
            self.label_params_bazal.setStyleSheet("QLabel{\n"
    "    border-radius:0px;\n"
    "    background-color: rgb(219, 219, 219);\n"
    "}")
            self.label_params_bazal.setAlignment(QtCore.Qt.AlignCenter)
            self.label_params_bazal.setObjectName("label_params_bazal")
            self.label_params_bazal.setMargin(5)
            self.gridLayout_example.addWidget(self.label_params_bazal, 12, 0, 1, 1)
            self.gridLayout_scroll_middle.addWidget(self.example_frame_1, 0, params["pos"], 1, 1)
            self.scrollArea_middle.setWidget(self.scrollAreaWidgetContents_middle)
            self.gridLayout_middle_frame.addWidget(self.scrollArea_middle, 1, 0, 1, 1)
            _translate = QtCore.QCoreApplication.translate
            
            #def setcolor(label, info): # Возможно пригодится, если нужно будет менять цвет
            #    if info[1]==0:
            #        print(label.styleSheet())
            #        label.setStyleSheet(label.styleSheet().split("}")[0]+"color: rgb(255, 255, 0);}")
                
            self.label_params_signallength.setText(_translate("MainWindow", str(params["signallength"])+" мин"))
            #setcolor(self.label_params_accel,params["accel"])
            self.label_params_accel.setText(_translate("MainWindow", str(params["accel"])))
            self.label_params_decel.setText(_translate("MainWindow", str(params["decel"])+" ("+str(params["decel>30"])+")"))
            self.label_params_date.setText(_translate("MainWindow", str(params["date"])))
            self.label_params_time.setText(_translate("MainWindow", str(params["time"])))
            self.label_params_srok.setText(_translate("MainWindow", str(params["srok"])))
            self.label_params_amp_osc.setText(_translate("MainWindow", str(params["osc"])+" уд/мин"))
            self.label_params_STV.setText(_translate("MainWindow", str(params["STV"])+" мс"))
            self.label_params_LTV.setText(_translate("MainWindow", str(params["LTV"])+" мс"))
            self.label_params_fisher.setText(_translate("MainWindow", str(params["fisher"])))
            self.label_params_douz.setText(_translate("MainWindow", str(params["douz"])))
            self.label_params_CHSS.setText(_translate("MainWindow", str(params["CHSS"][0])+" - "+str(params["CHSS"][1])+" уд/мин"))
            self.label_params_bazal.setText(_translate("MainWindow", str(params["bazal"])+" уд/мин"))        
        
        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(image_path, "logo.ico")))
            MainWindow.setWindowTitle(_translate("MainWindow", "STV540"))
            self.label.setText(_translate("MainWindow", app1.frame_Menu.frame_RightMenu.label._text))
            self.label_params.setText(_translate("MainWindow", "Параметры"))
            self.label_signal.setText(_translate("MainWindow", "Длительность сигнала"))
            self.label_time.setText(_translate("MainWindow", "Время"))
            self.label_accel.setText(_translate("MainWindow", "Количество акцелераций"))
            self.label_decel.setText(_translate("MainWindow", "Количество децелераций (>=30c)"))
            self.label_oscil_amplituda.setText(_translate("MainWindow", "Амплитуда осциляций"))
            self.label_date.setText(_translate("MainWindow", "Дата"))
            self.label_CHSS.setText(_translate("MainWindow", "Размах ЧСС"))
            self.label_LTV.setText(_translate("MainWindow", "LTV"))
            self.label_douz.setText(_translate("MainWindow", "Критерий Доуза-Редмана"))
            self.label_STV.setText(_translate("MainWindow", "STV"))
            self.label_srok.setText(_translate("MainWindow", "Срок, недель"))
            self.label_bazal.setText(_translate("MainWindow", "Базальный ритм"))
            self.label_fisher.setText(_translate("MainWindow", "Критерий Фишера"))
            self.label_middle.setText(_translate("MainWindow", "Значения параметров"))
            self.label_right.setText(_translate("MainWindow", "Среднее значение параметров"))
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    app1.deiconify()
    if app1.winfo_screenwidth()!=windowsize[0] and app1.winfo_screenheight()!=windowsize[1]:
        x=app1.winfo_screenwidth()/2-windowsize[0]/2
        y=app1.winfo_screenheight()/2-windowsize[1]/2
        app1.geometry(f"{windowsize[0]}x{windowsize[1]}+{int(x)}+{int(y)}")
    else:
        app1.state('zoomed')

class App(customtkinter.CTk): # окно всей программы
    def __init__(self):
        super().__init__()
        x=self.winfo_screenwidth()/2-windowsize[0]/2
        y=self.winfo_screenheight()/2-windowsize[1]/2
        self.geometry(f"{windowsize[0]}x{windowsize[1]}+{int(x)}+{int(y)}")
        self.title("STV540")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.frame_Menu=MainMenu(master=self, fg_color="White")
        self.frame_Menu.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    app = App()
    os.chdir("../")  
    app.iconbitmap(os.path.join("images", "logo.ico"))
    os.chdir("Researches")
    #app.attributes("-fullscreen", True)
    app.mainloop()