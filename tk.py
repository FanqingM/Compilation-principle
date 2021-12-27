from tkinter import *
import tkinter.messagebox as messagebox
from PIL import ImageTk, Image
from Automata import Automata, nfa_convert_to_dfa
from minimizer import DFA

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

class TkDemo():
    def __init__(self):
        master = Tk()
        master.title('词法分析GUI')
        # 创建菜单栏 (Menu)
        menubar = Menu(master)
        master.config(menu=menubar)
        # 创建文件下拉菜单
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=filemenu)
        filemenu.add_command(label="新建···", command=self.newfile)
        filemenu.add_command(label="打开···", command=self.openfile)
        filemenu.add_command(label="保存", command=self.savefile)
        filemenu.add_command(label="关闭填写", command=master.quit)
        # 创建编辑下拉菜单
        editmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=editmenu)
        editmenu.add_command(label="红色", command=self.red)
        editmenu.add_command(label="蓝色", command=self.blue)
        editmenu.add_command(label="黄色", command=self.yellow)
        editmenu.add_command(label="正常", command=self.nomal)
        # 创建帮助下拉菜单
        helpmenu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='帮助', menu=helpmenu)
        helpmenu.add_command(label='操作说明', command=self.description)
        helpmenu.add_command(label='关于', command=self.about)

        textmenu = Menu(menubar,tearoff=0)
        menubar.add_cascade(label='<---请先阅读帮助栏中的说明!!!', menu=helpmenu)

        # 文字 (Label)
        title = Label(master, text='编译原理图形化展示', font='15', bg='white', fg='red')
        title.pack()

        # 问题5放在frame5中
        frame1 = Frame(master)
        frame1.pack(fill=X)
        # 问题
        label1 = Label(frame1, text='正规式转NFA')
        label1.grid(row=1, column=0)
        # 画板  (Canvas)
        self.canvas = Canvas(frame1, width=200, height=300, bg="White")
        self.canvas.grid(row=1, column=1)
        self.pattern = StringVar()
        # 图案选择按钮
        btRectangle = Button(frame1, text = "确定", command = self.displayRect)

        btClear = Button(frame1, text="清 空", command=self.clearCanvas)
        btRectangle.grid(row = 2, column = 6)
        btClear.grid(row=2, column=7)


        frame2 = Frame(master)
        frame2.pack(fill=X)
        # 问题
        label2 = Label(frame1, text='NFA转DFA以及NFA最小化')
        label2.grid(row=3, column=0)
        # 画板  (Canvas)
        self.canvas2 = Canvas(frame2, width=200, height=300, bg="White")
        self.canvas2.grid(row=3, column=1)
        self.canvas3 = Canvas(frame2, width=200, height=300, bg="White")
        self.canvas3.grid(row=3, column=3)
        self.pattern = StringVar()
        # 图案选择按钮
        btRectangle = Button(frame2, text = "确定", command = self.displayRect2)

        btClear = Button(frame2, text="清 空", command=self.clearCanvas2)
        btRectangle.grid(row = 5, column = 2)

        btClear.grid(row=5, column=3)

        btRectangle = Button(frame2, text = "确定", command = self.displayRect3)

        btClear = Button(frame2, text="清 空", command=self.clearCanvas3)
        btRectangle.grid(row = 6, column = 6)

        btClear.grid(row=6, column=7)
        master.mainloop()

  # 属性
    # 文件栏
    def newfile(self):
        self.file = open(r'test.txt', 'w')
        self.file.close()
        messagebox.showinfo('新建文件','您已成功创建个人资料文档')   # 显示对话框
    def openfile(self):
        f = open(r'test.txt', 'r')
        try:
            f_read=f.read()
            #f_read_decode=f_read.decode('utf-8')
            print(f_read)
        finally:
            f.close()
    def savefile(self):
        messagebox.showwarning('保存文件', '亲，提交即保存哦！')    # 显示对话框

    # 编辑栏
    def red(self):
        self.group['bg'] = 'red'
    def blue(self):
        self.group['bg'] = 'blue'
    def yellow(self):
        self.group['bg'] = 'yellow'
    def nomal(self):
        self.group['bg'] = 'SystemButtonFace'

    # 帮助栏
    def description(self):
        messagebox.showinfo('Description', '1.新建您的个人资料\n2.填写调查问卷\n3.点击提交 ')   # 显示对话框
    def about(self):
        messagebox.showinfo('about', '本调查问卷是python小白建文大帝用来学习TK模块的，涵盖TK模块所有GUI界面 \n                                                              ----1.0版')   # 显示对话框

    # 名字
    def getname(self):
        name = self.name.get()
        print(name)

    # 性别
    def getsex(self):
        sex = self.sex.get()
        print(sex)

    # 年龄
    def getage(self):
        print(self.age.get())

    # 语言
    def getlanguage(self):
        print(self.listbox.get(0, END))

    # 图案
    def displayRect(self):
        global image
        global im
        image = Image.open("NFA.gv.png") 
        image = image.resize((100,300)) 
        im = ImageTk.PhotoImage(image)  
        self.canvas.create_image(100,150,image = im,tags = "img")  
        # self.canvas.create_rectangle(10, 10, 190, 90, tags = "rect")
        self.pattern = '长方形'

    def displayRect2(self):
        global image2
        global im2
        nfa=Automata()
        dfa1 = DFA()

        # Add NFA States
        for i in range(0,8):
            nfa.add_state(i)

        # Set Initial and Final(s) State
        nfa.add_final_state(7)
        nfa.add_start_state([0])

        # Register Alphabet
        nfa.add_symbol('a')
        nfa.add_symbol('b')

        # Register Transitions
        nfa.add_transition(0,Automata.epsilon(),5)
        nfa.add_transition(6,Automata.epsilon(),7)
        nfa.add_transition(5,'a',5)
        nfa.add_transition(5,'b',5)
        nfa.add_transition(5,Automata.epsilon(),1)
        nfa.add_transition(1,'a',3)
        nfa.add_transition(1,'b',4)
        nfa.add_transition(3,'a',2)
        nfa.add_transition(4,'b',2)
        nfa.add_transition(2,Automata.epsilon(),6)
        nfa.add_transition(6,'a',6)
        nfa.add_transition(6,'b',6)


        global dfa
        dfa = nfa_convert_to_dfa(nfa)

        # dfa.print()
        dfa.draw()
        image2 = Image.open("NFATODFA.png") 
        image2 = image2.resize((100,300)) 
        im2 = ImageTk.PhotoImage(image2)  
        self.canvas2.create_image(100,150,image = im2,tags = "img")  
        # self.canvas.create_rectangle(10, 10, 190, 90, tags = "rect")
        self.pattern = '长方形'

    def displayRect3(self):
        global image3
        global im3

        from Exp2NFA import ExpToNFA

        entity = ExpToNFA(1)
        entity.convert('(a|b)*cba')

        from Automata import generateNFA

        nfa = generateNFA(entity.transitions)
        nfa.draw()

        image3 = Image.open("DFA.png") 
        image3 = image3.resize((100,300)) 
        im3 = ImageTk.PhotoImage(image3)  
        self.canvas3.create_image(100,150,image = im3,tags = "img")  
        # self.canvas.create_rectangle(10, 10, 190, 90, tags = "rect")
        self.pattern = '长方形'
  
    def clearCanvas(self):
        self.canvas.delete("img", "oval", "arc", "polygon", "line", "string")
    def clearCanvas2(self):
        self.canvas2.delete("img", "oval", "arc", "polygon", "line", "string")
    def clearCanvas3(self):
        self.canvas3.delete("img", "oval", "arc", "polygon", "line", "string")

    # 球星
    def getstar(self):
        print(self.listbox2.get(ACTIVE))

    # 数字
    def getnumber(self):
        print(self.number.get())

    # 同意
    def getagree(self):
        print(self.agree.get())

    # 提交
    def allsubmit(self):
        with open(r'test.txt', 'w') as f:
            f.write('您的花名是：')
            f.write(self.name.get())
            f.write('\n您的性别为:')
            f.write(self.sex.get())
            f.write('\n您的年龄是：')
            f.write(str(self.age.get()))
            f.write('\n您会这么多编程语言：')
            for i in self.listbox.get(0, END):
                f.write(i)
                f.write(" ,")
            f.write('\n您喜欢的图案是：')
            f.write(self.pattern)
            f.write('\n您喜欢的球星号为：')
            f.write(self.listbox2.get(ACTIVE))
            f.write('\n您喜欢的数字为：')
            f.write(self.number.get())
            f.write('\n')
            f.write(self.agree.get())
            f.write('本调查问卷的真实性')
        messagebox.showinfo('Success', '恭喜您已成功提交 ')   # 显示对话框
TkDemo()


