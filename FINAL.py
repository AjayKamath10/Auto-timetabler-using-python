#Importing dependencies
from tkinter import *
import random as r
import mysql.connector as sql
from prettytable import PrettyTable
import webbrowser as wb

#Initializing variables required for further use
tch_count = 1
tch_names = dict()
subjects = dict()
timetable = dict()
classes = dict()
days = ['MON' , 'TUE' , 'WED' , 'THU' , 'FRI']
default_tch_names = ['Bill Gates' , 'Steve Jobs', 'Sundar Pichhai', 'Satya Nadella', 'Elon Musk', 'Kiran Mazumdar', 'Larry Page',
                     'Henry Ford' , 'Narayana Murthy', 'Walt Disney' , 'PT Usha', 'Indra Nooyi']#default_entry
max_freq_sub = 2#maximum number of times a subject can be taught per day
grade_count = 0#used in screen5
classcount = 0#used in screen6
bgc = '#87ceeb' #background colour
bbgc = '#e6e600' #button background colour
default_sub = [0,1,2,3,4,0,1,2,3,4,5,6]#default_entry - default selection of subjects
default_sub_index = 0#default_entry - index required for default selection of subjects

#Connection to MySQL
mydb = sql.connect(host = 'localhost',user = 'root',password = 'TIGER')
def sq(Input):# function to connect to MySQL
    global mydb
    mycur = mydb.cursor()
    mycur.execute(Input)
    mydb.commit()

#Pre requisites to start a fresh project in a new database
sq("DROP DATABASE IF EXISTS TIMETABLE")
sq("CREATE DATABASE TIMETABLE")
sq("USE TIMETABLE")

##Create empty table for teachers' data
sq("CREATE TABLE teachers (ID int(3) PRIMARY KEY, tchname varchar(30) UNIQUE)")

##Make the main window
root1 =  Tk('window1')
adjlabel = Label(root1 , text = '       ', bg = bgc)
adjlabel.grid(row = 0 , column = 0, padx = 250 , pady = 100)
root = Frame(root1, highlightbackground="black", highlightthickness=1)
root.grid(row = 1 , column = 1)

##Align the window to the centre of screen
windowWidth = root.winfo_reqwidth()# Gets the requested values of the height and width
windowHeight = root.winfo_reqheight()
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)# Gets both half the screen width/height and window width/height
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2)
##root1.geometry("+{}+{}".format(positionRight, positionDown))    # Positions the window in the center of the page
root1.geometry('1920x1080')
##Configuring the window
root.configure(background = bgc)
root1.configure(background = bgc)

##Validation functions
#If entry is repeated
def repeated_entry(phrase):
    sub_popup = Tk()
    sub_popup.geometry("+{}+{}".format(positionRight, positionDown))
    sub_popup.title("Error!!!")
    sub_popup.config(bg = 'red')
    local_label = Label(sub_popup , text = 'That ' + phrase + ' has already been entered!', bg = '#FF3333', font=("Times New Roman", 16))
    local_label.grid(row = 0 , column = 0)
    local_button = Button(sub_popup , text = '  OK  ', command = lambda: sub_popup.destroy(), bd = 3, bg = 'yellow', relief = 'ridge')
    local_button.grid(row = 1 , column = 0 , rowspan = 2 , padx = 10)
    return;

#If entry is empty or invalid
def empty_entry(phrase):
    local_popup = Tk()
    local_popup.geometry("+{}+{}".format(positionRight, positionDown))
    local_popup.title("Error!!!")
    local_popup.config(bg = 'red')
    local_label = Label(local_popup , text = 'Please enter only ' + phrase + '!', bg = '#FF3333', font=("Times New Roman", 16))
    local_label.grid(row = 0 , column = 0)
    local_button = Button(local_popup , text = '  OK  ', command = lambda: local_popup.destroy(),bd = 3, bg = 'yellow', relief = 'ridge')
    local_button.grid(row = 1 , column = 0 , rowspan = 2 , padx = 10)
    return;

#If selection is invalid or empty
def empty_selection(phrase):
    local_popup = Tk()
    local_popup.geometry("+{}+{}".format(positionRight, positionDown))
    local_popup.title("Error!!!")
    local_popup.config(bg = 'red')
    local_label = Label(local_popup , text = 'Please choose at least one ' + phrase + '!', bg = '#FF3333', font=("Times New Roman", 16))
    local_label.grid(row = 0 , column = 0)
    local_button = Button(local_popup , text = '  OK  ', command = lambda: local_popup.destroy(),bd = 3, bg = 'yellow', relief = 'ridge')
    local_button.grid(row = 1 , column = 0 , rowspan = 2 , padx = 10)
    return;

'''----------------------------------------------------------------SCREEN 1----------------------------------------------------------------------------------------------------------------------'''

##First screen - obtains number of grades, periods, teachers from the user
def screen1():
    global label1 , label2 , label3 , entry1 , entry2 , entry3 , button1
    label1 = Label(root,text = 'Enter number of grades: ', bg = bgc)
    label1.grid(row = 1 , column = 0)
    label2 = Label(root,text = 'Enter number of periods: ', bg = bgc)
    label2.grid(row = 2 , column = 0)
    label3 = Label(root,text = 'Enter number of teachers: ', bg = bgc)
    label3.grid(row = 3, column = 0)
    entry1 = Entry(root)
    entry1.insert(0 , '2')#default_entry
    entry1.grid(row = 1 , column = 1)
    entry2 = Entry(root)
    entry2.insert(0, '9')#default_entry
    entry2.grid(row = 2 , column = 1)
    entry3 = Entry(root)
    entry3.insert(0, '12')#default_entry
    entry3.grid(row = 3 , column = 1)
    button1 = Button(root, text = "Submit", command = lambda : submit1(), bd = 3, bg = bbgc, relief = 'ridge')#submit button
    button1.grid(row = 4 , columnspan = 5 )
    root.mainloop()
    return;

