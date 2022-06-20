import time
from tkinter import *
import re
import yadict
import json
import tkinter as tk



class TranslateBtn(Button):
    '''
    Tkinter button that call get_lang_pair from yadict
 that returns available language pairs
    '''
    def __init__(self):
        super().__init__(frame_btn, bg="#66CDAA", fg='#ffffff', activebackground='#ACFDF8',
                         relief=FLAT, borderwidth=1, text="TRANSLATE", command=self.select_lang_pair)
        self.lang_pair = StringVar()
        self.num_of_translated = IntVar()
        self.num_of_translated.set(100)
        try:
            with open("dictapi.txt", "r") as f:
                self.api_key = f.read()
        except:
            pass

    def select_lang_pair(self):
        btn_analyze['state'] = DISABLED
        btn_merge['state'] = DISABLED
        btn_help['state'] = DISABLED
        btn_get_unknown_words['state'] = DISABLED
        btn_translate["state"] = DISABLED

        lbl_run_status_var.set('Wait till completed')
        lbl_run_status.update()

        lbl_status_var.set("Translating...")
        lbl_status.update()

        lang_pairs_list = json.loads(yadict.get_lang_pair(self.api_key).text)
        self.lang_selector = Toplevel()

        self.lang_pair.set("en-ru")
        col=0
        r=0
        for i in lang_pairs_list:
            if col != 10:
                Radiobutton(self.lang_selector,
                            variable=self.lang_pair,
                            text=i,
                            command=lambda: self.translate(i),
                            value=i).grid(column=col, row=r, sticky=W)
                col += 1
            else:
                r += 1
                col = 0

    def translate(self, lang_pair):
        self.lang_selector.destroy()
        print(self.lang_pair.get())
        with open("unknown_words.txt", "r", encoding="utf8") as f:
            words = f.read().splitlines()
        
        self.translated_words = list()
        try:
            for ind, i in enumerate(words[:self.num_of_translated.get()]):
                i = i.split(",")
                print(i)
                yadict.translate(i[1], self.lang_pair.get(),
                                 self.translated_words, self.api_key)
                lbl_status_var.set(f"Translating {ind+1} of {self.num_of_translated.get()}")
                lbl_status.update()
        except IndexError:
            pass
            
        with open("translated words.txt", "w", encoding="utf8") as f:
            f.writelines(self.translated_words)

        window_output = 'Completed'
        lbl_run_status_var.set(window_output)
        lbl_run_status.update()

        lbl_status_var.set(" ")
        lbl_status.update()

        btn_analyze['state'] = NORMAL
        btn_merge['state'] = NORMAL
        btn_help['state'] = NORMAL
        btn_get_unknown_words['state'] = NORMAL
        btn_translate["state"] = NORMAL

# opens a window with the text from help.txt
def get_info():
    try:
        with open("help.txt", "r", encoding="utf8") as f:
            help_text=f.read()
        window_help = tk.Tk()
        window_help.config(bg='White')
        window_help.title('Help')
        lbl_help = Label(window_help, text=help_text, bg='White', justify=LEFT, fg='Black')
        lbl_help.pack()
    except:
        window_help = tk.Tk()
        window_help.title('Error')
        lbl_help = Label(window_help, text="help.txt doesn't exist or something",justify=LEFT)
        lbl_help.pack()


# change a string to lower case
def to_lowercase(text):
    text_lower = str()
    for letter in text:
        text_lower += letter.lower()
    return text_lower


