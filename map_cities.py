import folium
import requests
def get_coordinates():
    url1 = "http://ip-api.com/json/"
    resp = requests.get(url1)
    data = resp.json()
    if resp.status_code == 200:
        for x in data.keys():
            if x == "lat":
                latitude = data.get(x)
            if x == "lon":
                longitude = data.get(x)
    return [latitude, longitude]

map_obj=obj=map_obj=folium.Map(location=get_coordinates(), zoom_start=5)

def map_markups(p,l,a):
    c,m = message(a)
    folium.Marker(location=l,tooltip=f'{p}',popup=folium.Popup(f'AQI: <b>{a}</b>| {m}',max_width=1000),icon=folium.Icon(icon="",color=c)).add_to(map_obj)
    return map_obj

def save(obj):
    obj.save('map.html')

def message(a):
    if a>=0 and a<=50:
        c='green'
        m='<b> Good</b> Safe to go outside'
    elif a>50 and a<=100:
        c='lightgreen'
        m='</b> Moderate</b> '
    elif a>100 and a<=150:
        c='orange'
        m='<b>Unhealthy</b> for sensitive groups'
    elif a>150 and a<=200:
        c='red'
        m='<b>Very Unhealthy</b> Wear a Mask'
    elif a>200 and a<=300:
        c='purple'
        m='<b>Very Unhealthy</b> Health Alert'
    elif a>300:
        c='darkred'
        m='<b> Harazdous</b> : Health Emergency'
    return c,m