##submitbutton1
def submit1():
    global no_grades , no_perds , no_tchs , listbox2
    try:#Checks if only integers are entered
        no_grades = int(entry1.get())
        no_perds = int(entry2.get())
        no_tchs = int(entry3.get())
        if no_grades > 0 and no_perds > 0 and no_tchs > 0:#Checks if only positive integers are entered
            for i in [label1 , label2, label3, entry1,entry2,entry3,button1]:
                i.destroy()
            screen4_pre_requisites()#Screen is set up with widgets required for screen 4
        else:#In case of invalid entry
            empty_entry('positive integers')            
    except ValueError:#In case of invalid entry
        empty_entry('positive integers')
    return;
    

'''-----------------------------------------------------------------SCREEN 2--------------------------------------------------------------------------------------------------------------------------------------------------------'''

#Creates widgets required for screen 2
def screen2_pre_requisites():
    global listbox1 , listbox4 , label13 , label15 , scrollbar3 , scrollbar1
    scrollbar1 = Scrollbar(root)
    scrollbar1.grid(row  = 3 , column = 2, sticky = 'ns', pady = 20)
    listbox1 = Listbox(root, yscrollcommand = scrollbar1.set)
    listbox1.grid(row = 3 , column = 1 , pady = 20)
    scrollbar1.config(command = listbox1.yview)
    label15 = Label(root,text = "Teachers entered :-", bg = bgc)  
    label15.grid(row = 3 , column = 0)
    scrollbar3 = Scrollbar(root)
    scrollbar3.grid(row = 2 , column = 2 , sticky = 'ns')
    listbox4 = Listbox(root,selectmode = 'multiple' , yscrollcommand = scrollbar3.set)#Listbox containing the names of teachers entered by user
    listbox4.grid(row = 2 , column = 1)
    scrollbar3.config(command = listbox4.yview)
    label13 = Label(root , text = 'Select subjects :-', bg = bgc)
    label13.grid(row = 2 , column = 0)
    for i in range(len(subjects.keys())):#Listbox containing names of all subjects
        listbox4.insert(i , list(subjects.keys())[i])
    screen2()
    return;

##second screen - asks user for names of teachers
def screen2():
    global label4 , entry4 , button2 , listbox1 , listbox4
    label4 = Label(root , text = 'Enter name of teacher having ID '  + str(tch_count), bg = bgc)
    label4.grid(row = 1 , column = 0 , pady = 10)
    entry4 = Entry(root)
    default_entry_tch()#default_entry
    entry4.grid(row = 1 , column = 1 , pady = 10)
    button2 = Button(root , text = "Submit" , command = lambda : submit2(), bd = 3, bg = bbgc, relief = 'ridge')#To store the name entered
    button2.grid(row = 2 , column = 3)    
    return;

##To store the name of teacher entered by the user
def submit2():
    global subjects , listbox1 , label4 , entry4 , button2 , tch_count , tch_names , listbox4
    name = entry4.get()
    if name in tch_names.values():#Checks for invalid entry
        repeated_entry('name')
    elif name == '' or name.isspace():#Checks for invalid entry
        empty_entry("teacher's names")
    elif len(listbox4.curselection()) == 0:#Checks for invalid entry
        empty_selection('subject name')
    else:
        entry4.destroy()
        label4.destroy()
        button2.destroy()
        tch_names[tch_count] = name.replace(' ','_')#Adds the name of teacher with teachers ID as the key into the tch_names dictionary
        #spaces as replaced by _ to make it a valid MySQL tablename 
        for i in listbox4.curselection():#The selected values are the subjects taught by that teacher
            
            ##Add the name of teacher into the list held by the subjects' name that the teacher teaches as the key in the subjects dictionary 
            subjects[listbox4.get(i)] = subjects[listbox4.get(i)] + [name]
        listbox4.select_clear(0,listbox4.size()-1)
        listbox1.insert(tch_count,name+'(' + str(tch_count)+')')#Adds the ID and name of the teacher into listbox1
        tch_count += 1
        if tch_count <= no_tchs:#If more teachers are to be entered
            screen2()
        else:#If details about all teachers have been entered - clear all widgets and proceed to next screen 
            listbox4.destroy()
            scrollbar3.destroy()
            label15.destroy()
            label13.destroy()
            screen3()
        return;

##To add some names of teachers automatically
def default_entry_tch():
    global default_sub_index
    entry4.insert(0, default_tch_names[tch_count - 1])
    listbox4.selection_set(default_sub[default_sub_index])#default_entry
    default_sub_index += 1
    return;

    
'''--------------------------------------------------------------SCREEN 3----------------------------------------------------------------------------------------------------------------------------------------------------------'''


##Third screen - allows user to edit the teachers entered 
def screen3():
    global listbox1 , button3 , button4 , button7
    #listbox1 and listbox3 already exist in 3rd row
    button3 = Button(root,text = "Delete selected name", command = lambda : delete1(), bd = 3, bg = bbgc, relief = 'ridge')
    button3.grid(row = 4, column = 0)
    button4 = Button(root,text = "Add name",command = lambda : add1(), bd = 3, bg = bbgc, relief = 'ridge')
    button4.grid(row = 4, column = 1)
    button7 = Button(root,text = "OK" , command = lambda : ok1(), bd = 3, bg = bbgc, relief = 'ridge')
    button7.grid(row = 4 , column = 5)
    return;