# change the text to lower case with to_lowercase and split to single word list
def split_text(text):
    delim = [' ', '\,', '\.', '\?', '\!', '\¿', '\¡', '\%', '\:', '\;', '\'', '\'', '\"', '\«', '\»', '\-', '\—', '\n', '\)', '\(',
             '\*', '\<', '\>', '\=', '\–', '\+', '\|', '\&', '\“', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    text = to_lowercase(text)

    all_words_list_raw = re.split("|".join(item for item in delim), text)
    all_words_list = []
    for item in all_words_list_raw:
        if item != '' and len(str(item)) > 2:
            all_words_list.append(item)
        else:
            continue

    return all_words_list


# making the tuple (count,word) from a given list
def group_same_words(list):
    dict = {}
    for i in list:
        try:
            count = dict.get(i)
            count += 1
            dict[i] = count
        except:
            dict[i] = 1
    listword = []
    for key in dict:
        listword.append((dict.get(key), key))
    listword.sort(key=lambda i:i[0], reverse=True)

    # debug
    # total_words=0
    # for i in listword:
    #     total_words += i[0]
    #debug
    # print(total_words,  "in grouped")
    return listword


# merge output_new and base from files to one file
def merge():
    with open("base.txt", 'r', encoding="utf8") as file:
        base_list = [item for item in file.read().split("\n")]
    count_old = []
    word_old = []
    for item in base_list:
        try:
            count_old.append(int(item.split(",")[0]))
            word_old.append(item.split(",")[1])
        except:
            # print("wrong line")
            continue
    # debug
    # print(len(base_list), " <= len of base list")
    # print(len(count_old), " count", len(word_old), " words")

    with open("output-new.txt", 'r', encoding="utf8") as file:
        output_new_list = [item for item in file.read().split("\n")]
    count_new = []
    word_new = []
    for item in output_new_list:
        try:
            count_new.append(int(item.split(",")[0]))
            word_new.append(item.split(",")[1])
        except:
            # print("empty line")
            continue
    # debug
    # print(len(output_new_list), " <= len of output_new_list")
    # print(len(count_new), " count new len", len(word_new), " words new len")

    base_dict = dict()
    for word in word_old:
        try:
            base_dict[word] = count_old[word_old.index(word)]
        except:
            # print("base_dict throws an exception")
            continue
    # debug
    # print(base_dict)

    new_dict = dict()
    for word in word_new:
        try:
            new_dict[word] = count_new[word_new.index(word)]
        except:
            # print("new_dict throws an exception")
            continue

    #debug
    # print(new_dict)

    for key in new_dict:
        try:
            total_key_count = int(base_dict.get(key)) + int(new_dict.get(key))
            base_dict[key]=total_key_count
        except:
            base_dict[key] = new_dict.get(key)
            continue

    list_to_write = list()
    for key in base_dict:
        list_to_write.append((base_dict.get(key), key))

    list_to_write.sort(key=lambda i:i[0], reverse=True)

    # debug
    # print(len(base_dict), " len base_dict to write")

    with open("base.txt", "w", encoding="utf8") as file:
        for i in list_to_write:
            file.writelines(f"{i[0]},{i[1]}\n")


# run merge by clicking merge button
def merge_click():
    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED
    btn_get_unknown_words['state'] = DISABLED
    btn_translate["state"] = DISABLED

    lbl_status_var.set('Merging base and output_new')
    lbl_status.update()

    lbl_run_status_var.set('Wait till completed')
    lbl_run_status.update()

    try:
        merge()
    except:
        window_help = tk.Tk()
        window_help.title('Error')
        lbl_help = Label(window_help, text="Something is wrong", justify=LEFT)
        lbl_help.pack()

    window_output = 'Completed'
    lbl_run_status_var.set(window_output)
    lbl_run_status.update()

    lbl_status_var.set(' ')
    lbl_status.update()
    time.sleep(0.5)

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL
    btn_get_unknown_words['state'] = NORMAL
    btn_translate["state"] = NORMAL


# takes list of known words and returns list of unknown words
def make_list_unknown_words():

    with open("base.txt", 'r', encoding="utf8") as file:
        base_list = [item for item in file.read().split("\n")]
    count_old = []
    word_old = []
    for item in base_list:
        try:
            count_old.append(item.split(",")[0])
            word_old.append(item.split(",")[1])
        except:
            # print("wrong line")
            continue
    # debug
    # print(len(base_list), " <= len of base list")
    # print(len(count_old), " count", len(word_old), " words")

    with open("known_words.txt", "r", encoding="utf8") as file:
        known_words = [item for item in file.read().split("\n")]

    base_dict = dict()
    for word in word_old:
        try:
            base_dict[word] = count_old[word_old.index(word)]
        except:
            # print("base_dict throws an exception")
            continue
    # debug
    #print(base_dict)
    unknown_words = list()
    for key in base_dict:
        if key not in known_words:
            unknown_words.append((base_dict.get(key),key))

    with open("unknown_words.txt", "w", encoding="utf8") as file:
        for i in unknown_words:
            file.writelines(f"{i[0]},{i[1]}\n")


def make_list_unknown_words_clicked():
    btn_analyze['state'] = DISABLED
    btn_merge['state'] = DISABLED
    btn_help['state'] = DISABLED
    btn_get_unknown_words['state'] = DISABLED
    btn_translate["state"] = DISABLED

    lbl_run_status_var.set('Wait till completed')
    lbl_run_status.update()

    lbl_status_var.set("Searching for unknown words...")
    lbl_status.update()

    time.sleep(0.5)
    try:
        make_list_unknown_words()
    except Exception as e:
        window_help = tk.Tk()
        window_help.title('Error')
        lbl_help = Label(window_help, text=f"Something is wrong. Check help.txt, each file must exist\n{e}", justify=LEFT)
        lbl_help.pack()

    window_output = 'Completed'
    lbl_run_status_var.set(window_output)
    lbl_run_status.update()

    lbl_status_var.set(" ")
    lbl_status.update()

    btn_analyze['state'] = NORMAL
    btn_merge['state'] = NORMAL
    btn_help['state'] = NORMAL
    btn_get_unknown_words['state'] = NORMAL
    btn_translate["state"] = NORMAL


# starts the process of the text analysis
def run_analyze():
    try:
        lbl_warning_var.set('Wait till completed')
        lbl_warning.update()

        btn_analyze['state'] = DISABLED
        btn_merge['state'] = DISABLED
        btn_help['state'] = DISABLED
        btn_get_unknown_words['state'] = DISABLED

        with open('input.txt', 'r', encoding='utf8') as f:
            input_text = f.read()
        all_words_list = split_text(input_text)
        input_text_length = len(input_text)
        lbl_warning_var.set(f"The text length is {input_text_length} characters")
        lbl_warning.update()


        lbl_run_status_var.set("1 of 3 is completed")
        lbl_run_status.update()

        count_word_list_of_tuples = group_same_words(all_words_list)
        lbl_run_status_var.set('2 of 3 is completed')
        lbl_run_status.update()

        with open('output-new.txt', 'w', encoding='utf8') as f:
            for key in count_word_list_of_tuples:
                f.write('{},{}\n'.format(key[0],key[1]))

            # debug
            # print("last item in output_new is ",count_word_list_of_tuples[-1])



        lbl_run_status_var.set('Completed. Check base.txt')
        lbl_run_status.update()
        lbl_status_var.set('')
        lbl_status.update()

        lbl_warning_var.set("Build your own vocabulary list \nto make language learning easier")
        lbl_warning.update()

        btn_analyze['state'] = NORMAL
        btn_merge['state'] = NORMAL
        btn_help['state'] = NORMAL
        btn_get_unknown_words['state'] = NORMAL
    except Exception as e:
        window_help = tk.Tk()
        window_help.title('Error')
        lbl_help = Label(window_help, text=f"Something is wrong. Check help.txt, each file must exist\n{e}",justify=LEFT)
        lbl_help.pack()

if __name__ == "__main__":
    try:
        root = Tk()
        root.title("Vocabuilder v. 3.0 by Cafe p\'Aguantarme")
        root.config(bg='White')
        root.geometry("200x210")

        root.iconbitmap('logo.ico')
        lbl_warning_var = StringVar()
        lbl_status_var = StringVar()
        lbl_run_status_var = StringVar()

        lbl_warning_var.set('Build your own vocabulary list \nto make language learning easier')
        lbl_warning = Label(root, bg="White", fg='#228987', textvariable=lbl_warning_var)
        lbl_warning.pack(side=BOTTOM, fill=X)
        lbl_status = Label(root, bg="White", fg='#228987', textvariable=lbl_status_var)
        lbl_status.pack(side=BOTTOM, fill=X)
        lbl_run_status = Label(root, bg="White", fg='#228987', textvariable=lbl_run_status_var)
        lbl_run_status.pack(side=BOTTOM, fill=X)

        frame_btn = Frame(root, bg="#66CDAA", )
        frame_btn.pack(side=TOP, fill=X)
        btn_help = Button(frame_btn, bg="#66CDAA", text='HELP', fg='#ffffff', activebackground='#ACFDF8',
                          command=get_info, relief=FLAT, borderwidth=1)
        btn_help.pack(fill=X)
        btn_analyze = Button(frame_btn, text='ANALYZE', bg="#66CDAA", fg='#ffffff', activebackground='#ACFDF8',
                             command=lambda: run_analyze(), relief=FLAT, borderwidth=1)
        btn_analyze.pack(fill=X)
        btn_merge = Button(frame_btn, bg="#66CDAA", fg='#ffffff', activebackground='#ACFDF8',
                           text="MERGE", relief=FLAT, borderwidth=1, command=lambda: merge_click())
        btn_merge.pack(fill=X)
        btn_get_unknown_words = Button(frame_btn, bg="#66CDAA", fg='#ffffff', activebackground='#ACFDF8',
                           text="NEW WORDS", relief=FLAT, borderwidth=1, command=lambda: make_list_unknown_words_clicked())
        btn_get_unknown_words.pack(fill=X)

        btn_translate = TranslateBtn()
        btn_translate.pack(fill=X)

        root.resizable(False, False)
        root.mainloop()
    except Exception as e:
        
        window_help = tk.Tk()
        window_help.title('Error')
        lbl_help = Label(window_help, text=f"Something is wrong\n{e}", justify=LEFT)
        lbl_help.pack()





