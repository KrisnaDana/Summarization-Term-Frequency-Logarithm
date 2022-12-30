from NLP import break_into_token, stop_list, stemming
from Summary import Summary
import customtkinter as ctk
from tkinter import filedialog as fd
from tkinter import IntVar
from tkinter import StringVar
from tkinter import LEFT


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry = "500x500"
        self.title("Stemming Demonstration")
        self.protocol("WM_DELETE_WINDOW", self.on_close) #when WM_DELETE_WINDOW, call self.on_close()
        self.write_file = False
        self.result = None

        # =========== making 2 frames ==========
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = ctk.CTkFrame(master=self, width=200, corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = ctk.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)


        self.frame_left.grid_rowconfigure(0, minsize=20) # going to the top
        self.frame_left.grid_rowconfigure(5, weight=5) # giving it some space so that the next row will be on the bottom
        self.frame_left.grid_rowconfigure(8, minsize=35) # spacing using minsize
        # ========== configuring content =======

        # =========== left frame ==============
        self.input_label = ctk.CTkLabel(master=self.frame_left, text="Input Text File", text_font=("Roboto Medium", 16))
        self.input_label.grid(row=1, column=0, pady=15, padx=15, sticky="n")

        self.input_button = ctk.CTkButton(master=self.frame_left, text="Input File", command=self.select_file)
        self.input_button.grid(row=2, column=0, pady=15, padx=15, sticky="n")

        self.checkbox_var = IntVar()
        self.chk_output_new = ctk.CTkCheckBox(master=self.frame_left, text="Write to new file", offvalue=0, onvalue=1, variable=self.checkbox_var)
        self.chk_output_new.grid(row=8, column=0, pady=10, padx=20, sticky="s")

        # ========== right frame ==========
        # self.chk_show_process = ctk.CTkCheckBox(master=self.frame_right, text="Show Detailed Process")
        # self.chk_show_process.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        self.start_stem_btn = ctk.CTkButton(master=self.frame_left, text="Start Process", command=self.stem)
        self.start_stem_btn.grid(row=3, column=0, padx=15, pady=15, sticky="n")

        self.text_result = StringVar()
        self.input_label = ctk.CTkLabel(master=self.frame_right, textvariable=self.text_result, text_font=("Roboto Medium", 12), anchor="w", justify=LEFT)
        self.input_label.grid(row=1, column=0, pady=15, padx=15, sticky="w")

    def select_file(self):
        file_type = (("text files", "*.txt"), ("all files", "*.*"))
        path_to_file = fd.askopenfilename(title="Select a text file", filetypes=file_type)            
        try:
            self.text_file = open(path_to_file, 'r', encoding='utf-8').read()
        except:
            self.text_file = ""

    
    def stem(self):
        self.summary = Summary(self.text_file)

        # self.result = stemming(stop_list(break_into_token(self.text_file)))
        # result_temp = ''''''
        # count = 0
        # for rs_temp in self.result:
        #     if count % 20 == 0 and count != 0:
        #         result_temp += ' '+rs_temp+'\n'
        #     else:
        #         result_temp += ' '+rs_temp
        #     count+=1
        # self.text_result.set(result_temp)

        self.result = self.summary.get_summary()
        result_temp = ''''''
        count = 0
        for rs_temp in self.result:
            if count % 200 == 0 and count != 0:
                result_temp += ''+rs_temp+'-\n'
            else:
                result_temp += ''+rs_temp
            count+=1
        self.text_result.set(result_temp)

        if self.checkbox_var.get() == 1:
            if (self.result != None):
                with open("result.txt", 'w') as f:
                    f.write(f"{self.result} ")
        

    def on_close(self):
        self.destroy()

app = App()
app.mainloop()