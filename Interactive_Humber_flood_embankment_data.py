# Create an interactive map displaying various Humber flood embankment data

# import necessary modules
import pandas as pd
import geopandas as gpd
import folium

# The Flood Areas shapefile will provide the multi-polygon shape on which all other data will be spatially located;
# note that this and subsequent shapefiles are loaded using Geopandas, which associates each with a GeoDataFrame;
# GeoDataFrame - tabular data structure, adds 'geometry' column to the shaoefile attribute table.
areas = gpd.read_file('HSCR_Flood_Areas/HSCR_FloodAreas_2080406.shp')

# # see a subset of the first 5 lines, the key column is UNIT and the multi-polygon will be visualised on this basis;
# note the additional 'geometry' column, as this is a GeoDataFrame.
areas.head()

# To create an interactive leaflet map, use geopandas.GeoDataFrame.explore
# for more info see https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.explore.html
# Using UNIT column to visualise the multi-polygon; colour is chosen from matpoltlib's Qualitative colormaps selection
# for more info see https://matplotlib.org/stable/tutorials/colors/colormaps.html
m = areas.explore('UNIT', cmap='Accent')

# open flood embankment network polylines shapefile; contains all the earth flood defence embankments around the Humber
defences = gpd.read_file('Flood_embankment_network/Embankment_alignment_Humber_primary.shp')

# open a sub-set of the data, 'Type' is the column with witch the data will be added to map.
defences.head()

# add the defence shapefile to the map; note: basemap is OpenStreetMap.
defences.explore( 'Type',
                 m=m, # adds markers to map
                 marker_type='marker', # specify type of marker
                 popup=True, # enter true or false based on preference for popup on map
                 legend=True, # enter true or false based on preference for inclusion of separate legend
                 legend_kwds={'caption': 'Flood Defence Embankments'}, # set the caption wording
                 cmap='Dark2' # set the colour
                )


# open low sections polyline shapefile; contains LIDAR-derived data of where flood embankments are lower in height
# than adjacent sections and could present a flood risk from overtopping during storm events when water levels are high.
Low_sections = gpd.read_file('LIDAR_derived_data/Embankment_low_sections_defects.shp')

# open subset of data, key column is 'Type'
Low_sections.head()

# add the low sections to the existing map
Low_sections.explore( 'Type',
                    m=m,
                 marker_type='marker',
                 popup=True,
                 legend=True,
                 legend_kwds={'caption': 'Low sections'},
                 cmap='Set1'
                )

# open steep slopes polygon shapefile; contains LIDAR-derived data of where flood embankments slopes, either front (facing the water) or rear (facing the land),
# are steeper than the standard angle of repose and could theoretically affect the long-term stability of the embankments
Steep_slopes = gpd.read_file('LIDAR_derived_data/Embankment_steep_slope_anomalies.shp')

# open subset of data, key column is 'Face'
Steep_slopes.head()

# add steep slopes to the map
Steep_slopes.explore( 'Face',
                 m=m, #
                 marker_type='marker',
                 popup=True,
                 legend=True,
                 legend_kwds={'caption': 'Steep slopes'},
                 cmap='tab20b'
                )

# open palaeochannels point data shapefile; contains LIDAR-derived data of where infilled former channels, either natural
# or engineered are situated directly below earth embankments and may theoretically affect the structural stability.
Palaeochannels = gpd.read_file('LIDAR_derived_data/Palaeochannel_anomalies_intersect_embank.shp')

# open subset of data, key column is 'channel'
Palaeochannels.head()

Palaeochannels.explore( 'channel',  # note, marker type is omitted so that default circle is loaded
                 m=m,
                 popup=True,
                 legend=True,
                 legend_kwds={'caption': 'Palaeochannels'},
                 cmap='tab10'
                )

# open geophysical survey polyline shapefile; contains interpreted data from DEMP (Dipole Electromagnetic Profiling)
# as to the material composition of surveyed flood embankments, which provide geotechnical context to assessments.
Geophysical_survey_embankment_materials = gpd.read_file('Geophysical_survey_data_material_composition/Geophysical_survey_embankment_materials.shp')

# open subset of data, the key column is 'Material'
Geophysical_survey_embankment_materials.head()

# add the geophysical survey data to the map
Geophysical_survey_embankment_materials.explore( 'Material',
                 m=m,
                 marker_type='marker',
                 popup=True,
                 legend=True,
                 legend_kwds={'caption': 'Material'},
                 cmap='Dark2'
                )

# the interactive map is complete; note that the different legends may overlap spatially but can be moved using the mouse;
# now save the map as an html file
m.save('Interactive_Humber_flood_embankment_data.html')