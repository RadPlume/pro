 After the plant is selected from the dropdown, lat1 and long1 need to be
# updated to refelect the selected plant. 
# %%
from UI import GUI
import numpy as np
from bokeh.tile_providers import ESRI_IMAGING
#import newdose
# Get direction input and choose angle from pre-defined list or have user input variable


def _get_coordinates():
    ui = GUI()
    
    ui.xs
    ui.ys

    r_earth = 6371.0001 #km

    #wind is 16-wind compass rose
    ui.rads

    # After running the dose equation, the Y values need to be converted into km
    
    newY = Yval/1000 

    lat_array = (Xval*ui.r_cos) + (newY*ui.r_sin)
    lon_array = (newY*ui.r_cos) - (Xval*ui.r_sin)


    #Latitude from X
    for element in lon_array:
        lats = lat + (lon_array/r_earth)*(180/np.pi)

    #Longitude from Y
    for element in lat_array:
        longs = lon + (lat_array/r_earth) * ((180/np.pi) / np.cos(lat1 * np.pi/180))


'''LAT LONG and DOSE'''    
# lat /long coordinates from Xval/Yval
lats1, longs1, dose = np.asarray([lats, longs, ted_puff]).flatten()


# %%
class DoseTED():

    lambda w,x,y,z:  np.where(dose > 5)



class BaseMap():
    '''To create map, location should be [lat1,long1']'''
    
    Rad_Map = folium.Map(
        location=[33.38749636791151, -112.86533282010271],
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


class DoseEquivalency():
    '''Adding the TED colored circles to the map'''
    def main(self):
        # add red marker one by one on the map
        json_child = {
            'location': {[red_area.iloc[i]['lats'], red_area.iloc[i]['lons']]},
            'popup': red_area.iloc[i]['dose'],
            'radius: 50,
            'color': 'red',
            'fill': True,
            'fill_color': 'red',
        }

        def add_child(self):
            for i in range(0,len(red_area)):
                FG_TED.add_child(folium.Circle(
                    self.location=[red_area.iloc[i]['lats'], red_area.iloc[i]['lons']],
                    self.popup=red_area.iloc[i]['dose'],
                    self.radius=50,
                    self.color="red",
                    self.fill=True,
                    self.fill_color="red"
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
        

class DoseArea:
    '''Adult Thyroid Dose Area'''
    def at_red
    dose1 = (np.asarray(adult_puff)).flatten()

    # check for values greater than or equal to 500 rem in dose data
    red1 = np.where(dose1 >= 500)
    for las, lon, rdose in lats1, longs1, dose1:
        red_area1 = pd.DataFrame({
            'lats': lats1[red1],
            'lons': longs1[red1],
            'dose': red_dose1)
           
        red_dose1 = dose1[red1]

# %%
    colors = [read,orange,yellow,green]
    def area1(self,colors):    
            

# %%        
    # red area pandas df to iterate folium circles function with
    red_area1 = pd.DataFrame({
        'lats': lats6,
        'lons': longs6,
        'dose': red_dose1
    })


#######################################

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

##########################################


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
######################################

    # check for values less than 0.1 rem (100 millirem) and greater than 0.001 rem (1000 millirem) in dose data
    green1 = np.where((dose1 < 5) & (dose1 > 0.1))

    for lassss, lonnnn, g_dose in lats1:
            lats9 = lats1[green1]
    
    # pandas data fram with green data    
    green_area1 = pd.DataFrame({
        'lats3': lats9,
        'lons3': longs9,
        'dose': green_dose1
    })



class TED():
    def __inti__():
        self.latitudes, self.longitudes = gui.xs. gui.ys

    def ted():
        '''TED Dose Area'''
        filter_indices[0.001, 0.1, 1, 5]
        np.arrary(dose)[filter_indices]

        slices = [[:0.001], 0.0001:0.1, 0.1001:1, 1.001:5, 5:]

        red = np.where(dose > 5) # greater than 5 rem in dose data
        
        for las, lon, rdose in lats1, longs1, dose:
            lats2 = lats1[red]
            long2 = longs1[red]
            red_dose = dose[red]
       
        # red area pandas df to iterate folium circles function with
        red_area = pd.DataFrame({
            'lats': lats2,
            'lons': longs2,
            'dose': red_dose
        })

        orange_area = pd.DataFrame({
        'lats1': lats3,
        'lons1': longs3,
        'dose': orange_dose
        })

        yellow_area = pd.DataFrame({
        'lats2': lats4,
        'lons2': longs4,
        'dose': yellow_dose
        })

        green_area = pd.DataFrame({
        'lats3': lats5,
        'lons3': longs5,
        'dose': green_dose
        })


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


