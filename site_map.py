import folium

m = folium.Map((41.5853,-71.5707),
               zoom_start=9,
               tiles='https://tiles.stadiamaps.com/tiles/alidade_smooth_dark/{z}/{x}/{y}{r}.png',
               minZoom= 0,
               maxZoom= 20,
               attr= '&copy; <a href="https://www.stadiamaps.com/" target="_blank">Stadia Maps</a> &copy; <a href="https://openmaptiles.org/" target="_blank">OpenMapTiles</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
               )



folium.LayerControl().add_to(m)

m.save("templates/sites_map.html")