##Delete selected teacher's name
def delete1():
    global listbox1 , tch_names , subjects
    cursor1 = listbox1.curselection()[0]
    #To obtain name ID of a teacher from a string containing the name with ID in brackets
    name = str((listbox1.get(cursor1).split('('))[0])
    loc_var = int((listbox1.get(cursor1).split('('))[1][:-1])
    
    for i in subjects.keys():
        if name in subjects[i]:
            subjects[i].remove(name)
    del tch_names[loc_var]
    listbox1.delete(cursor1)
    return;

##popup screen for adding a teacher name 
def add1():
    global popup1
    try:
        popup1.deiconify()#try to bring the window to the front if add subject button already clicked          
    except:
        global tch_names , entry5 , label5 , entry6 , label6 , button5 , submit3 , listbox5, scrollbar4
        popup1 = Tk()
        popup1.config(bg = bgc)
        popup1.title("Add name")
        label5 = Label(popup1 , text = "Enter teacher ID : ", bg = bgc)
        entry5 = Entry(popup1)
        label6 = Label(popup1 , text = "Enter name : ", bg = bgc)
        entry6 =Entry(popup1)
        button5 = Button(popup1 , text = "Submit" , command = lambda : submit3(), bd = 3, bg = bbgc, relief = 'ridge')#To store the teacher ID and name entered by user
        label14 = Label(popup1 , text = 'Select subjects:-', bg = bgc)
        scrollbar4 = Scrollbar(popup1)
        scrollbar4.grid(row = 2 , column = 2)
        listbox5 = Listbox(popup1, selectmode = 'multiple', yscrollcommand = scrollbar4.set)
        listbox5.grid(row = 2 , column = 1)
        scrollbar4.config(command = listbox5.yview)
        for i in range(len(subjects.keys())):
            listbox5.insert(i , list(subjects.keys())[i])
        label5.grid(row = 0 , column = 0)
        entry5.grid(row = 0 , column = 1)
        label6.grid(row = 1 , column = 0)
        entry6.grid(row = 1 , column = 1)
        button5.grid(row = 3 , column = 1)
        label14.grid(row = 2 , column = 0)
        popup1.mainloop() 
    return;

##Stores the teacher ID , name entered by user
def submit3():
    global tch_names , listbox1 , popup1 , entry5 , label5 , button5 , label6 , entry6, listbox4
    #Check for invalid entry:
    if len(listbox5.curselection()) == 0:#if subject selections not done
        empty_selection('subject')
    elif entry5.get() == '' or not entry5.get().isdigit():#if numbers not entered in Entry5
        empty_entry('numbers as ID')
    elif entry6.get() == '' or entry6.get().isspace():#if Entry6 left empty or only whitespace entered
        empty_entry("teacher's name")
    elif (int(entry5.get()) in tch_names.keys()) or (entry6.get().replace(' ','_') in tch_names.values()):#if ID or name of teacher already exists
        repeated_entry('ID or name')
    #If entry is valid:
    else:
        tch_names[entry5.get()] = entry6.get().replace(' ','_')#spaces are replaced by _ because spaces are not allowed in table names in MySQL
        for i in listbox5.curselection():
            subjects[listbox5.get(i)] = subjects[listbox5.get(i)] + [entry6.get()]
        listbox5.select_clear(0,listbox5.size()-1)        
        listbox1.insert(entry5.get() , entry6.get() + '(' + str(entry5.get()) + ')' )
        popup1.destroy()
    return;    

##Proceed to next screen after user confirms that data entered is correct
def ok1():
    global listbox2
    for i in [listbox1, button3, button4, button7, scrollbar1]:
        i.destroy()
    for tid , tname in tch_names.items():
        sq('INSERT INTO TEACHERS VALUES( ' + str(tid) + ' , "' + tname + '" )') 
    create_tch_tables()#Create empty time table for each teacher
    screen5_pre_requisites()
    return;

##Creates empty time table for each teacher
def create_tch_tables():
    for tid , tname in tch_names.items():
        sq('CREATE TABLE IF NOT EXISTS TCH' + tname + ' (DAY VARCHAR(10))')
        for curday in days: 
            sq('INSERT INTO TCH' + tname + '(DAY) VALUES(' + '"' + curday + '"' + ')') #Adds all days as rows
        for period in range( 1 , no_perds + 1 ):
           #Adds the period numbers as columns
           sq('ALTER TABLE TCH' + tname + ' ADD COLUMN P' + str(period) + ' VARCHAR(30) DEFAULT "0"')
    return;

'''---------------------------------------------------------------SCREEN 4-----------------------------------------------------------------------------------------------------------------------------------------------------------'''

                      
##Widgets required for screen 4
def screen4_pre_requisites():
    global listbox2 , scrollbar2
    scrollbar2 = Scrollbar(root)
    scrollbar2.grid(row = 0 , column = 6 , rowspan = 4 , sticky = 'ns' )
    listbox2 = Listbox(root, yscrollcommand = scrollbar2.set)#Listbox containing names of subjects entered
    listbox2.grid(row = 0 , column = 5 , rowspan = 4 )
    scrollbar2.config(command = listbox2.yview)
    default_input_sub()#deafult_entry - enters 5 subjects as default values
    screen4()
    return;

##Function to automatically input 7 subject names
def default_input_sub():#default_entry
    global n_index
    listbox2.insert(0 , 'Mathematics')
    listbox2.insert(1 , 'Physics')
    listbox2.insert(2 , 'Chemistry')
    listbox2.insert(3 , 'Computer Science')
    listbox2.insert(4 , 'English')
    listbox2.insert(5 , 'Library')
    listbox2.insert(6 , 'Pt')
    subjects.update({'Mathematics':[]})
    subjects.update({'Physics':[]})
    subjects.update({'Chemistry':[]})
    subjects.update({'Computer Science':[]})
    subjects.update({'English':[]})
    subjects.update({'Pt':[]})
    subjects.update({'Library':[]})
    n_index = 5#Due to 5 default_entry, otherwise 0
    return;

