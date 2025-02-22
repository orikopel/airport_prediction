import pandas as pd

import folium
import geopandas as gpd
from shapely.ops import split
from shapely.geometry import LineString, MultiLineString


def create_marker_with_label(location, label, traffic):
    """
    Create a marker with a label and traffic information.
    Args:
        location (tuple): The latitude and longitude of the marker.
        label (str): The label to display on the marker.
        traffic (str): The traffic information to display on the marker.
    Returns:
        folium.FeatureGroup: A FeatureGroup containing the marker and text label.
    """

    # Create the default location icon
    icon = folium.Icon(color="blue", icon="info-sign")

    # Create a DivIcon for the text label
    text_icon = folium.features.DivIcon(
        icon_size=(150, 36),
        icon_anchor=(7, 0),  # Adjust to position text next to the default icon
        html='<div style="font-size: 12pt; color: white;">%s<br>Predicted Traffic: %s</div>' % (label, traffic),
    )

    # Create a FeatureGroup to combine the icon and text
    fg = folium.FeatureGroup()
    marker = folium.Marker(location=location, icon=icon).add_to(fg)
    text_marker = folium.Marker(location=location, icon=text_icon).add_to(fg)

    return fg

def make_line(locations_df):
    """
    create a line between location points
    """

    # extract locations
    point1, point2 = locations_df["geo"].tolist()

    # create linestring between locations
    line = LineString([point2, point1])

    # Split the line if it crosses the antimeridian
    if line.crosses(LineString([(180, -90), (180, 90)])):
        split_line = split(line, LineString([(180, -90), (180, 90)]))
        line = MultiLineString(split_line.geoms)  # Create a MultiLineString

    # create line object
    gdf = gpd.GeoDataFrame(geometry=[line], crs="EPSG:4326")

    return gdf

def make_locations(m, locations_df):
    """
    create location point and add to map
    """

    # extract locations
    point1, point2 = locations_df["geo"].tolist()

    # extract location names
    name1, name2 = locations_df["name"].tolist()

    # extract location traffics
    traffic1, traffic2 = locations_df["traffic"].tolist()

    #
    m.add_child(create_marker_with_label([point1[1], point1[0]], name1, traffic1))
    m.add_child(create_marker_with_label([point2[1], point2[0]], name2, traffic2))

    return m

def make_map(locations_df):
    """
    create an interactive map for the route
    """

    # make line between locations
    line = make_line(locations_df)

    # Create a map centered on the midpoint of the line
    point1, point2 = locations_df["geo"].tolist()
    midpoint = [(point1[1] + point2[1]) / 2, (point1[0] + point2[0]) / 2]
    m = folium.Map(location=midpoint, zoom_start=3, tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', attr='Esri')

    # Add the line to the map
    folium.GeoJson(line).add_to(m)

    # add location points
    m = make_locations(m , locations_df)

    # Make the map interactive
    m.add_child(folium.LatLngPopup())

    return m
