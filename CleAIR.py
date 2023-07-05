'''                                    CleAIR is an application that gives the air quality details.

                                       The code is divided into two parts. The first allows the user to sign up and sign in.
                                       The second lets the user to navigate throughout the app.
                                       Menu 1: Sign up and Sign in page
                                       Menu 2: Navigation through app pages
                                               --> Current day air composition bar graph
                                               --> Average forecast over 7 days for PM10, PM2.5 and Ozone
                                               --> Map for visualising AQI of different cities around the world


reference: https://nagasudhir.blogspot.com/2021/07/draw-markers-in-python-folium-maps.html
Group members: Aarzoo (2022008), Anushka Srivastava (2022086), Vanshika Pal (2022560)
'''

import requests
import string
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import date
import map_cities

def aqi(city): 
    api="74e1a8b17aa5dc692236bb296a0eb7c3d0c45832"
    url=f"https://api.waqi.info/feed/{city}/?token={api}"
    res=requests.get(url)
    if res.status_code==200:
        data=res.json()["data"]
    else:
        print("Bad Gateway")
    for x,y in data.items():
        if x=='aqi':
            aqi=int(y)
            print('Current AQI is:',y)
            if aqi<=50:
                print('Good')
            elif aqi>=51 and aqi<=100:
                print('Moderate')
            elif aqi>=101 and aqi<=150:
                print('Unhealthy for sensitive groups')
            elif aqi>=151 and aqi<=200:
                print('Unhealthy')
            elif aqi>=201 and aqi<=300:
                print('Very unhealthy') 
            else:
                print('Hazardous')

def emailcheck(m):
    f=True
    if "@" in m and m.endswith(".com"):
        pass
    else:
        f=False
    l=m.split("@")
    user=l[0]
    domain=l[1].split(".")
    for i in user:
        if i.isalnum()==0 and i!="_":
            f=False
    if domain[0].isalpha() and domain[1]=="com":
        pass
    else:
        f=False
    return f

def userid():
    global user_id
    user_id=input("Enter User id")
    return user_id
    
def pwf():
    global pw
    pw=input("Set password: ")
    checkl(pw)
    
def checkl(pw):
    if len(pw)<=7:
        print("Password too short. Try again")
        pwf()
    else:
        checknum(pw)

def checknum(pw):
    c=0
    for i in pw:
        if i.isdigit():
            c+=1
    if c==0:
        print("Password must have atleast 1 digit")
        pwf()
    else:
        checksym(pw)

def checksym(pw):
    global q
    l=list(string.punctuation)
    s=0
    for i in pw:
        if i in l:
            s+=1
    if s==0:
        print("Password must have one special character")
        pwf()
    else:
        q=pw

#reading the file to retrieve the login details of all accounts
f=open("C:\\Users\\aarzo\\OneDrive\\Desktop\\12 IP bonus CleAIR\\IP bonus\\details.txt","r")
det=f.readlines()
login=[]
for i in det:
    i=i.split(",")
    login.append([i[0],i[1],i[2]])
f.close()

#Menu 1
print("Welcome to CleAIR".center(100,"-"))
print("1. Sign Up\n2. Sign In")
opt=int(input("Enter choice: "))
if opt==1:
    while True:
        email=input("Enter email id: ")
        temp=None
        for j in login:
            if email in j:
                print("Account already exists for this email id.")
                temp=False
                break
        if temp==False:
            continue
        valid=emailcheck(email)
        if valid==False:
            print("Enter valid email id.")
        else:
            break
    while True:
        un=input("Enter username: ")
        temp=False
        for j in login:
            if j[0]==un:
                print("Username already exists")
                temp=True
                break
            else:
                continue
        if temp==False:
            break
    pwf()
    login.append([un,email,q])
    f=f=open("details.txt","a")
    f.write(f"\n{un},{email},{q}")
    f.close()
    print("Account made :)")
elif opt==2:
    while True:
        un=input("Enter username: ")
        temp=False
        check=None
        for i in login:
            if i[0]==un:
                temp=True
                check=i
                break
        else:
            if temp==False:
                print("Username doesn't exist")
        if temp==True:
            break
    while True:
        password=input("Enter password: ")
        if check[2]==password:
            print("Logged in successfully")
            break
        else:
            print("Invalid password")
print()

#Menu 2
print("1. Location\n2. AQI details\n3. Logout")
print()

