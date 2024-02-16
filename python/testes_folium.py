import folium, geocoder
from funções import marcadorDeBoia, trilhaDaBoia, criaListaDeCoordenadas
from io import StringIO
#import classes as c
from folium.plugins import MiniMap, FloatImage, MeasureControl, MousePosition, TagFilterButton

#--------------#
#Cores disponiveis
#red, blue, green, purple, orange, darkred, lightred, beige, darkblue, 
#darkgreen, cadetblue, darkpurple, white, pink, lightblue, lightgreen, gray, black, lightgray
#--------------#

#SETUP
rosaDosVentos = ("https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png")
formatter = "function(num) {return L.Util.formatNum(num, 6) + ' &deg; ';};" #formatador pros pontos da posição do mouse
florianopolis_coords = [-27.5973002, -48.5496098] # Coordenadas aproximadas do centro de Florianópolis

laranja = 'orange'; verde = 'green'; preto = 'black'; vermelho = 'red'; roxo = 'purple'
bv = 'Boia Vermelha'; bvd = 'Boia Verde'; bl = 'Boia Laranja'; bp = 'Boia Preta'
flag = 'glyphicon-flag'
#Funcoes

def plotarBoia(listaCoordenadasBoia, corDaBoia, grupoBoia):
    marcadorDeBoia(listaCoordenadasBoia[0],corDaBoia, flag, grupoBoia)
    trilhaDaBoia(listaCoordenadasBoia, corDaBoia, grupoBoia)

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

teste = -27.280, -48.434


ctb = criaListaDeCoordenadas('python\laranja.txt')
#dct = {latlng: c.coordBoia(latlng) for latlng in ctb}
#new_list = [item.replace("'", '') for item in ctb]
#print(teste)
#print(ctb)

plotarBoia(ctb, verde, grupoVerde)

marcadorDeBoia([-27.28, -48.57], verde, flag, grupoVerde)
marcadorDeBoia([-27.280, -48.434], laranja, flag, grupoLaranja)
marcadorDeBoia([-27.208, -48.533], preto, flag, grupoPreto)

marcadorDeBoia([-27.6017447,-48.5176886], roxo, flag, grupoPreto) #marcador na UFSC

marcadorDeBoia([-27.6964055,-48.5487495], 'gray', flag, grupoPreto)

#folium.Marker([-27.6891183,-48.5244573], popup=folium.Popup(str([-27.6891183,-48.5244573]), max_width=100), icon=folium.Icon(color='white', icon=flag, popup=[-27.6891183,-48.5244573])).add_to(mapa)
#coordenadasDaTrilha = [(-27.414, -48.518), (-27.414, -48.517), (-27.413, -48.517), (-27.412, -48.517), (-27.412, -48.516), (-27.411, -48.516)]
#print(coordenadasDaTrilha)
#marcadorDeBoia(coordenadasDaTrilha[0], 'Boia Vermelha', 'red', grupoVermelho)
#trilhaDaBoia(coordenadasDaTrilha, 'Boia Vermelha', 'red')


#Boat Marker
#folium.plugins.BoatMarker(
   # location=(-27.525047, -48.329480), heading=-20, wind_heading=46, wind_speed=25, color="#f2f2f2").add_to(mapa)

#Local usuário
folium.plugins.LocateControl(auto_start=False).add_to(mapa)

g = geocoder.ip('192.168.1.12')
g = geocoder.ip('me')
print(g.latlng)
folium.Marker(g.latlng, popup=folium.Popup(str(g.latlng), max_width=100), icon=folium.Icon(color='white', icon=flag, popup=g.latlng)).add_to(mapa)
#folium.plugins.BoatMarker(location=g.latlng, heading=-20, wind_heading=46, wind_speed=25, color="#f2f2f2").add_to(mapa)

#centrar nos marcadores 
folium.FitOverlays(fly=True).add_to(mapa)
folium.LayerControl().add_to(mapa)

# Mostrar o mapa
mapa.save('mapaFlorianopolis.html')