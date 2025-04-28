import folium
import geopandas
import pandas

m = folium.Map((41.5853,-71.5707),
               zoom_start=9,
               tiles=None
               )

# Tiles are sourced from Jawg maps. This provider requires an access token to limit the amount of map views
# (max veiws is 25000 in free version). These tiles were chosen for reliability despite the limited access.
# access token is associated with jevans0000@uri.edu
folium.raster_layers.TileLayer(
    tiles='https://tile.jawg.io/jawg-light/{z}/{x}/{y}{r}.png?access-token=qlH1rmXXIAFgdl7HAHKl8Kf0LDkig02LxzDANjpBK2Rh2khcLTGyBX9Sa261A5GB',
    name='Light Mode',
    attr='<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
).add_to(m)

folium.raster_layers.TileLayer(
    tiles='https://tile.jawg.io/jawg-dark/{z}/{x}/{y}{r}.png?access-token=qlH1rmXXIAFgdl7HAHKl8Kf0LDkig02LxzDANjpBK2Rh2khcLTGyBX9Sa261A5GB',
    name='Dark Mode',
    attr='<a href="https://jawg.io" title="Tiles Courtesy of Jawg Maps" target="_blank">&copy; <b>Jawg</b>Maps</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    ).add_to(m)

lgd_txt = '<span style="color:blue;">Sampling Locations</span>'
sampLocations = folium.FeatureGroup(name= lgd_txt.format()).add_to(m)
with open("sampData/locations.csv") as f:
    df = pandas.read_csv(f)
for index, row in df.iterrows():
    popup = folium.Popup("<div>" + row['Description'] +
            "<br>Most Recent Sample:<br>Date: " + str(row['Date Sampled']) +
            "<br>Concentration (ppb): " + str(row['Concentration (ppb)'])+"</div><a href='/" +
            row['Point_ID'] + "' target='_top'>View Site Data</a>", max_width=300)

    folium.Marker([row['GPS_N'],row['GPS_W']],popup=popup, tooltip=row['Description']).add_to(sampLocations)

lgd_txt = '<span style="color:green;">ASRI Refuges</span>'
refuges = folium.FeatureGroup(name= lgd_txt.format()).add_to(m)
gdf = geopandas.read_file("static/ASRI Refuges.geojson")
folium.GeoJson(gdf,style_function=lambda feature: {'fillColor': 'lime', 'color': 'lime'} ).add_to(refuges)

folium.map.LayerControl('topleft', collapsed= False).add_to(m)

m.save("templates/map.html")