##Fourth screen - asks user for subject names
def screen4():
    global label7 , label8, entry7 , button8 , listbox2 , button9
    label7 = Label(root , text = "--------------------------------Subjects--------------------------------", bg = bgc)
    label7.grid(row = 0 , column = 0  , rowspan = 2, columnspan = 4)
    label8 = Label(root , text = "Enter a subject: " , justify = 'right', bg = bgc)
    label8.grid(row = 2 , column = 0 )
    entry7 = Entry(root)
    entry7.grid(row = 2 , column = 1 )
    button8 = Button(root, text = 'Submit' , command = lambda:submit4(), bd = 3, bg = bbgc, relief = 'ridge')#When user enters 1 subject name
    button8.grid(row = 3 , column = 0 , padx = 100 , columnspan  = 4)
    button9 = Button(root, text = 'OK' , command = lambda:ok2(), bd = 3, bg = bbgc, relief = 'ridge')#When user is done with entering subject names
    button9.grid(row = 4, column = 5 , padx = 5)    
    return;

##Store the subject names
def submit4():
    global subjects , label7 , label8 , entry7 , listbox2, n_index
    subname = entry7.get().capitalize()
    if subname == '' or subname.isspace() or subname.isdigit():#Check for invalid entry
        empty_entry('subject names')
    elif subname not in subjects.keys():#Check for valid entry
        subjects.update({subname:[]})
        listbox2.insert( n_index , subname) 
        for i in [label7,label8,entry7,button8,button9]:
            i.destroy()#Clears the widgets from the screen
        n_index+=1
        screen4()       
    else:#Check for invalid entry
        repeated_entry('subject')        
    return;

##When user is done with entering subject names
def ok2():
    global button11 , button12 , button13 , label7 , label8 , entry7 , listbox2, n_index
    n_index = 5 #Due to 5 default_entry, otherwise 0
    for i in [label7,label8,entry7,button8,button9]:
        i.destroy()#Clears screen from widgets of screen 4
        
##Option for user to edit the entered names:
    button11 = Button(root , text = 'Add subject' , command  = lambda: add2(), bd = 3, bg = bbgc, relief = 'ridge')#Add another subject
    button11.grid(row = 5 , column = 0)
    button12 = Button(root , text = 'Delete selected subject' , command = lambda : delete2(), bd = 3, bg = bbgc, relief = 'ridge')#Remove a selected subject
    button12.grid(row = 5 , column = 4)
    button13 = Button(root , text = 'OK' , command = lambda : ok3(), bd = 3, bg = bbgc, relief = 'ridge' )#User confirms that data is correct
    button13.grid(row = 6 , column = 5)
    return;

##Creates a popup for user to add a subject
def add2():
    global popup3 
    try:
        popup3.deiconify() #Checks if the Add subject popup already exists and bring that window forward
    except:
        global subjects , listbox2 , label9 , entry9
        popup3 = Tk()
        popup3.config(bg = bgc)
        popup3.title("Add subject...")
        label9 = Label(popup3 , text = 'Enter name of subject : ', bg = bgc)
        label9.grid(row = 0 , column = 0)
        entry9 = Entry(popup3)
        entry9.grid(row = 0 , column = 1)
        button10 = Button(popup3, text = "Submit", command  = lambda: submit5(), bd = 3, bg = bbgc, relief = 'ridge')
        button10.grid(row = 1 , column = 0 , columnspan = 1)
    return;

##To store the subject added by the user
def submit5():
    global subjects, listbox2, popup3, n_index
    subname = entry9.get().capitalize()
    if subname == '' or subname.isspace():
        empty_entry('subject')
    elif subname not in subjects.keys():
        n_index += 1
        subjects.update({subname : []})
        listbox2.insert(n_index , subname)        
        popup3.destroy()
    else:
        repeated_entry('subject')
    return;

##Deletes the selected subjects from the stored values
def delete2():
    global listbox2 , subjects
    if len(listbox2.curselection()):
        loc_var = listbox2.curselection()[0]
        del subjects[(listbox2.get(loc_var))]
        listbox2.delete(loc_var)
    else:
        empty_selection('subject')
    return;

##Clears the screen and adds widgets required for screen 2
def ok3():
    global listbox1  , listbox4
    for i in (button11 , button12 , button13 , listbox2 , scrollbar2):
        i.destroy()
    screen2_pre_requisites()
    return;



'''--------------------------------------------------------------SCREEN 5------------------------------------------------------------------------------------------------------------------------------------------------------'''

##Adds 2 grades automatically
def default_entry_screen5():#default_entry
    listbox3.selection_set(0,6)
    entry10.insert(0,('11','12')[grade_count])
    return;    

##Creates widgets required for screen5
def screen5_pre_requisites():
    global label12 , listbox3 , scrollbar5
    label12 = Label(root , text = 'Select subjects for that grade : ', bg = bgc)
    label12.grid(row = 2 , column = 0 , pady = 10)
    scrollbar5 = Scrollbar(root)
    scrollbar5.grid(row = 3 , column = 2, sticky = 'ns')
    listbox3 = Listbox(root,selectmode = 'multiple', yscrollcommand = scrollbar5.set)
    listbox3.grid(row = 3, column = 1)#Listbox containing all subject names
    scrollbar5.config(command = listbox3.yview)
    loc_count = 0#index count for adding subjects into listbox3
    for i in subjects.keys():#Adds suject names into listbox3
        listbox3.insert(loc_count,i)
        loc_count += 1
    screen5()
    return;