#asking for queries from the above menu
while True:
    ch=int(input("Enter option: "))
    if ch==1:
        url1="http://ip-api.com/json/"                               
        resp=requests.get(url1)
        data=resp.json()
        if resp.status_code==200:
            print("Your current location details are:")
            for x in data.keys():
                if x=="country":
                    country=data.get(x)
                    print('Country: ',data.get(x))     
                elif x=="city":
                    city=data[x]
                    print('City: ',data.get(x),'\n')        
            c=input("Would you like to change this?(yes/no) ").lower()
            if c=="yes":
                city="%20".join(input("Enter city: ").split())
        else:
            print("Bad gateway")
    elif ch==2:
        aqi(city)
        api="74e1a8b17aa5dc692236bb296a0eb7c3d0c45832"
        url=f"https://api.waqi.info/feed/{city}/?token={api}"
        res=requests.get(url)
        if res.status_code==200:
            data1=res.json()["data"]
        else:
            print("Error")
        #Menu 3
        print("1. View today's air composition\n2. View forecast\n3. View map\n4. Exit")
        while True:
            opt=int(input("Enter your choice: "))
            if opt==1:
                today=date.today()
                lx=['o3','pm10','pm2.5']
                ly=[]
                if res.status_code==200:
                    for x,y in data1.items():
                        if x=='forecast':
                            for u,v in y.items():
                                if u=='daily':
                                    for p,q in v.items():
                                        if p=='o3':
                                            for i in range(len(q)):
                                                for d,g in q[i].items():
                                                    if d=='day' and g==str(today):
                                                        ly.append(q[i]['avg'])
                                        if p=='pm10':
                                            for i in range(len(q)):
                                                for d,g in q[i].items():
                                                    if d=='day' and g==str(today):
                                                        ly.append(q[i]['avg']) 
                                        if p=='pm25':
                                            for i in range(len(q)):
                                                for d,g in q[i].items():
                                                    if d=='day' and g==str(today):
                                                        ly.append(q[i]['avg'])
                else:
                    print('Error')                                                                              
                plt.bar(lx, ly, width=0.5,color='pink')
                plt.xlabel("Air composition")
                plt.ylabel("Concentrations")
                plt.title('Today\'s report')  
                plt.show()
            elif opt==2:
                dates=[i["day"][5:] for i in data1["forecast"]["daily"]["o3"]]
                year=datetime.now().year
                val_o3=[i["avg"] for i in data1["forecast"]["daily"]["o3"]][:len(dates)]
                val_pm10=[i["avg"] for i in data1["forecast"]["daily"]["pm10"]][:len(dates)]
                val_pm25=[i["avg"] for i in data1["forecast"]["daily"]["pm25"]][:len(dates)]
                def_x=range(len(dates))
                plt.xlabel(f"Dates ({year})")
                plt.ylabel("Average level")
                plt.plot(def_x,val_o3,label="Ozone",color="blue")
                plt.xticks(def_x,dates)
                plt.plot(def_x,val_pm10,label="PM10",color="green")
                plt.xticks(def_x,dates)
                plt.plot(def_x,val_pm25,label="PM2.5",color="red")
                plt.xticks(def_x,dates)
                temp=len(dates)
                plt.title(f"Average forecast over {temp} days")
                plt.legend()
                plt.show()
                plt.show()
                plt.show()
            elif opt==3:
                api="74e1a8b17aa5dc692236bb296a0eb7c3d0c45832"
                l=[]
                state_capitals=[]
                print("Enter cities you want to compare with")
                while True:
                    x=input()
                    if x=="":
                        break
                    state_capitals.append(x)
                state_capitals.append(city)
                for cities in state_capitals:
                    url=f"https://api.waqi.info/feed/{cities}/?token={api}"
                    res=requests.get(url)
                    if res.status_code==200:
                        data=res.json()["data"]
                        if data!="Unknown station":
                            l.append([cities,data["city"]["geo"],data["aqi"]])
                    else:
                        print("Invalid Getaway")
                for mark in l[:-1]:
                    place,coord,aqi=mark
                    map_cities.map_markups(place,coord,aqi)
                place,coord,aqi=l[-1]
                obj= map_cities.map_markups(place,coord,aqi)
                map_cities.save(obj)
                print("Map created")
            elif opt==4:
                break
            print()
    elif ch==3:
        break
    print()
print()
print("Logged out successfully")
print("Thank you for using our app :)")