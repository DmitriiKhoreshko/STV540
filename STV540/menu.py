import customtkinter
from customtkinter import filedialog
from tkcalendar import DateEntry
from datetime import datetime
from WorkSpaceFile import WorkSpace
import os
from PIL import Image
import re
import shutil
import json
import copy

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

# Глобальные переменные 
windowsize=[1600,900]     
globalfolderpage=19
globalresearchespage=19
foldersfilter="filter-off"
researchesfilter="filter-off"
pagetype="folders"
compare=0
comparelist=[]

class MainMenu(customtkinter.CTkFrame): # главное меню
    def __init__(self, master, app,**kwargs):
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
                                def res_btn():
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

                class dialog_filter(customtkinter.CTkToplevel): # подтверждение удаления папки
                    class FolderSettings(customtkinter.CTkFrame): # фрейм сравнения исследований
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
                    class ResearchesSettings(customtkinter.CTkFrame): # фрейм сравнения исследований
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