##Screen 5 - user enters number of sections in each grade and selects subjects taught for that subject
def screen5():
    global tch_names ,  label10 , entry10 , label11 , spinbox1 , button14 , listbox3
    label10 = Label(root,text  = 'Enter name of grade : ', bg = bgc)
    label10.grid(row = 0, column = 0)
    entry10 = Entry(root)
    default_entry_screen5()#default_entry - adds 2 grades automatically
    entry10.grid(row = 0 , column = 1)
    label11 = Label(root,text = 'Enter number of sections : ', bg = bgc)
    label11.grid(row = 1 , column = 0)
    spinbox1 = Spinbox(root, from_ = 0 , to = 26)#Spinbox to allow use to enter number of sections
    spinbox1.config(from_ = 2)#from_ = 2 because of 2 default entry, else 0
    spinbox1.grid(row = 1 , column = 1)
    button14 = Button(root , text = 'Submit' , command = lambda : submit6(), bd = 3, bg = bbgc, relief = 'ridge')#To store the data entered
    button14.grid(row = 4 , column = 3 , ipadx = 20 , ipady = 10 , padx = 10 , pady = 10)
    return;

##Stores the number of sections entered by the user in each grade 
def submit6():
    global spinbox1 , label10 , entry10 , label11 , button14  , listbox3 , grade_count , classes
    grade = str(entry10.get())
    #Check for invalid input
    if grade == '' or grade.isspace():
        empty_entry('grade name')
    elif int(spinbox1.get()) == 0:
        empty_selection('at least one section')
    elif len(listbox3.curselection()) == 0:
        empty_selection('subject')
    #If input is valid:
    else:    
        for index in listbox3.curselection():
            subname = listbox3.get(index)
            for num in range( 1 , int(spinbox1.get()) + 1):
                section = chr( 64+num )#Assigns a letter to each section - 'A', 'B', 'C' ,...
                #If the already dictionary contains grade + section as a key, add the list containing details about a subject 
                if grade+section in classes.keys():
                    classes[grade+section].append([subname,'',''])
                #Otherwise, create grade + section as a key, add the list containing details about a subject
                else:
                    classes[grade+section] = [[subname,'',''],]
        grade_count += 1
        for i in [spinbox1 , label10 , entry10 , label11 , button14]:
            i.destroy()
        if grade_count < no_grades:#If deatls about more grades have to be entered 
            listbox3.select_clear(0,listbox3.size()-1)
            screen5()
        else:#If details about all grades have been entered- proceed to next screen
            label12.destroy()
            listbox3.destroy()
            scrollbar5.destroy()
            screen6()
    return;


'''----------------------------------------------------------------------SCREEN6---------------------------------------------------------------------------'''
 
##Subject details are stored in a list having 3 elements:
    #1st element - name of subject
    #2nd element - name of teacher teaching that subject
    #3rd element - number of classes per week of that subject


##Screen6 - Enter details about all subjects taught to each section of each grade 
def screen6():
    global classcount , label16 , listbox6 , label17 , label18 , button15 , listbox7 , button16 , index_assign , cur_class , spinbox2 , label22, cur_subject
    cur_class = list(classes.keys())[classcount]
    label16 = Label(root , text = "Class " + cur_class , justify = 'center', bg = bgc)
    label16.grid(row = 0 , columnspan = 5)
    label17 = Label(root , text = 'Subjects for class ' + cur_class, bg = bgc)
    label17.grid(row = 2 , column = 2)
    listbox6 = Listbox(root)
    listbox6.grid(row = 2 , column = 3)
    for i in range(len(classes[cur_class])):
        listbox6.insert( i , classes[cur_class][i][0])
    button15 = Button(root , text = 'Edit subjects' , command = lambda : edit_subjects(), bd = 3, bg = bbgc, relief = 'ridge')
    button15.grid(row = 3 , column = 3)
    for i in range(len(classes[cur_class])):
        if classes[cur_class][i][1] == '':
            index_assign = i 
            cur_subject = classes[cur_class][i][0]
            label18 = Label(root , text = "Select teacher for " + cur_subject + ": ", bg = bgc)
            label18.grid(row = 2 , column = 0)
            listbox7 = Listbox(root)
            listbox7.grid(row = 2 , column = 1)
            label22 = Label(root , text = "Enter classes per week for " + cur_subject, bg = bgc)
            label22.grid(row = 3 , column = 0)
            spinbox2 = Spinbox(root , from_ = 0 , to = 100)
            spinbox2.config(from_ = set_def_cpw())#default_entry
            spinbox2.grid(row = 3 , column = 1)
            for x in range(len(subjects[cur_subject])):
                listbox7.insert( x , subjects[cur_subject][x])
            listbox7.selection_set(def_tch_selection())
            button16 = Button(root , text = 'Submit' , command = lambda : submit7(), bd = 3, bg = bbgc, relief = 'ridge', width = 9)
            button16.grid(row = 4  , columnspan = 3)            
            break       
    return;

##default_entry - selects teachers by default
def def_tch_selection():
    if cur_class[:2] == '11' or cur_subject in ['Pt' , 'Library']:
        return 0
    elif cur_class[:2] == '12':
        return 1
    else:
        return 0

#default_entry - sets default classes per week for all subjects
def set_def_cpw():
    if cur_subject == 'Pt':
        return 3
    if cur_subject == 'Library':
        return 2
    else:
        return 8

#Submit details about all subjects
def submit7():
    global classcount , classes
    if len(listbox7.curselection()) == 0:
        empty_selection('Teacher')
    elif int(spinbox2.get()) <= 0:
        empty_selection("Class per week")
    else:
        classes[cur_class][index_assign][1] = listbox7.get(listbox7.curselection()[0]).replace(' ','_')
        classes[cur_class][index_assign][2] = int(spinbox2.get())
        if classes[cur_class][index_assign][0] == classes[cur_class][-1][0]:
            classcount += 1
        for i in[label16 , label17 , listbox6 , button15 , label18 , listbox7 , button16, spinbox2 , label22]:
            i.destroy()
        if classcount == len(classes.keys()):
            algorithm()
        else:
            screen6()
    return;

