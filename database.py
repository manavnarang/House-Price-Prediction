import pyodbc 
import pandas as pd
from components import State
from components import City


class DALLocality:
    def __init__(self):
        self.con = pyodbc.connect('DRIVER={sql server};SERVER=MANAV\Manav;database=property;UID=sa;pwd=Manav@1499')
        
    def GetStates(self):
            allstates = []
            
            cur = self.con.cursor()
            cur.execute("Select * from states")
            
            records = cur.fetchall()
            
            
            for rec in records:
                s = State()
                
                s.StateId = rec[0]
                s.StateName = rec[1]
                
                allstates.append(s)
                
            return allstates;     
        
        
    def GetCities(self, StateId):
        AllCities = []
        
        cur = self.con.cursor()
        cur.execute("Select * from cities where StateId=?", (StateId))
        
        records = cur.fetchall()
        
        
        
        for rec in records:
            c = City()
            c.CityId = rec[0]
            c.CityName = rec[1]
            c.StateId = rec[2]
            
            AllCities.append(c)
            
        return AllCities
    
    
    def GetProperties(self,CityId):
        query = "Select * from Properties where CityId="+str(CityId);
        df = pd.read_sql(query, self.con)        
        
        return df   
         




    
            
        
            
            
                
                
                
            
    
        
        
    
    
    