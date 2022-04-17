#用于完善编译原理实验二，加入first and follow集合
from tkinter import *
from myfunction import *
class MY_GUI():
    def __init__(self,init_window_name):
        self.init_window_name = init_window_name
    def set_init_window(self):
        self.init_window_name.title("LL(1)文法")
        self.init_window_name.geometry('1200x570+10+10')
        self.input_label = Label(self.init_window_name, text="请输入句子串")
        self.input_label.grid(row=0, column=0)
        self.output_label = Label(self.init_window_name, text="输出结果")
        self.output_label.grid(row=3, column=0)
        self.init_data_Text = Text(self.init_window_name, width=35, height=1)
        self.init_data_Text.grid(row=1, column=0, rowspan=1, columnspan=1)
        self.result_data_Text = Text(self.init_window_name, width=150, height=35)
        self.result_data_Text.grid(row=30, column=0, rowspan=1, columnspan=1)
        self.button = Button(self.init_window_name, text="LL(1)", bg="lightblue", width=10,command=self.begin_with)
        self.button.grid(row=1, column=10)
    def use_function(self,src):
        self.result_data_Text.insert('end', src)
        self.result_data_Text.insert(INSERT, '\n')
    def begin_with(self):  # 进行输入，lol终于写完了
        read_text()
        pro_deal()
        get_first()
        get_follow()
        get_analysis()

        # print(FIRST)    #first集合
        # print(FOLLOW)   #follow集合
        # print(grammer) #语法
        # print(vt)  # 终结符号
        # print(vn)  # 非终结符号
        # print(analysis) #转换表

        sentence = src = self.init_data_Text.get(1.0, END).strip().replace("\n", "")
        input_stack = Stack('#')  # 存储输入串的栈
        ana_stack = Stack('#')  # 建立分析栈
        product_stack = Stack()  # 建立存储所用产生式的栈
        ana_stack.push(vn[0])
        act_stack = Stack()  # 建立动作栈
        for i in list(reversed(sentence)):
            input_stack.push(i)
        act_stack.push('初始化')
        out_put = "{0:<10}\t{1:<25}\t{2:<30}\t{3:<40}\t{4:<20}"
        self.use_function(out_put.format("步骤", "分析栈", "剩余输入串", "所用产生式", "行为", chr(12288)))
        step = 0
        try:
            while (not ana_stack.isempty()):
                self.use_function(
                    out_put.format(step, str(ana_stack.show()), str(input_stack.show()), str(product_stack.show()),
                                   str(act_stack.show()), chr(12288)))
                step = step + 1
                product_stack.clear()
                act_stack.clear()
                if ana_stack.show_last_one() == input_stack.show_last_one():
                    ana_stack.pop()
                    input_stack.pop()
                    act_stack.push('POP')
                elif ana_stack.show_last_one() == 'e':
                    ana_stack.pop()
                    act_stack.push('POP')
                elif analysis[ana_stack.show_last_one()][input_stack.show_last_one()]:
                    med = ana_stack.pop()
                    act_stack.push('POP')
                    for i in list(reversed(list(analysis[med][input_stack.show_last_one()])[0])):
                        ana_stack.push(i)
                    product_stack.push("{0}->{1}".format(med, str(list(analysis[med][input_stack.show_last_one()])[0])))
                    act_stack.push('PUSH({0})'.format(str(list(analysis[med][input_stack.show_last_one()])[0])))
                else:
                    self.use_function('ERROR')
                    break
        except KeyError:
            self.use_function('Error,你输入错误句子')

def gui_start():
    init_window = Tk()
    xu = MY_GUI(init_window)
    xu.set_init_window()
    init_window.mainloop()
if __name__=="__main__":
    gui_start()
