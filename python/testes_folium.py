import folium
#import coordenadas
from folium.plugins import MiniMap, FloatImage, MeasureControl, MousePosition, TagFilterButton

#--------------#
#Cores disponiveis
#red, blue, green, purple, orange, darkred, lightred, beige, darkblue, 
#darkgreen, cadetblue, darkpurple, white, pink, lightblue, lightgreen, gray, black, lightgray
#--------------#

#SETUP
rosaDosVentos = ("https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png")
formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};" #formatador pros pontos da posição do mouse
florianopolis_coords = [-27.5973002, -48.5496098] # Coordenadas aproximadas do centro de Florianópolis

#Funcoes 
def trilhaDaBoia(coordenadas, nomeDaBoia, corDaBoia):
    folium.PolyLine(coordenadas, tooltip=nomeDaBoia, dash_array="5,10", color=corDaBoia, smooth_factor=30).add_to(mapa)
    for coordenada in coordenadas[1:]:
        folium.Marker(coordenada, icon=folium.Icon(color=corDaBoia, icon='circle')).add_to(mapa)

def marcadorDeBoia(coordenadaDaBoia, nomeDaBoia, corDaBoia, grupoBoia):
    folium.Marker(coordenadaDaBoia, tooltip=nomeDaBoia, icon=folium.Icon(color=corDaBoia, icon='glyphicon-flag')).add_to(grupoBoia)

#-------------#

# Criar um mapa centrado em Florianópolis
mapa = folium.Map(location=florianopolis_coords, zoom_start=12)#, tiles="Esri.WorldImagery", attr='Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community')
#Adicionar minimapa
MiniMap(toggle_display=True).add_to(mapa)

#Adicionar rosa dos ventos
FloatImage(rosaDosVentos, bottom=70, left=4).add_to(mapa)

#Medir distância no mapa
mapa.add_child(MeasureControl())

#Adiciona posição do mouse
MousePosition(position="bottomleft", separator=" | ", lat_formatter=formatter, lng_formatter=formatter, prefix="Coordinates:").add_to(mapa)


#Criar grupos de pontos para as boias
grupoVermelho = folium.FeatureGroup("Boia Vermelha").add_to(mapa)
grupoVerde = folium.FeatureGroup("Boia Verde").add_to(mapa)
grupoPreto = folium.FeatureGroup("Boia Preta").add_to(mapa)
grupoLaranja = folium.FeatureGroup("Boia Laranja").add_to(mapa)

#marcadorDeBoia([-27.43, -48.49], 'Boia Vermelha', 'red', grupoVermelho)
marcadorDeBoia([-27.28, -48.57], 'Boia Verde', 'green', grupoVerde)
marcadorDeBoia([-27.280, -48.434], 'Boia Laranja', 'orange', grupoLaranja)
marcadorDeBoia([-27.208, -48.533], 'Boia Preta', 'black', grupoPreto)

#Colocar coordenadas da trilha de uma boia
#trail_coordinates = [(-27.615129, -48.3964593),(-27.626640, -48.418400), (-27.635592, -48.378848), (-27.653399, -48.399833)]
#folium.PolyLine(trail_coordinates, tooltip='Caminho da Boia Verde', dash_array="5,10", color="green").add_to(mapa)

coordenadasDaTrilha = [(-27.414, -48.518), (-27.414, -48.517), (-27.413, -48.517), (-27.412, -48.517), (-27.412, -48.516), (-27.411, -48.516)]
marcadorDeBoia(coordenadasDaTrilha[0], 'Boia Vermelha', 'red', grupoVermelho)
trilhaDaBoia(coordenadasDaTrilha, 'Boia Vermelha', 'red')


#Boat Marker
#folium.plugins.BoatMarker(
   # location=(-27.525047, -48.329480), heading=-20, wind_heading=46, wind_speed=25, color="#f2f2f2").add_to(mapa)

#Local usuário
folium.plugins.LocateControl(auto_start=False).add_to(mapa)


#centrar nos marcadores 
folium.FitOverlays(fly=True).add_to(mapa)
folium.LayerControl().add_to(mapa)

# Mostrar o mapa
mapa.save('mapaFlorianopolis.html')