from Tkinter import *
from tkFileDialog import askopenfilename
from tkMessageBox import *
import pandas
import numpy
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
import time                                                 #importing required modules and libraries
import sys

root = None
choose_label = None
filename_label = None
name = None
X = []
Y = []
X_Fit = []
dataHead = []
clf = linear_model.Ridge(alpha=0.5)
deg = 1
degree_entry=''
x_value_entry=''
y_value_show=''
x_value_label=''
y_value_label=''                                           #declaring variables

fh = open('Log.txt','a')                                   #For error files Logging

def openPushFunction():
    global filename_label
    global name
    global X
    global Y
    global dataHead
    x = []                                                 # referncing to already declared variables
    
    name = askopenfilename()

    if(name != None):
        try:
            x = name.split('.')
            if(x[1] != 'csv'):
                showinfo(message = 'Error!!! Only .csv files allowed')
                fh.write(str(time.asctime())+' Wrong file format selected\n')

            else:
                data = pandas.read_csv(name)
                dataHead = data.columns.values.tolist()
                X = data[str(dataHead[0])]
                Y = data[str(dataHead[1])]
                X = numpy.array(X)
                Y = numpy.array(Y)
                X = X.reshape(len(X),1)
                Y = Y.reshape(len(Y),1)
        except Exception as E:
            showinfo(message = 'Error!!! Only .csv files allowed')
            fh.write(str(time.asctime())+' Wrong file format selected\n')

            #X and Y are now numpy arrays
    #Here we have now got our data in X and Y

def plotPushButton():
    #Plotting will be done here
    global X
    global Y
    global dataHead
    try:
        plt.subplot(211)
        plt.scatter(X,Y)
        plt.ylabel(str(dataHead[1]))
        plt.xlabel(str(dataHead[0]))
        plt.title('Scatter Plot for '+str(dataHead[0])+' VS '+str(dataHead[1]))
        plt.subplot(212)
        plt.plot(X,Y)
        plt.ylabel(str(dataHead[1]))
        plt.xlabel(str(dataHead[0]))
        plt.title('Line Plot for '+str(dataHead[0])+' VS '+str(dataHead[1]))
        plt.tight_layout()
        plt.show()
    except Exception as E:
        showinfo(message = 'Plotting not done because of file not selected or contents of file not according to given format')
        fh.write(str(time.asctime())+' Plotting not possible. Check if file choosen or contents of file in correct format\n')
    # settings to plot a graph on the basis of stored data
    
def regressionDo():
    #Doing polynomial fitting and Regression
    global X
    global Y
    global X_Fit
    global clf
    global deg
    global degree_entry
    try:
        deg = int(degree_entry.get())
        poly = PolynomialFeatures(deg)
        X_Fit = poly.fit_transform(X) #The new fitted transformed X array
        clf.fit(X_Fit,Y)
        showinfo(message="Regression successful")
    except Exception as E:
        fh.write(str(time.asctime())+' Regression not done because of degree unavailability or function issue\n')
        showinfo(message="Regression Not possible. Make sure you have choosen the degree for regression")


def predictVal():
    global clf
    global x_value_entry
    global y_value_show
    global y_value_label
    global x_value_label
    global dataHead
    try:
        polyP = PolynomialFeatures(deg)
        x_get = float(x_value_entry.get())
        X_list = []
        X_list.append(x_get)
        X_list_n= numpy.array(X_list)
        X_Pre = polyP.fit_transform(X_list_n)
        Y_pre = clf.predict(X_Pre)
        y_val = float(Y_pre[0][0])
        y_value_label.config(text=str(dataHead[1]), bg = "black", fg = "white")
        x_value_label.config(text=str(dataHead[0]), bg = "black", fg = "white")
        y_value_show.config(text=str(y_val), bg = "black", fg = "white")        # carry out operations in case no errors occur
    except Exception as e:
        fh.write(str(time.asctime())+str(e)+'\n')   # carry out operations in case of errors arising
    
    
    
def main():
    global root
    global choose_label
    global filename_label
    global text
    global y_value_show
    global x_value_entry
    global degree_entry
    global y_value_label
    global x_value_label
    root = Tk()
   
    frame1 = Frame(root)
    frame2 = Frame(root)
    frame3 = Frame(root)
    frame4 = Frame(root)
    frame5 = Frame(root)
    frame6 = Frame(root)                                # declaring frames

    root.configure(bg = "black")
    frame1.configure(bg = "black")
    frame2.configure(bg = "black")
    frame3.configure(bg="black")
    frame4.configure(bg="black")
    frame5.configure(bg="black")
    frame6.configure(bg="black")


    
    title_label = Label(frame1,text = '2-Dimensional Data Prediction', bg = "black", fg = "white")
    title_label.pack()
    
    choose_label = Label(frame2,text = 'Choose a file', bg = "black", fg = "white")
    choose_label.pack(side = LEFT,padx = 20,pady = 10)
    
    open_button = Button(frame2,text = 'Open', command = openPushFunction)
    open_button.pack(padx = 40,pady = 10)
    
    plot_button = Button(frame3,text = 'PLOT', command = plotPushButton)
    plot_button.pack(pady = 10)
    
    degree_label = Label(frame4, text = 'Degree of regression', bg = "black", fg = "white")#, bg = "black")
    degree_label.pack(side = LEFT)
    
    degree_entry = Entry(frame4,width = 10)
    degree_entry.pack(side = LEFT,padx = 10)        # buttons and fields for varius essentials
    
    start_button = Button(frame5,text = 'Start\n Regression',command=regressionDo)
    start_button.pack()                             # setting up for regression

    x_value_label = Label(frame6, text = 'X-value', bg = "black", fg = "white")#, bg = "black")
    x_value_label.pack(side=LEFT)
    x_value_entry = Entry(frame6,width = 10)
    x_value_entry.pack(side=LEFT)                   # entry-field for input

    go_button = Button(frame6,text = 'GO',command=predictVal)
    go_button.pack(side=RIGHT)                      # proceeds for computation
   
    y_value_show = Label(frame6,text='', bg = "black", fg = "white")#, bg = "black", fg="white")
    y_value_show.pack(side=RIGHT,padx=30)
    y_value_label = Label(frame6,text = 'Y-value', bg = "black", fg = "white")#, bg = "black")
    y_value_label.pack(side=RIGHT,padx=30)          # display the computed result
    
    
    frame1.pack()
    frame2.pack()
    frame3.pack()
    frame4.pack(pady = 10)
    frame5.pack(pady = 20)
    frame6.pack()
    root.geometry('400x300+0+0')                    # packing content into the frame
    
    root.resizable(width=False, height=False)
    root.title('Predict2Data')
    root.iconbitmap('icon.ico')
    root.mainloop()                                 # Features of overall appearance set
    
main()
