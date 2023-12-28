import folium, re
from folium.plugins import MiniMap, FloatImage, MeasureControl, MousePosition, TagFilterButton

caminhoArquivoLaranja = 'python\laranja.txt'
rosaDosVentos = ("https://raw.githubusercontent.com/ocefpaf/secoora_assets_map/a250729bbcf2ddd12f46912d36c33f7539131bec/secoora_icons/rose.png")
formatter = "function(num) {return L.Util.formatNum(num, 3) + ' &deg; ';};" #formatador pros pontos da posição do mouse
florianopolis_coords = [-27.5973002, -48.5496098] # Coordenadas aproximadas do centro de Florianópolis
laranja = 'orange'; verde = 'green'; preto = 'black'; vermelho = 'red'; roxo = 'purple'
bv = 'Boia Vermelha'; bvd = 'Boia Verde'; bl = 'Boia Laranja'; bp = 'Boia Preta'; br = 'Boia Roxa'
circle = 'circle'; flag = 'glyphicon-flag'

#Setup do mapa
mapa = folium.Map(location=florianopolis_coords, zoom_start=12)
MiniMap(toggle_display=True).add_to(mapa)
FloatImage(rosaDosVentos, bottom=70, left=4).add_to(mapa)
mapa.add_child(MeasureControl())
MousePosition(position="bottomleft", separator=" | ", lat_formatter=formatter, lng_formatter=formatter, prefix="Coordinates:").add_to(mapa) #posicao mouse
folium.plugins.LocateControl(auto_start=False).add_to(mapa) #local user


#Criar grupos de pontos para as boias
grupoVermelho = folium.FeatureGroup("Boia Vermelha").add_to(mapa)
grupoVerde = folium.FeatureGroup("Boia Verde").add_to(mapa)
grupoPreto = folium.FeatureGroup("Boia Preta").add_to(mapa)
grupoLaranja = folium.FeatureGroup("Boia Laranja").add_to(mapa)

def trilhaDaBoia(coordenadas, nomeDaBoia, corDaBoia, grupoBoia):
    folium.PolyLine(coordenadas, tooltip=nomeDaBoia, dash_array="5,10", color=corDaBoia, smooth_factor=30).add_to(mapa)
    for coordenada in coordenadas[1:]:
        marcadorDeBoia(coordenada, nomeDaBoia, corDaBoia, circle, grupoBoia)

def marcadorDeBoia(coordenadaDaBoia, nomeDaBoia, corDaBoia, icone, grupoBoia):
    folium.Marker(coordenadaDaBoia, tooltip=nomeDaBoia, icon=folium.Icon(color=corDaBoia, icon=icone)).add_to(grupoBoia)

    
def criaListaDeCoordenadas(caminhoArquivo):
    coordenadasLidas = []
    with open(caminhoArquivo) as arquivo:
        temp = []
        for lat_long_str in arquivo:
            lat_long = [float(x) for x in re.split(r',\s*', lat_long_str)]
            if tuple(lat_long) not in coordenadasLidas:
                coordenadasLidas.append(tuple(lat_long))
    return coordenadasLidas

marcadorDeBoia([-27.28, -48.57], bvd, verde, flag, grupoVerde)
marcadorDeBoia([-27.280, -48.434], bv, laranja, flag, grupoLaranja)
marcadorDeBoia([-27.208, -48.533], bp, preto, flag, grupoPreto)

marcadorDeBoia([-27.6017447,-48.5176886], br, roxo, flag, grupoPreto) #marcador na UFSC

listaCoordenadasBoia = criaListaDeCoordenadas(caminhoArquivoLaranja)
marcadorDeBoia(listaCoordenadasBoia[0], bl, vermelho, flag, grupoVermelho)
trilhaDaBoia(listaCoordenadasBoia, bl, vermelho, grupoVermelho)


folium.FitOverlays(fly=True).add_to(mapa) #centrar nos marcadores 
folium.LayerControl().add_to(mapa)
mapa.save('mapaFlorianopolis.html')