#Remove the subjects listbox from screen6 and show it only when edit_subjects is clicked
def edit_subjects():
    global popup4
    try:
        popup4.deiconify()
    except:
        global classes , label19 , listbox8 , button17 , button18 , button19  
        popup4 = Tk()
        label19 = Label(popup4 , text = "Change subjects for class " + cur_class , justify = 'center', bg = bgc)
        label19.grid( row = 0 , columnspan = 3)
        listbox8 = Listbox(popup4)
        listbox8.grid(row = 1 , column = 0 , rowspan = 3)
        for i in range(len(classes[cur_class])):
            listbox8.insert( i , classes[cur_class][i][0])
        button17 = Button(popup4 , text = 'Add subject' , command = lambda : add3(), bd = 3, bg = bbgc, relief = 'ridge')
        button17.grid(row = 1 , column = 1)
        button18 = Button(popup4 , text = 'Delete selected subject' , command = lambda : delete3(), bd = 3, bg = bbgc, relief = 'ridge')
        button18.grid(row = 2 , column = 1) 
        button19 = Button(popup4 , text = 'Ok' , command = lambda : ok4(), bd = 3, bg = bbgc, relief = 'ridge')
        button19.grid(row = 3 , column = 1)
    return;

##User confirms entered information
def ok4():
    popup4.destroy()
    for i in[label16 , label17 , listbox6 , button15 , label18 , listbox7 , button16]:
            i.destroy()
    screen6()
    return;

##To delete a subject
def delete3():
    global classes
    if len(listbox8.curselection()) == 0:
        empty_selection("subject to be deleted")
    else:
        for i in classes[cur_class]:
            if i[0] == listbox8.get(listbox8.curselection()[0]):
                classes[cur_class].remove(i)
        popup4.destroy()
        edit_subjects()#this will refresh edit subjects screen        
    return;

##To add a subject
def add3():
    global popup5 , label20 , entry10 , label21 , listbox9 , button20
    popup5 = Tk()
    popup5.config(bg = bgc)
    label20 = Label(popup5 , text = 'Enter new subject for class ' + cur_class, bg = bgc)
    label20.grid(row = 0 , column = 0)
    entry10 = Entry(popup5)
    entry10.grid(row = 0 , column = 1)
    label21 = Label(popup5 , text = 'Existing subjects: ', bg = bgc)
    label21.grid(row = 1 , column = 0)
    listbox9 = Listbox(popup5)
    listbox9.grid(row = 1 , column = 1)
    for i in range(len(classes[cur_class])):
        listbox9.insert( i , classes[cur_class][i][0])
    button20 = Button(popup5 , text = 'Submit' , command = lambda : submit8(), bd = 3, bg = bbgc, relief = 'ridge')
    button20.grid(row = 2 , column = 1)
    return;

##Submit subject information
def submit8():
    global popup5 , label20 , entry10 , label21 , listbox9 , button20 , classes
    if entry10.get().isalpha():
        classes[cur_class].append([entry10.get(),''])
        for i in (popup5 , label20, entry10, label21, listbox9, button20 ):
            i.destroy()
        popup4.destroy()
        edit_subjects()#this will refresh edit subjects screen 
    else:
        empty_entry('a subject name')
    return;

'''----------------------------------------------------------------------algorithm-----------------------------------------------------------------------'''

