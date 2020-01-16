# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 22:16:26 2019

@author: arthurd
"""

import os
import json

from utils import io
import core.nctrack as nc
import dbconnect as dbc
import core.model.stats as sts


def main(file, properties=None, out_dirname=".", method="nearest", db_file='database.db', log=True):
    
    if not properties:
        raise Exception ("Length of files and properties should match.")
        
    # Connecting to the database
    conn = dbc.connect(db_file)
    
    
    
    for i in range(len(files)):              
        # Extract the track informations
        file = files[i]
        name = file.split("\\")[-1].split(".")
        filename = name[0]
        ext = name[1]
        # Extract the meta.properties informations
        file_props = properties[i]
   
        # Open the geojson
        with open(file) as f:
            geojson = json.load(f)
            
        if log:
            print("========================")
            print("track : {0}, track size : {1}".format(filename, len(geojson)))
               
        # Convert in dataframe
        df = io.geojson_to_df(geojson, extract_coordinates=True)
        df_corr = nc.correct_track(df)
        
        df_props = io.properties_to_df(file_props)
        df_props.insert(loc=0, column='track_id', value=[filename])
        
        if log:
            print("------------------------")
            print("stats {0}".format(method))
            print(sts.global_stats(df_corr[['proj_length', 'path_length', 'unlinked', 'proj_accuracy']]))
        
        
        # Convert back to geojson  
        properties = [key for key in df_corr]
        properties.remove('type')
        properties.remove('longitude')
        properties.remove('latitude')
        properties.remove('elevation')
        gj = io.df_to_geojson(df_corr, properties, geometry_type='type', 
                              lat='latitude', lon='longitude', z='elevation')
            
        # test if the out directory exists
        directory = out_dirname + '/track_' + method
        outname = directory + '/' + filename + '_' + method + '.' + ext
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        # write the geojson
        with open(outname, 'w') as f:
            json.dump(gj, f)
        
        # Create and add to the database            
        if i == 0:
            dbc.create_table_from_df(conn, 'point', df_corr)
            dbc.create_table_from_df(conn, 'meta', df_props)
        dbc.df_to_table(conn, 'point', df_corr)
        dbc.df_to_table(conn, 'meta', df_props)
            
    # closing the database
    conn.close()

if __name__ == "__main__":
    print("\n\t-----------------------\n",
            "\t       Matching\n\n")
    
# =============================================================================
#     1/ Read all the Geojson files
# =============================================================================
    print("1/ Reading the files")
    files = io.open_files("../data/track")
    # files = files[:10]
    print(files[23:])
    files = [files[0]]
    
    properties = io.open_files("../data/track", ext="properties")
    # files = files[:10]
    print(properties[23:])
    props = [properties[0]]
    
# =============================================================================
#     2/ Map matching
# =============================================================================
    print("2/ Map Matching")
    main(files, properties=props, out_dirname='../data', method='hmm', db_file='../database/database_hmm_test.db', log=True)








