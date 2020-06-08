
from database import DALLocality
import tkinter as tk
from tkinter.ttk import Combobox
from tkinter.ttk import Treeview
from sklearn import linear_model
import pandas as pd

class form:
    def __init__(self):


        self.root = tk.Tk()
        self.Area=tk.StringVar()
        self.Rooms=tk.StringVar()
        self.Age=tk.StringVar()
        
        self.option = tk.StringVar()
        
        self.count = tk.IntVar()

        self.option.set("House")

        self.root.geometry("1080x1920")
        self.root.title("House Price Predictor")

        self.lbl1 = tk.Label(self.root,text = "State")
        self.lbl1.place(x = 50,y = 50)
        
        self.cmbStates = Combobox(self.root,state = "readonly")
        self.cmbStates.place(x = 100 , y = 50)
        
        self.l1 = tk.Label(self.root,fg = "red")
        self.l1.place(x = 100 , y = 80)
        
    
        objDAL = DALLocality()
        self.AllStates = objDAL.GetStates()

        list1 = []
        
        for state in self.AllStates:
            list1.append(state.StateName)
        
        self.cmbStates['values'] = list1
        self.cmbStates.bind("<<ComboboxSelected>>", self.ComboItemChanged)

        self.lbl2 = tk.Label(self.root,text = "City")
        self.lbl2.place(x = 350 , y = 50)
        
        self.cmbCities = Combobox(self.root,state = "readonly")
        self.cmbCities.place(x= 400 , y = 50 )
         
        self.l2 = tk.Label(self.root, fg = "red")
        self.l2.place(x = 400 , y =80)
        
        
        self.lb6 = tk.Label(self.root,text = "CATEGORY")
        self.lb6.place(x = 600 , y = 50 )
        
        self.rbt1 = tk.Radiobutton(self.root,text="House", variable = self.option , value = "House")
        self.rbt1.place(x = 680, y = 50)
        
        self.rbt2 = tk.Radiobutton(self.root,text="Flat", variable = self.option , value = "Flat")
        self.rbt2.place(x = 750,y = 50 )
    
        
        self.lbl3 = tk.Label(self.root,text = "AREA")
        self.lbl3.place(x = 50 , y = 120)
        
        self.ent1 = tk.Entry(self.root,textvariable = self.Area )
        self.ent1.place(x = 100 , y = 120)
        
        self.l3 = tk.Label(self.root,fg = "red")
        self.l3.place(x = 100,y = 150)
        
        self.lbl4 = tk.Label(self.root,text = "Rooms")
        self.lbl4.place(x = 350 , y =120 )
        
        self.ent2 = tk.Entry(self.root,textvariable = self.Rooms)
        self.ent2.place(x = 400 , y =120)
        
        self.l4 = tk.Label(self.root,fg = "red")
        self.l4.place(x = 400,y = 150)
        
        
        self.lbl5 = tk.Label(self.root,text = "Age")
        self.lbl5.place(x = 600 , y = 120)
        
        self.ent3 = tk.Entry(self.root,textvariable = self.Age)
        self.ent3.place(x = 650, y =  120)
        
        self.l5 = tk.Label(self.root,fg = "red")
        self.l5.place(x = 650,y = 150)
        
        
        self.btn1 = tk.Button(self.root,text='Add',width=20,bg='brown',fg='white', command = self.AddClicked)
        self.btn1.place(x = 850 , y = 120)
        self.count = 1
        
        self.tree1=Treeview(self.root)
        self.tree1['columns']=("c1","c2","c3","c4" )
       
        self.tree1.heading("c1",text = "AREA (SQR. Ft.)")
        self.tree1.heading("c2",text = "ROOMS")
        self.tree1.heading("c3",text = "AGE (Years)")
        self.tree1.heading("c4", text="Predicted Price in INR")
        
        self.tree1.place(x = 50 , y = 200)
        
        self.l6 = tk.Label(self.root,fg = "red")
        self.l6.place( x = 400 , y = 450)
        
        self.btn2 = tk.Button(self.root,text = "PREDICT",width=20,bg='brown',fg='white' , command = self.PredictClicked)
        self.btn2.place(x = 650 , y = 450)
        
        self.btn3 = tk.Button(self.root,text = "EXIT",width=20,bg='brown',fg='white',command = self.root.destroy)
        self.btn3.place(x = 850 , y =450)
        
        
        
        self.AreasList = []
        self.RoomsList = []
        self.AgesList=[]
        
        
    def AddClicked(self):
        r = self.validateinputs1()
        if r == True:
            self.tree1.insert("",self.count,text = "Property "+str( self.count), values =(self.Area.get(),self.Rooms.get(),self.Age.get(),0 ))
            self.count+=1
            self.AreasList.append(self.Area.get())
            self.RoomsList.append(self.Rooms.get())
            self.AgesList.append(self.Age.get())
    
            self.Area.set ("")
            self.Rooms.set("")
            self.Age.set("")
            
    
    def ComboItemChanged(self, event):
        index =  self.cmbStates.current()
       
        StateId = self.AllStates[index].StateId
        
        objDAL = DALLocality()
        self.AllCities = objDAL.GetCities(StateId)
        
        
        list2 = []
        
        for city in self.AllCities:
            list2.append(city.CityName)
        
        self.cmbCities['values']=list2
        return index
        
    def PredictClicked(self):
        response = self.validateinputs2()
        if response == True:
            index = self.cmbCities.current()
            self.CityId = self.AllCities[index].CityId
            objDAL = DALLocality()
            TrainingData =objDAL.GetProperties(self.CityId)
            
            model= linear_model.LinearRegression()
            model.fit(TrainingData[['Area','Rooms','Age']],TrainingData.Price)

            TestData = pd.DataFrame({"Area":self.AreasList,\
                                     "Rooms":self.RoomsList,\
                                     "Age":self.AgesList})
        
            predictedprices =model.predict(TestData[["Area","Rooms","Age"]])
        
            print(predictedprices)
        
            children = self.tree1.get_children()       
            for child in children:
                self.tree1.delete(child)

            noe = len(self.AreasList)
        
            i = 0
            while i<noe:
                self.tree1.insert("", i , text= "Property "+str(i+1), values=( self.AreasList[i], self.RoomsList[i], self.AgesList[i], predictedprices[i]  ))
                i+=1
    
    def validateinputs1(self):
        r = True
        self.l3.config(text = "")
        self.l4.config(text = "")
        self.l5.config(text = "")
        
       
        
        
        
        if self.Area.get().isdigit() == False:
            self.l3.config(text = "Empty Field")
            r = False
        if self.Rooms.get().isdigit() == False:
            self.l4.config(text = "Empty field")
            r = False
        if self.Age.get().isdigit() == False:
            self.l5.config(text = "Empty Field")
            r = False
        return r
        
    def validateinputs2(self):
          response = True
          self.l1.config(text = "")
          self.l2.config(text = "")
          self.l6.config(text = "")
          index = self.cmbCities.current()
          if index == -1:
              self.l1.config(text = "State is Empty")
              self.l2.config(text = "City is Empty")
              response = False
          if len(self.AreasList) == 0:
              self.l6.config(text = "NO PROPERTY ADDED")
              response = False
              
          return response    
              
              
          
        
    
    
    
    
    
    
    
    def showframe(self):
        self.root.mainloop()


O=form()
O.showframe()
            
            
        
            
        
            
        
        
        
    
  
        
        
        
        
        
        
        
   
        

        