
compare = np.array([[])
class Dose:
    dose_type: int
    latitude: float
    longitude: float
    dose: str
   

    def __init__(self, dose_type: like:np._ArrayLikeInt, latitude: float, longitude: float):
        self.dose_type = dose_type
        self._set_cutoffs()
        self.longitude = longitude
        self.latitude = latitude

    @param.depends('dose_type', Watch=True)
    def _set_cutoffs(self):
        self.cutoffs = self.dose_type






############### TED Dose Area #############




# check for values less than or equal to 5 rem and greater than 1 rem in dose data
orange = np.where((dose <= 5) & (dose > 1))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats3 = lats1[orange]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs3 = longs1[orange]   

# make new orange dose list to be used for pandas dataframe    
for odose in dose:
    orange_dose = dose[orange]

# pandas data fram with orange data    
orange_area = pd.DataFrame({
    'lats1': lats3,
    'lons1': longs3,
    'dose': orange_dose
})

# check for values less than or equal to 1 rem and greater than 0.1 rem in dose data
yellow = np.where((dose <= 1) & (dose > 0.1))

# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats4 = lats1[yellow]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs4 = longs1[yellow]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose:
    yellow_dose = dose[yellow] 
 
# pandas data fram with yellow data    
yellow_area = pd.DataFrame({
    'lats2': lats4,
    'lons2': longs4,
    'dose': yellow_dose
})

# check for values less than 0.1 rem (100 millirem) and greater than 0.001 rem (1000 millirem) in dose data
green = np.where((dose <= 0.1) & (dose > 0.001))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats5 = lats1[green]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs5 = longs1[green]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose:
    green_dose = dose[green] 

# pandas data fram with green data    
green_area = pd.DataFrame({
    'lats3': lats5,
    'lons3': longs5,
    'dose': green_dose
})


####################Creating the map##############

#To create map, location should be [lat1,long1]
Rad_Map = folium.Map(
    location=[lat1, long2],
    zoom_start=10
)



#Add dose area layers to map
FG_TED = folium.FeatureGroup(name="TED Dose").add_to(Rad_Map)
FG_Adult = folium.FeatureGroup(name="Adult Thyroid Dose", show=False).add_to(Rad_Map)
FG_Child = folium.FeatureGroup(name="Child Thyroid Dose", show=False).add_to(Rad_Map)
FG_EM = folium.FeatureGroup(name="EM Worker Dose", show=False).add_to(Rad_Map)



#Add Layer Control
folium.LayerControl().add_to(Rad_Map)

#Add measure tool 
plugins.MeasureControl(position='topright', primary_length_unit='meters', secondary_length_unit='miles', primary_area_unit='sqmeters', secondary_area_unit='acres').add_to(Rad_Map)

#################### Adding the TED colored circles to the map ##############

# add red marker one by one on the map
for i in range(0,len(red_area)):
    FG_TED.add_child(folium.Circle(
      location=[red_area.iloc[i]['lats'], red_area.iloc[i]['lons']],
      popup=red_area.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add orange marker one by one on the map
for i in range(0,len(orange_area)):
    FG_TED.add_child(folium.Circle(
      location=[orange_area.iloc[i]['lats1'], orange_area.iloc[i]['lons1']],
      popup=orange_area.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add yellow marker one by one on the map
for i in range(0,len(yellow_area)):
    FG_TED.add_child(folium.Circle(
      location=[yellow_area.iloc[i]['lats2'], yellow_area.iloc[i]['lons2']],
      popup=yellow_area.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))

# add green marker one by one on the map
for i in range(0,len(green_area)):
    FG_TED.add_child(folium.Circle(
      location=[green_area.iloc[i]['lats3'], green_area.iloc[i]['lons3']],
      popup=green_area.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
############### Adult Thyroid Dose Area #############

# dose data updates
dose1 = (np.asarray(adult_total)).flatten()

# check for values greater than or equal to 500 rem in dose data
red1 = np.where(dose1 >= 500)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats6 = lats1[red1]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs6 = longs1[red1]   
 
# make new red dose list to be used for pandas dataframe    
for rdose in dose1:
    red_dose1 = dose1[red1]
    
# red area pandas df to iterate folium circles function with
red_area1 = pd.DataFrame({
    'lats': lats6,
    'lons': longs6,
    'dose': red_dose1
})

# check for values less than 500 rem and greater than or equal to 10 rem in dose data
orange1 = np.where((dose1 < 500) & (dose1 >= 10))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats7 = lats1[orange1]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs7 = longs1[orange1]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose1:
    orange_dose1 = dose1[orange1]

# pandas data fram with orange data    
orange_area1 = pd.DataFrame({
    'lats1': lats7,
    'lons1': longs7,
    'dose': orange_dose1
})

# check for values less than to 10 rem and greater than or equal to 5 rem in dose data
yellow1 = np.where((dose1 < 10) & (dose1 >= 5))

# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats8 = lats1[yellow1]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs8 = longs1[yellow1]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose1:
    yellow_dose1 = dose1[yellow1] 
 
# pandas data fram with yellow data    
yellow_area1 = pd.DataFrame({
    'lats2': lats8,
    'lons2': longs8,
    'dose': yellow_dose1
})

# check for values less than 0.1 rem (100 millirem) and greater than 0.001 rem (1000 millirem) in dose data
green1 = np.where((dose1 < 5) & (dose1 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats9 = lats1[green1]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs9 = longs1[green1]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose1:
    green_dose1 = dose1[green1] 

# pandas data fram with green data    
green_area1 = pd.DataFrame({
    'lats3': lats9,
    'lons3': longs9,
    'dose': green_dose1
})


#################### Adding the Adut Thyroid colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[red_area1.iloc[i]['lats'], red_area1.iloc[i]['lons']],
      popup=red_area1.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[orange_area1.iloc[i]['lats1'], orange_area1.iloc[i]['lons1']],
      popup=orange_area1.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[yellow_area1.iloc[i]['lats2'], yellow_area1.iloc[i]['lons2']],
      popup=yellow_area1.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area1)):
    FG_Adult.add_child(folium.Circle(
      location=[green_area1.iloc[i]['lats3'], green_area1.iloc[i]['lons3']],
      popup=green_area1.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
    
############### Child Thyroid Dose Area #############

# dose data update
dose2 = (np.asarray(child_total)).flatten()

# check for values greater than or equal to 500 rem in dose data
red2 = np.where(dose2 >= 500)

# make new lats list with index list corresponding to 5 rem dose data values
for las in lats1:
    lats10 = lats1[red2]
    
# make new longs list with index list corresponding to 5 rem dose data values
for lon in longs1:
    longs10 = longs1[red2]    

# make new red dose list to be used for pandas dataframe       
for rdose in dose2:
    red_dose2 = dose2[red2]

# make new red dose list to be used for pandas dataframe        
red_area2 = pd.DataFrame({
    'lats': lats10,
    'lons': longs10,
    'dose': red_dose2
})
  
# check for values less than 500 rem and greater than or equal to 100 rem in dose data
orange2 = np.where((dose2 < 500) & (dose2 >= 5))
    
# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats11 = lats1[orange2]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs11 = longs1[orange2]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose2:
    orange_dose2 = dose2[orange2]

# pandas data fram with orange data    
orange_area2 = pd.DataFrame({
    'lats1': lats11,
    'lons1': longs11,
    'dose': orange_dose2
})  
    
# check for values less than 5 rem and greater than or equal to 1 rem in dose data
yellow2 = np.where((dose2 < 5) & (dose2 >= 1))
    
# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats12 = lats1[yellow2]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs12 = longs1[yellow2]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose2:
    yellow_dose2 = dose2[yellow2] 
 
# pandas data fram with yellow data    
yellow_area2 = pd.DataFrame({
    'lats2': lats12,
    'lons2': longs12,
    'dose': yellow_dose2
})

# check for values less than 1 rem and greater than 0.1 rem (100 millirem) in dose data
green2 = np.where((dose2 < 1) & (dose2 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats13 = lats1[green2]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs13 = longs1[green2]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose2:
    green_dose2 = dose2[green2] 

# pandas data fram with green data    
green_area2 = pd.DataFrame({
    'lats3': lats13,
    'lons3': longs13,
    'dose': green_dose2
})

#################### Adding the Child Thyroid colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area2)):
    FG_Child.add_child(folium.Circle(
      location=[red_area2.iloc[i]['lats'], red_area2.iloc[i]['lons']],
      popup=red_area2.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area2)):
    FG_Child.add_child(folium.Circle(
      location=[orange_area2.iloc[i]['lats1'], orange_area2.iloc[i]['lons1']],
      popup=orange_area2.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area2)):
    FG_Child.add_child(folium.Circle(
      location=[yellow_area2.iloc[i]['lats2'], yellow_area2.iloc[i]['lons2']],
      popup=yellow_area2.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area2)):
    FG_Child.add_child(folium.Circle(
      location=[green_area2.iloc[i]['lats3'], green_area2.iloc[i]['lons3']],
      popup=green_area2.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))
    
############### Emergency Worker Dose Area #############
    
# dose data update
dose3 = (np.asarray(ted_total)).flatten()

# check for values greater than 25 rem in dose data
red3 = np.where(dose3 > 25)

# make new red dose list to be used for pandas dataframe  

# check for values less than or equal to 25 rem and greater than 10 rem in dose data
orange3 = np.where((dose3 <= 25) & (dose3 > 10))

# make new lats list with index list corresponding to orange dose data values
for lass in lats1:
    lats15 = lats1[orange3]

# make new longs list with index list corresponding to orange dose data values
for lonn in longs1:
    longs15 = longs1[orange3]   
    
# make new orange dose list to be used for pandas dataframe        
for odose in dose3:
    orange_dose3 = dose3[orange3]

# pandas data fram with orange data    
orange_area3 = pd.DataFrame({
    'lats1': lats15,
    'lons1': longs15,
    'dose': orange_dose3
})  

# check for values less than or equal to 10 rem and greater than 5 rem in dose data
yellow3 = np.where((dose3 <= 10) & (dose3 > 5))
    
# make new lats list with index list corresponding to yellow dose data values
for lasss in lats1:
    lats16 = lats1[yellow3]

# make new longs list with index list corresponding to yellow dose data values
for lonnn in longs1:
    longs16 = longs1[yellow3]

# make new yellow dose list to be used for pandas dataframe    
for ydose in dose3:
    yellow_dose3 = dose3[yellow3] 
 
# pandas data fram with yellow data    
yellow_area3 = pd.DataFrame({
    'lats2': lats16,
    'lons2': longs16,
    'dose': yellow_dose3
})

# check for values less than or equal to 5 rem and greater than 0.1 rem (100 millirem) in dose data
green3 = np.where((dose3 <= 5) & (dose3 > 0.1))

# make new lats list with index list corresponding to green dose data values
for lassss in lats1:
    lats17 = lats1[green3]

# make new longs list with index list corresponding to green dose data values
for lonnnn in longs1:
    longs17 = longs1[green3]
    
# make new green dose list to be used for pandas dataframe    
for gdose in dose3:
    green_dose3 = dose3[green3] 

# pandas data fram with green data    
green_area3 = pd.DataFrame({
    'lats3': lats17,
    'lons3': longs17,
    'dose': green_dose3
})

#################### Adding the Emergency Worker colored circles to the map ##############

# add marker one by one on the map
for i in range(0,len(red_area3)):
    FG_EM.add_child(folium.Circle(
      location=[red_area3.iloc[i]['lats'], red_area3.iloc[i]['lons']],
      popup=red_area3.iloc[i]['dose'],
      radius=50,
      color="red",
      fill=True,
      fill_color="red"
   ))
    
# add marker one by one on the map
for i in range(0,len(orange_area3)):
    FG_EM.add_child(folium.Circle(
      location=[orange_area3.iloc[i]['lats1'], orange_area3.iloc[i]['lons1']],
      popup=orange_area3.iloc[i]['dose'],
      radius=50,
      color="orange",
      fill=True,
      fill_color="orange"
   ))

# add marker one by one on the map
for i in range(0,len(yellow_area3)):
    FG_EM.add_child(folium.Circle(
      location=[yellow_area3.iloc[i]['lats2'], yellow_area3.iloc[i]['lons2']],
      popup=yellow_area3.iloc[i]['dose'],
      radius=50,
      color="yellow",
      fill=True,
      fill_color="yellow"
   ))
    
# add marker one by one on the map
for i in range(0,len(green_area3)):
    FG_EM.add_child(folium.Circle(
      location=[green_area3.iloc[i]['lats3'], green_area3.iloc[i]['lons3']],
      popup=green_area3.iloc[i]['dose'],
      radius=50,
      color="green",
      fill=True,
      fill_color="green"
   ))

Rad_Map.save("PlumeMap.html")
