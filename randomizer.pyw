from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkinter.font
import random
import os

root = Tk()

sw = root.winfo_screenwidth()
sh = root.winfo_screenheight()

w = 800
h = 554

x = (sw/2) - (w/2)
y = (sh/2) - (h/2)

root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.title('Shuffle - Randomizer')
root.resizable(0, 0)
root.iconbitmap("img/search.ico")

def on_start(filename):
	fn = filename
	txt = os.popen('attrib +h ' + fn)
	x = txt.read()
	txt.close()

def exit_process(filename):
	fn = filename
	txt = os.popen('attrib -h ' + fn)
	x = txt.read()
	txt.close()

def on_exit():
	exit_process("male.txt")
	exit_process("female.txt")

	root.destroy()

root.protocol("WM_DELETE_WINDOW", on_exit)

on_start("male.txt")
on_start("female.txt")

bg_image = PhotoImage(file="img/bg_image.gif")

cv = Canvas(width=w, height=h, borderwidth=0, highlightthickness=0)
cv.pack(side='top', fill='both', expand='yes')
cv.create_image(0, 0, image=bg_image, anchor='nw')

with open("male.txt") as f:
	male_content = f.readlines()
male_content = [x.strip() for x in male_content]
with open("female.txt") as f:
	female_content = f.readlines()
female_content = [x.strip() for x in female_content]

both = male_content + female_content
male = male_content
female = female_content

def randomize():
	global male_content
	global female_content

	global both
	global male
	global female

	picked_g = gender.get()
	picked_n = ""

	both.sort(reverse=False)

	if picked_g == "both":
		if len(both) == 0:
			mb_reset = messagebox.askokcancel ('Reset', 'Do you want to reset the list?', icon='warning')
			if mb_reset == True:
				cv.itemconfig(lbl_name, text="Default")

				with open("male.txt") as f:
					male_content = f.readlines()
				male_content = [x.strip() for x in male_content]
				with open("female.txt") as f:
					female_content = f.readlines()
				female_content = [x.strip() for x in female_content]

				both = male_content + female_content
				male = male_content
				female = female_content

				both = male + female
				both.sort(reverse=True)

				for student in both:
					list_students.insert(0,student)
				list_recent.delete(0,END)

				checkbox_m.config(state=NORMAL)
				checkbox_f.config(state=NORMAL)

				scrollbar1.focus()
			else:
				pass
		else:
			index = random.randint(0,len(both)-1)
			picked_n = both[index]
			cv.itemconfig(lbl_name, text=str(picked_n))

			list_students.delete(both.index(picked_n))

			both.remove(picked_n)
			if picked_n in male:
				male.remove(picked_n)
			elif picked_n in female:
				female.remove(picked_n)

			if len(male) == 0:
				checkbox_m.config(state=DISABLED)
			if len(female) == 0:
				checkbox_f.config(state=DISABLED)

	elif picked_g == "male":
		if len(male) == 0:
			checkbox_m.config(state=DISABLED)
			checkbox_b.select()
		else:
			index = random.randint(0,len(male)-1)
			picked_n = male[index]
			cv.itemconfig(lbl_name, text=str(picked_n))

			list_students.delete(both.index(picked_n))

			both.remove(picked_n)
			male.remove(picked_n)

	elif picked_g == "female":
		if len(female) == 0:
			checkbox_f.config(state=DISABLED)
			checkbox_b.select()
		else:
			index = random.randint(0,len(female)-1)
			picked_n = female[index]
			cv.itemconfig(lbl_name, text=str(picked_n))

			list_students.delete(both.index(picked_n))

			both.remove(picked_n)
			female.remove(picked_n)

	if picked_n == "":
		pass
	else:
		list_recent.insert(END, picked_n)
		list_recent.see(END)

	for i in range(0, list_recent.size()-1):
		list_recent.selection_clear(i)
	list_recent.select_set(list_recent.size()-1)
	list_recent.event_generate("<<ListboxSelect>>")
	scrollbar1.focus()

label_font = tkinter.font.Font(family="Evogria", size=90)
button_font = tkinter.font.Font(family="Raleway", size=14, weight="bold")
rb_font = tkinter.font.Font(family="Montserrat", size=12)

listbox_font = tkinter.font.Font(family="SlimJoe", size=10)

lbl_name = cv.create_text(400, 280, text="Default", fill="#232323", font=label_font, anchor="center")

btn_randomize = Button(cv, text="Randomize", font=button_font, bd=0, relief=FLAT, fg="white", bg="royal blue", cursor="hand2", command=randomize)
btn_randomize.place(x=450, y=400, width=281)

def func(event=None):
	randomize()
root.bind('<Return>', func)

gender = StringVar()
checkbox_b = Radiobutton(cv, text="Both", font=rb_font, value="both", width=10, cursor="hand2", bg="#f5f5f7", anchor=W, variable=gender)
checkbox_b.place(x=450, y=451)
checkbox_b.select()
checkbox_m = Radiobutton(cv, text="Male", font=rb_font, value="male", width=10, cursor="hand2", bg="#f5f5f7", anchor=W, variable=gender)
checkbox_m.place(x=545, y=451)
checkbox_m.deselect()
checkbox_f = Radiobutton(cv, text="Female", font=rb_font, value="female", width=10, cursor="hand2", bg="#f5f5f7", anchor=W, variable=gender)
checkbox_f.place(x=640, y=451, width=90)
checkbox_f.deselect()

list_students = Listbox(cv, font=listbox_font, borderwidth=1, selectbackground="royal blue", selectmode="single", 
	highlightthickness=0)
list_students.place(x=54, y=390, height=125, width=145)

scrollbar1 = ttk.Scrollbar(cv, orient="vertical", command=list_students.yview)
scrollbar1.place(x=199, y=390, height=125)
list_students.config(yscrollcommand=scrollbar1.set)

list_recent = Listbox(cv, font=listbox_font, borderwidth=1, selectbackground="royal blue", selectmode="single", 
	highlightthickness=0)
list_recent.place(x=219, y=390, height=125, width=145)

scrollbar2 = ttk.Scrollbar(cv, orient="vertical", command=list_recent.yview)
scrollbar2.place(x=364, y=390, height=125)
list_recent.config(yscrollcommand=scrollbar2.set)

both = male + female
both.sort(reverse=True)

for student in both:
	list_students.insert(0, student)

def info_func(event):
	messagebox.showinfo("Help", "This application was created by Yvan Lowell T. Aquino \nand for further questions: you can email me at \"lowell.dycian03@gmail.com\". \n(Tips: To ensure that this application runs properly, make sure you have the \"img\" folder and both the \"male.txt\" and \"female.txt\" in the directory.)")

info_image = PhotoImage(file="img/info_help.gif")
info = Label(cv, image=info_image, borderwidth=0)
info.place(x=760, y=514)

info.bind("<Button-1>", info_func)

root.mainloop()
