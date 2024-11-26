import streamlit as st
import osmnx as ox
import networkx as nx
import folium
from folium import plugins

# Lista de fincas para elegir
fincas = [
    {"nombre": "Finca El Encanto", "lat": 1.23, "lon": -77.25},
    {"nombre": "Finca La Esperanza", "lat": 1.3, "lon": -77.35},
    {"nombre": "Finca Buenavista", "lat": 1.5, "lon": -77.4},
    {"nombre": "Finca El Vergel", "lat": 1.7, "lon": -77.5},
    {"nombre": "Finca La Primavera", "lat": 1.8, "lon": -77.6}
]

# Lista de puntos de venta para elegir
puntos_venta = [
    {"nombre": "Supermercado Central", "lat": 1.45, "lon": -77.45},
    {"nombre": "Centro Comercial San Juan", "lat": 1.35, "lon": -77.5},
    {"nombre": "Mercado El Progreso", "lat": 1.5, "lon": -77.6},
    {"nombre": "Supermercado La Esperanza", "lat": 1.55, "lon": -77.65},
    {"nombre": "Tienda Especial Nariño", "lat": 1.6, "lon": -77.7}
]

# Función para mostrar el mapa de producción


def mostrar_mapa_produccion():
    mapa = folium.Map(location=[1.287, -77.28], zoom_start=8)
    for finca in fincas:
        folium.Marker(
            location=[finca["lat"], finca["lon"]],
            popup=f"{finca['nombre']}",
            icon=folium.Icon(color="green", icon="leaf")
        ).add_to(mapa)
    return mapa

# Función para mostrar el mapa de comercialización


def mostrar_mapa_ventas():
    mapa = folium.Map(location=[1.287, -77.28], zoom_start=8)
    for venta in puntos_venta:
        folium.Marker(
            location=[venta["lat"], venta["lon"]],
            popup=f"{venta['nombre']}",
            icon=folium.Icon(color="orange", icon="shopping-cart")
        ).add_to(mapa)
    return mapa

# Función para mostrar el mapa de rutas de distribución basadas en vías reales


def mostrar_mapa_rutas(origen, destino):
    G = ox.graph_from_place("Nariño, Colombia", network_type="drive")

    # Encontrar los nodos más cercanos a las coordenadas de origen y destino
    nodo_origen = ox.distance.nearest_nodes(G, origen[1], origen[0])
    nodo_destino = ox.distance.nearest_nodes(G, destino[1], destino[0])

    # Calcular la ruta más corta en función de la distancia
    ruta = nx.shortest_path(G, nodo_origen, nodo_destino, weight='length')

    # Obtener las coordenadas de la ruta
    ruta_coords = [(G.nodes[n]['y'], G.nodes[n]['x']) for n in ruta]

    # Crear el mapa de la ruta
    mapa_ruta = folium.Map(location=origen, zoom_start=10)

    # Dibujar la ruta sobre el mapa
    folium.PolyLine(ruta_coords, color="blue", weight=2.5,
                    opacity=1).add_to(mapa_ruta)

    # Marcar los puntos de origen y destino
    folium.Marker(origen, popup="Finca de Origen",
                  icon=folium.Icon(color="green")).add_to(mapa_ruta)
    folium.Marker(destino, popup="Destino", icon=folium.Icon(
        color="orange")).add_to(mapa_ruta)

    return mapa_ruta


# Crear la aplicación Streamlit
st.title("Plataforma de Producción y Comercialización de Café")

# Pestañas
tabs = st.radio("Selecciona una opción", [
                "Producción", "Comercialización", "Ruta de Distribución"])

if tabs == "Producción":
    st.header("Mapa de Producción")
    mapa_produccion = mostrar_mapa_produccion()
    st.markdown(mapa_produccion._repr_html_(), unsafe_allow_html=True)

elif tabs == "Comercialización":
    st.header("Mapa de Comercialización")
    mapa_ventas = mostrar_mapa_ventas()
    st.markdown(mapa_ventas._repr_html_(), unsafe_allow_html=True)

elif tabs == "Ruta de Distribución":
    st.header("Ruta de Distribución")
    # Selección de finca de origen
    finca_origen_opcion = st.selectbox("Selecciona la finca de origen", [
                                       finca["nombre"] for finca in fincas])
    finca_origen = next(
        finca for finca in fincas if finca["nombre"] == finca_origen_opcion)

    # Selección de punto de venta de destino
    destino_venta_opcion = st.selectbox("Selecciona el punto de venta de destino", [
                                        venta["nombre"] for venta in puntos_venta])
    destino_venta = next(
        venta for venta in puntos_venta if venta["nombre"] == destino_venta_opcion)

    # Mostrar la ruta
    mapa_ruta = mostrar_mapa_rutas(
        (finca_origen['lat'], finca_origen['lon']), (destino_venta['lat'], destino_venta['lon']))
    st.markdown(mapa_ruta._repr_html_(), unsafe_allow_html=True)