##Main algorithm
def algorithm():
    cursor1 = mydb.cursor()
    for x_class in classes:
        slots = []
        for x in days:
            for y in range(1 , no_perds+1):
                slots.append( x + 'P' + str(y))
        sq('CREATE TABLE ' + x_class + ' ( DAY CHAR(3) )')
        for x_day in days:
            sq('INSERT INTO ' + x_class + ' (DAY) VALUES("' + x_day + '")' )
        for x_perd in range(1 , no_perds + 1):
            sq('ALTER TABLE ' + x_class + ' ADD COLUMN P' + str(x_perd) + ' VARCHAR(25) DEFAULT "0" ')
        list_subs = [classes[x_class][sub] for sub in range(len(classes[x_class]))]
        while len(list_subs) > 2:
            for x_subject in list_subs:
                if x_subject[0] not in ['Pt' , 'Library']:
                    r_sub_details = x_subject
                    break
            r_sub , sub_tch , sub_cpw = r_sub_details
            sub_no_perds = 0
            available_slots = [i for i in slots]
            while sub_no_perds < int(sub_cpw):
                r_slot = r.choice(available_slots)
                r_day = r_slot[:3]
                r_day_freq = 0
                cursor1 = mydb.cursor()
                cursor1.execute('SELECT * FROM ' + x_class + ' WHERE DAY LIKE "' + r_day + '"')
                list_r_day_freq = cursor1.fetchall()
                for array in list_r_day_freq:
                    r_day_freq += array.count(r_sub)
                if r_day_freq < max_freq_sub :
                    r_slot1 = r_slot
                    r_perd = r_slot1.split('P')[-1]
                    cursor1.execute('SELECT P' + r_perd + ' FROM ' + 'TCH' + sub_tch + ' WHERE DAY LIKE "' + r_day + '"')
                    fetch = cursor1.fetchall()
                    if fetch[0][0] == '0':
                        sq('UPDATE ' + x_class + ' SET P' + r_perd + ' = ' + '"' + r_sub + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        sq('UPDATE ' + 'TCH' + sub_tch + ' SET P' + r_perd + ' = ' + '"' + x_class + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        sub_no_perds += 1
                        slots.remove(r_slot)
                        available_slots.remove(r_slot)
                    else:
                        available_slots.remove(r_slot)
            list_subs.remove(r_sub_details)
        lib_count = 0
        pt_count = 0
        while len(slots) != 0:#Insert light periods into the timetable
                if lib_count <= 2:
                    r_slot = r.choice(slots)
                    for x_subject in list_subs:
                        if x_subject[0] == 'Library':
                            r_sub_details = x_subject
                            break
                    r_sub , sub_tch , sub_cpw = r_sub_details
                    r_day = r_slot[:3]
                    r_slot1 = r_slot
                    r_perd = r_slot1.split('P')[-1]
                    if fetch[0][0] == '0':
                        sq('UPDATE ' + x_class + ' SET P' + r_perd + ' = ' + '"' + r_sub + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        sq('UPDATE ' + 'TCH' + sub_tch + ' SET P' + r_perd + ' = ' + '"' + x_class + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        slots.remove(r_slot)
                    lib_count += 1
                if pt_count <= 3:
                    r_slot = r.choice(slots)
                    for x_subject in list_subs:
                        if x_subject[0] == 'Pt':
                            r_sub_details = x_subject
                            break
                    r_sub , sub_tch , sub_cpw = r_sub_details
                    r_day = r_slot[:3]
                    r_slot1 = r_slot
                    r_perd = r_slot1.split('P')[-1]
                    if fetch[0][0] == '0':
                        sq('UPDATE ' + x_class + ' SET P' + r_perd + ' = ' + '"' + r_sub + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        sq('UPDATE ' + 'TCH' + sub_tch + ' SET P' + r_perd + ' = ' + '"' + x_class + '"' + ' WHERE DAY LIKE ' + '"' + r_day + '"')
                        slots.remove(r_slot)
                    lib_count += 1

    root1.destroy()
    return;                          

    
screen1()
root.mainloop()



'''---------------------------------------------------------------------WEB BROWSER------------------------------------------------------------------------'''


mycur = mydb.cursor()

###############################1. MAIN WEBSITE ############################
f = "main website.html"
file = open( f , 'w')
contents ='''
<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size:22px;
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 15px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
  font size: 20;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: #4CAF50;
}

.nav .current {
  background-color: tomato;
}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: center;
}


.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>

<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>
<center><img src="logo.jpg" style="width:45%"></center>
</body>
</html>
'''
file.write(contents)
file.close()
wb.open_new_tab(f)

####################################################2.CLASSES AND 3.TEACHERS############################################


tch = open('teachers.html', 'w')
cl = open('classes.html', 'w')

style = '''<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size: 22px;
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 15px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: tomato;
}

.tx {
  background-color: lightcyan; 
  border: none;
  color: black;
  padding: 16px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
}

.tx:hover {
 background-color: lightcoral;
}

.nav .current {
  background-color: tomato;
}

table, th, td {
  border: 1px solid black;
  border-collapse: collapse;
}
th, td {
  padding: 5px;
  text-align: center;
}

.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>
'''

midcl ='''
<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>'''

midtch ='''
<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>'''

end = '''
</body>
</html>'''

codetch = ''' '''
for i in tch_names:
    bu = open(tch_names[i]+".html", 'w')
    h1 =  '''<center><h1>{}'s timetable</h1></center>'''.format(tch_names[i])
    mycur.execute("DESC "+'tch'+tch_names[i])
    cols = [k[0] for k in mycur.fetchall()]
    table = '''<table style="width:100%"><tr>'''
    for k in cols:
        table += "<th>{}</th>".format(k)
    table += "</tr>"
    mycur.execute("SELECT * FROM {}".format('tch'+tch_names[i]))
    rows = mycur.fetchall()
    for j in range(len(rows)):
        table += "<tr>"
        rt = rows[j]
        for m in rt:
            table += "<td>{}</td>".format(m)
        table+= "</tr>"
    table += "</table>"
    l = style+ midtch+ h1 + table + end
    bu.write(l)
    bu.close()
    codetch += '''<a href={}><button type="button" class="tx">'''.format(tch_names[i]+".html")+ tch_names[i] + '''</button></a>''' + '''\n'''


finaltch = style + midtch + codetch  + end
tch.write( finaltch )
tch.close()

codecl = ''' '''
for i in classes:
    classtab = open(i+".html", 'w')
    h1 = '''<center><h1>{} timetable</h1></center>'''.format(i)
    mycur.execute("DESC "+ i)
    cols = [k[0] for k in mycur.fetchall()]
    table = '''<table style="width:100%"><tr>'''
    for k in cols:
        table += "<th>{}</th>".format(k)
    table += "</tr>"
    mycur.execute("SELECT * FROM {}".format(i))
    rows = mycur.fetchall()
    for j in range(len(rows)):
        table += "<tr>"
        rt = rows[j]
        for m in rt:
            table += "<td>{}</td>".format(m)
        table+= "</tr>"
    table += "</table>"
    l = style+ midcl + h1 + table + end
    classtab.write(l)
    classtab.close()
    codecl += '''<a href={}><button type="button" class="tx">'''.format(i+".html")+ i + '''</button></a>''' + '''\n'''

finalcl = style + midcl + codecl + end
cl.write( finalcl )
cl.close()

#########################################4. Help #########################################

file2 = open( "abtproj.html", 'w' )
mainb ='''
<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size: 22px
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 22px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
  font-size: 22px;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: #4CAF50;
}

.nav .current {
  background-color: tomato;
}

.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>

<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>

</body>
</html>
'''
file2.write( mainb )
file2.close()


######################################################5. Credits ####################################################

file3 = open("doneby.html", 'w' )
doneby = '''
<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size: 22px;
  background-color: powderblue;
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 22px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
  font-size: 22px;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: #4CAF50;
}

.nav .current {
  background-color: tomato;
}

.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>

<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<center><h1> Credits </h1></center>
<p>This project was developed by Ajay V Kamath and Shiva Patil of class 12 'B', 
Sindhi High School, Hebbal, Bengaluru. The creators are persuing Computer
Science as their major subject and have developed this project as part of the
prescribed syllabus for AISSCE by CBSE. </p>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>

</body>
</html>'''
file3.write(doneby)
file3.close()

###################################################6. About ###########################################

file4 = open("moreabt.html", 'w' )
moreabt = '''
<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size: 22px;
  background-color: powderblue;
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 22px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
  font-size: 22px;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: #4CAF50;
}

.nav .current {
  background-color: tomato;
}

.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>

<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<center><h1> About </h1></center>
<p>Timetable scheduling is the process of creating timetables that fit the constraint of the scenario.
It has various applications ranging from scheduling transportation and school timetables to creating complex schedules
for highly optimized automated factories.
Majority of small-scale scheduling are done manually while larger operations require computer assisted scheduling.
There exist a lot of problem-solving methods, which typically use the concept of customary optimization algorithms
such as Genetic Algorithms, Backtracking, Constraint Logic Programming. Newer methods like Genetic Algorithm, which mimics Natural Selection,
and Tabu Search use Metaheuristic or Meta-strategy and Artificial Intelligence to solve the problem.
Automated timetabling has become subject to multiple advanced research and there exists even a conference named
The International Series of Conferences on the Practice and Theory of Automated Timetabling (PATAT) which is held biennially to serve as a forum for
an international community of researchers, practitioners and vendors on all aspects of computer-aided timetable generation.
Our project aims to achieve the goal of timetabling by a simpler algorithm with lesser constraints and more to do with our school's requirements. 
</p>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>

</body>
</html>'''

file4.write( moreabt )
file4.close()


####################################################7. End User #############################################

file5 = open("enduser.html", 'w' )
enduser = '''
<!DOCTYPE html>
<html lang="en-ca">
<head>
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-size: 22px;
  background-color: powderblue;
}

.header {
  background-color: #2196F3;
  color: white;
  text-align: center;
  padding: 22px;
}


.nav {
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;
  background-color: #777;
  font-size: 22px;
}

.nav li {
  float: left;
}

.nav li a {
  display: inline-block;
  color: white;
  text-align: center;
  padding: 16px;
  text-decoration: none;
}

.nav li a:hover {
  background-color: tomato;
}

.nav li a.active {
  color: white;
  background-color: #4CAF50;
}

.nav .current {
  background-color: tomato;
}

.dropdown {
  float: left;
  overflow: hidden;
  font-size: 22px;
}

.dropdown .dropbtn {
  cursor: pointer;
  font-size: 22px;  
  border: none;
  outline: none;
  color: white;
  padding: 14px 16px;
  background-color: inherit;
  font-family: inherit;
  margin: 0;
}

.dropdown:hover .dropbtn, .dropbtn:focus {
  background-color: red;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  float: none;
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
  text-align: left;
}

.dropdown-content a:hover {
  background-color: #ddd;
}

.show {
  display: block;
}
</style>
</head>
<body>

<header>
    <nav>
        <ul class="nav"> 
            <li><a href="main website.html">Home</a></li>
            <li><a href="classes.html">Classes</a></li>
            <li><a href="teachers.html">Teachers</a></li>
            <div class="dropdown">
  <button class="dropbtn" onclick="myFunction()">Help
    <i class="fa fa-caret-down"></i>
  </button>
  <div class="dropdown-content" id="myDropdown">
    <a href="doneby.html">Credits</a>
    <a href="moreabt.html">About</a>
    <a href="enduser.html">End User</a>
  </div>
  </div> 
</div>	
</header>

<center><h1> End User </h1></center>
<p>Scheduling classes in an institution is one of the tasks that can be categorized under operations management. Operations management aims to maximize efficiency in a certain area. Scheduling classes is often done by humans which proves to be efficient but does not mean it is perfect. Using computers to find the best solution for this problem using conventional method is extremely inefficient. Computers were therefore ignored for a time when solving such problem. However, rise in computing power and usage has opened ways in solving scheduling problems.
Operations management is often considered as backbone of many companies. Getting the most efficient work means higher profit. In an educational institution scenario, getting the most efficient schedule does not only help reduce expense but mainly to cater to students. Often, better schedules give students and instructors better control on their time.
Creating schedules is done better by humans than conventional computing techniques because humans have powerful brain to assess constraints and combinations better. However, scheduling is known to be non-deterministic polynomial time (NP) complete problem where in order to find the best solution, every possible combination should be executed. Humans cannot compute every possible combination and therefore solves the problem by just filling up and making sure that the constraints are met. This is known to be “good enough” solution. This process is prone to errors, inefficiency and violation of constraints especially when working in a highly tight scenario.
This project is specifically designed for medium-large size schools. The main motive was to create an automatic timetabler with the specific requirements of our school in mind.
 </p>

<script>
/* When the user clicks on the button, 
toggle between hiding and showing the dropdown content */
function myFunction() {
  document.getElementById("myDropdown").classList.toggle("show");
}

// Close the dropdown if the user clicks outside of it
window.onclick = function(e) {
  if (!e.target.matches('.dropbtn')) {
  var myDropdown = document.getElementById("myDropdown");
    if (myDropdown.classList.contains('show')) {
      myDropdown.classList.remove('show');
    }
  }
}
</script>

</body>
</html>'''

file5.write( enduser )
file5.close()
