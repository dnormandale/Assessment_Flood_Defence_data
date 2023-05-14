# Humber flood embankment analysis

# A suite of shapefile data for understanding spatial distribution of available LIDAR and Geophysical
# survey-derived geotechnical data for engineered flood defence embankments on the Humber estuary, England.



import os
import geopandas as gpd
import matplotlib.pyplot as plt
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
# these are modules that require importing


# generates a legend to be populated by the datesets later;
# for more info see https://matplotlib.org/stable/tutorials/intermediate/legend_guide.html
def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles

# set up the scale bar in preparation for finalised map, based on scale of Humber estuary, 20km fits best
# for for info see https://stackoverflow.com/q/32333870 and also https://stackoverflow.com/a/35705477
def scale_bar(ax, location=(0.92, 0.95)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 20000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx-10000, sbx - 20000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby-4500, '20 km', transform=ax.projection, fontsize=10)
    ax.text(sbx-12500, sby-4500, '10 km', transform=ax.projection, fontsize=10)
    ax.text(sbx-24500, sby-4500, '0 km', transform=ax.projection, fontsize=10)

    # open Flood Areas polygon shapefile as this will be the basemap for subsequent data;
    # note that this and subsequent shapefiles are loaded using Geopandas, which associates each with a GeoDataFrame;
    # GeoDataFrame - tabular data structure, adds 'geometry' column to the shaoefile attribute table.
    areas = gpd.read_file('HSCR_Flood_Areas/HSCR_FloodAreas_2080406.shp')

    # see a subset of the first 5 lines, the key column is FloodArea_ and basemap will be rendered on this basis;
    # note the additional 'geometry' column, as this is a GeoDataFrame.
    areas.head(5)

    # open flood embankment network polylines shapefile; contains all the earth flood defence embankments around the Humber
    defences = gpd.read_file('Flood_embankment_network/Embankment_alignment_Humber_primary.shp')

    # open low sections polyline shapefile; contains LIDAR-derived data of where flood embankments are lower in height
    # than adjacent sections and could present a flood risk from overtopping during storm events when water levels are high
    Low_sections = gpd.read_file('LIDAR_derived_data/Embankment_low_sections_defects.shp')

    # open steep slopes polygon shapefile; contains LIDAR-derived data of where flood embankments slopes, either front (facing the water) or rear (facing the land),
    # are steeper than the standard angle of repose and could theoretically affect the long-term stability of the embankments
    Steep_slopes = gpd.read_file('LIDAR_derived_data/Embankment_steep_slope_anomalies.shp')

    # open palaeochannels point data shapefile; contains LIDAR-derived data of where infilled former channels, either natural
    # or engineered are situated directly below earth embankments and may theoretically affect the structural stability
    Palaeochannels = gpd.read_file('LIDAR_derived_data/Palaeochannel_anomalies_intersect_embank.shp')

    # open geophysical survey polyline shapefile; contains interpreted data from DEMP (Dipole Electromagnetic Profiling)
    # as to the material composition of surveyed flood embankments, which provide geotechnical context to assessments
    Geophysical_survey_bank_materials = gpd.read_file(
        'Geophysical_survey_data_material_composition/Geophysical_survey_embankment_materials.shp')

    # now the key datasets are opened, comparative analysis can be started; first on the defence, see subset of columns, rows
    # in the GeoDataFrame.
    defences.head(5)

    # to establish the linear length of earth embankment flood defences on the Humber estuary and main tidal tributary
    # rivers, the 'Shape_Leng' column is totalled up in metres and converted to kilometres (divide by 1000).
    defences['Shape_Leng'].sum() / 1000

    # the next dataset to be compared is the low sections; see subset of the data and note again a 'Shape_Leng' column
    Low_sections.head(5)

    # sum and convert to km
    Low_sections['Shape_Leng'].sum() / 1000

    # find low sections linear length as a percentage of defences to understand the scale of this type of this issue.
    # output should be 1.5% rounded up, so an issue which only affects a tiny proportion of the embankments.
    Low_sections['Shape_Leng'].sum() / defences['Shape_Leng'].sum() * 100

    # Steep slopes is a polygonal dataset; in this instance Shape_Leng refers to the perimeter of each polygon in the dataset,
    # rather than the linear length of embankment which is affected; Shape_Area does not relate to linear length either.
    Steep_slopes.head(5)

    # Alternative analysis can be carried out on how many of these occurrences are present.
    Steep_slopes['Face'].count()

    # There are over 4000 instances, more context can be derived from understanding which face (slope) of the embankments
    # are affected, the subset of the GeoDataframe above just indicated 'front' but a check can be carried out to
    # establish whether rear slopes are also listed.
    type_Steep_slopes = list(Steep_slopes.Face.unique())
    print('Name of unique features: {}'.format(type_Steep_slopes))

    # Calculate how many of the 4029 are affecting the front slope/face
    Steep_slopes[Steep_slopes['Face'] == 'Front'].count()

    # Calculate how many are affecting the rear slope/face
    Steep_slopes[Steep_slopes['Face'] == 'Rear'].count()

    # Calculate the instances of rear slope/face as a percentage of the total instance and by deduction,
    # the remaining percentage of front slope: 74.3 % rear (to 1 d.p) and 25.7 % front.
    2995 / 4029 * 100

    # See a subset of the Palaeochannels point data; the key column for further analysis is 'Class'.
    Palaeochannels.head(5)

    # Given the data are points, linear length calculation is not applicable; instead calculate instances.
    Palaeochannels['Class'].count()

    # 53 palaeochannels are identified in the data; define how many descriptive types there are.
    num_Palaeochannels = len(Palaeochannels.channel.unique())
    print('Number of unique features: {}'.format(num_Palaeochannels))

    # List the names of these 2 unique features.
    type_Palaeochannels = list(Palaeochannels.channel.unique())
    print('Name of unique features: {}'.format(type_Palaeochannels))

    # Calculate how many of the overall 53 are classed as 'depression'
    # 'depression' means a palaeochannel is lower in elevation than the surrounding land, as identified in LIDAR analysis.
    Palaeochannels.loc[Palaeochannels['channel'] == 'Depression'].count()

    # Calculate 49 depressions as a % of total 53 palaeochannels; answer is 92.5% (1 d.p), therefore 'extrusions'
    # where a palaeochannel is higher in elevation than the surrounding land constitute 7.5% of the total.
    49 / 53 * 100

    # Final data to analyse are the geophysical survey results; note there are a significant number of columns (27).
    Geophysical_survey_bank_materials.head(5)

    # List the column headings to aid appreciation of what data are included.
    Geophysical_survey_bank_materials.columns

    # Now establish the number of features i.e. the rows.
    rows, cols = Geophysical_survey_bank_materials.shape
    print('Number of features: {}'.format(rows))

    # Calculate the linear distance of survey conducted, using 'Tot_dist_m' which accurately reflects the actual length of
    # survey undertaken, rather than 'Shape_leng', which is a measure of the polyline lengths. Convert to km.
    Geophysical_survey_bank_materials['Tot_dist_m'].sum() / 1000

    # As these data are linear, a percentage calculation can be made in respect to the overall lemgth of earth embankments;
    # 37.2 % (to 1 d.p) has been surveyed, leaving 62.3 % available for future survey.
    Geophysical_survey_bank_materials['Tot_dist_m'].sum() / defences['Shape_Leng'].sum() * 100

    # The geophysical results have been interpreted in respect of the types of material within the embankments;
    # Create a list of all these material types;
    # Material types are based on four standard material types - clay, silt, sand, gravel. Where any of these materials
    # are considered the dominant constiuents, the name is shown in upper case, with lesser constituents in lower case.
    type_materials = list(Geophysical_survey_bank_materials.Material.unique())
    print('Name of unique features: {}'.format(type_materials))

    # Flood embankments should optimally be constructed from finer-grained, cohesive materials - clays and silts;
    # Where coarser-grained, less cohesive (and therefore more permeable) materials predominate there is theoretically
    # a greater risk of seepage of water through an embankment body and possibly also increased settlement of the crest
    # height as there are moe micro voids in coarser-grained materials;
    # This analysis, by linear length of material types will give a valuable overview.
    Geophysical_survey_bank_materials.groupby(['Material'])['Tot_dist_m'].sum() / 1000

    # The inherent saturation levels of the flood embankments is also a key factor in understanding embankment effectivness;
    # 'High' saturation indicates waterlogging,which is sub-optimal, as is 'Low' , which indicates excessive permeability;
    # By definition 'Normal' is optimal and from this analysis is the dominant Saturation type - 85 of 125 km.
    Geophysical_survey_bank_materials.groupby(['Saturation'])['Tot_dist_m'].sum() / 1000

    # To understand the spatial coverage of geophysical survey, data can be grouped by Hydraulic Units, into which the
    # Humber estuary interest area is sub-divided based on it's hydraulic functioning in times of flood.
    # Calculate and convert to km.
    Geophysical_survey_bank_materials.groupby(['HS_Hyd_Uni'])['Tot_dist_m'].sum() / 1000

    # Calculate the number of Hydraulic Units in which geophysical survey was carried out.
    num_Units_surveyed = len(Geophysical_survey_bank_materials.HS_Hyd_Uni.unique())
    print('Number of unique features: {}'.format(num_Units_surveyed))

    # Create the full list of Hydraulic Units on the Humber, based on the Areas GeoDataFrame.
    full_list_Units = list(areas.UNIT.unique())
    print('Name of unique features: {}'.format(full_list_Units))

    # Count the total number of Hydraulic Units
    # There are 15, therefore geophysical survey has been carried out in 10 of 15.
    num_Units = len(areas.UNIT.unique())
    print('Number of unique features: {}'.format(num_Units))

    # Create map displaying above data

    myFig = plt.figure(figsize=(16, 16))  # creates figure with definied dimensions in inches

    myCRS = ccrs.OSGB()  # Set the CartoPy Coordinate reference system to the Ordnance Survey Great Britain to ensure
    # compatibility with all the datasets.

    ax = plt.axes(projection=myCRS)  # create axes using the OSGB projection.

    # Add the Areas basemap, edged in light grey and with a white face colour.
    areas_feature = ShapelyFeature(areas['geometry'], myCRS, edgecolor='lightgray', facecolor='w')
    xmin, ymin, xmax, ymax = areas.total_bounds
    # Add this feature to the map
    ax.add_feature(areas_feature)

    # set the zoom extent to match the basemap shapefile extent with a 10km buffer on the x and y axes
    ax.set_extent([xmin - 10000, xmax + 10000, ymin - 10000, ymax + 10000], crs=myCRS)

    myFig  # draw the updated map

    # To colour in the Areas basemap, the number of colours required will be the total Flood Area features.
    num_areas = len(areas.FloodArea_.unique())
    print('Number of unique features: {}'.format(num_areas))

    # choose 35 colours from here https://matplotlib.org/stable/gallery/color/named_colors.html
    areas_colors = ['sandybrown', 'bisque', 'tan', 'moccasin', 'floralwhite', 'gold', 'darkkhaki',
                    'lightgoldenrodyellow', 'olivedrab', 'chartreuse', 'palegreen', 'mediumspringgreen',
                    'lightseagreen', 'paleturquoise', 'darkturquoise', 'deepskyblue', 'mediumpurple', 'darkorchid',
                    'plum', 'm', 'palevioletred', 'lightgray', 'lightcoral', 'mistyrose', 'peachpuff', 'navajowhite',
                    'orange', 'lemonchiffon', 'yellowgreen', 'c', 'skyblue', 'violet', 'fuchsia', 'indianred', 'salmon',
                    'y']

    # list and sort the areas
    area_numbers = list(areas.FloodArea_.unique())
    area_numbers.sort()

    # set more parameters as arguments, including the geometry (from the GeoDataFrame), edge colour, line width
    # and transparency (alpha - on a scale 0 to 1); face colour is set to the listed colours above.
    for ii, name in enumerate(area_numbers):
        feat = ShapelyFeature(areas.loc[areas['FloodArea_'] == name, 'geometry'],
                              myCRS,
                              edgecolor='w',
                              facecolor=areas_colors[ii],
                              linewidth=0.1,
                              alpha=0.25)
        ax.add_feature(feat)  # add features to map

    myFig  # draw updated map

    # Add defences in the same way
    defences = ShapelyFeature(defences['geometry'],
                              myCRS,
                              edgecolor='b',  # blue
                              linewidth=2.0,
                              alpha=0.25
                              )
    ax.add_feature(defences)  # add features to the map

    myFig  # draw updated map

    # Add geophysical survey data
    Geophysical_survey_bank_materials = ShapelyFeature(Geophysical_survey_bank_materials['geometry'],
                                                       myCRS,
                                                       edgecolor='lime',
                                                       linewidth=1.0,
                                                       )
    ax.add_feature(Geophysical_survey_bank_materials)

    myFig

    # Add low sections data
    Low_sections = ShapelyFeature(Low_sections['geometry'],
                                  myCRS,
                                  edgecolor='darkorange',
                                  linewidth=1.0)
    ax.add_feature(Low_sections)

    myFig

    # Add Steep slopes, note as these data are polygons, the facecolor needs to be set
    Steep_slopes = ShapelyFeature(Steep_slopes['geometry'],
                                  myCRS,
                                  edgecolor='k',  # black
                                  facecolor='k',  # due to scale of map, a separate colour will not be discernible
                                  linewidth=0.1)
    ax.add_feature(Steep_slopes)

    myFig

    # Palaeochannels are point data so do not need the ShapelyFeature class from cartopy.feature, ax.plot can be used directly.

    Palaeochannels_handle = ax.plot(Palaeochannels.geometry.x, Palaeochannels.geometry.y, 'o', color='0.7', ms=3,
                                    transform=myCRS)
    # 'o' is circle, courtesy of list here https://stackoverflow.com/questions/8409095/set-markers-for-individual-points-on-a-line
    # colour is String representation of float value in closed interval [0, 1] for grayscale values, os 0.7 is light grey
    # see https://matplotlib.org/stable/tutorials/colors/colors.html

    myFig

    # Use generate-handles function to add labels and colours. Note - Areas is omitted for visual clarity, given there
    # are 35 areas.

    defences_handle = generate_handles(['Flood embankments'], ['b'], alpha=0.25)

    Low_sections_handle = generate_handles(['Low sections of embankments'], ['darkorange'])

    Steep_slopes_handle = generate_handles(['Steep embankment slopes'], ['k'])

    Palaeochannels_handle = generate_handles(['Palaeochannel intersections'], ['chocolate'])

    Geophysical_survey_bank_materials_handle = generate_handles(['Geophysical survey extents'], ['lime'])

    # generate legend content and parameters
    # for more info see https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html

    handles = defences_handle + Low_sections_handle + Steep_slopes_handle + Palaeochannels_handle + Geophysical_survey_bank_materials_handle  # use '+' to concatenate (combine) lists
    labels = ['Flood embankments', 'Low sections of embankments', 'Steep embankment slopes',
              'Palaeochannel intersections', 'Geophysical survey extents']

    leg = ax.legend(handles, labels, title='Legend', title_fontsize=14,
                    fontsize=12, loc='upper left', frameon=True, framealpha=1)

    myFig

    # now add scale bar which was previously specified
    scale_bar(ax)

    myFig

    # save the map to the current folder in png format; also specify no border (bbox) and resolution in dpi (dots per inch).
    myFig.savefig('Humber_flood_embankment_data.png', bbox_inches='tight', dpi=800)
