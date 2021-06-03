#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import gif
import json
import tqdm
import geopy
import warnings
import requests
import seaborn as sns
import pandas as pd
import numpy as np
from tqdm import tqdm

warnings.filterwarnings('ignore')


# In[2]:


def pre_process_data(path):
    """Returns a dictionary of dataframes per file"""
    data_dictio = {}
    p = re.compile('Y\d{4}')
    
    print('Start reading files...')
    # to combine list of lists into one list | listception
    years = [j for i in [p.findall(x) for x in os.listdir(path)] for j in i] 
    
    for f in tqdm(range(len(os.listdir(path)))):
        data_dictio[years[f]] = (pd.read_csv(path + '/' + os.listdir(path)[f])
                                 .rename(columns={'t': 'year', 'k': 'hscode',
                                                  'i':'exporter', 'j':'importer', 
                                                  'v':'value_kUSD', 
                                                  'q':'quantity_mtons'}))
    print('Reading files completed...')
    print('Start getting Country Code and HS Codes online...')
    
    #country code
    r_cc1 = (requests.get('https://comtrade.un.org/data/cache/reporterAreas.json')
             .json())
    r_cc2 = (requests.get('https://comtrade.un.org/data/cache/partnerAreas.json')
             .json())
    #product code
    r_pc = requests.get(r'https://comtrade.un.org/data/'
                        r'cache/classificationH0.json').json()
    
    # Converting details into a dictionary
    country_code1 = {int(code['id']):code['text'] for code 
                    in r_cc1['results'][1:-2]} 
    country_code2 = {int(code['id']):code['text'] for code 
                    in r_cc2['results'][1:-2]} 
    country_code = {**country_code1, **country_code2}
    
    prod_code = {int(prod['id']):prod['text'] for prod in r_pc['results'][5:-2]}
    
    print('Getting Country Code and HS Codes online completed...')
    print('Start mapping Country Code and HS Codes to each df...')
    
    # Converting ISO 3166 Codes to Country Name
    for year in tqdm(data_dictio.keys()):
        for role in ['exporter', 'importer']:
            data_dictio[year][role] = data_dictio[year][role].map(country_code)
    
    # Getting the Section Names of the HS Code
    for year in tqdm(data_dictio.keys()):
        hs_section = []
        data_dictio[year]['hscode'] = data_dictio[year]['hscode'].astype(str)
        for x in data_dictio[year]['hscode']:
            if len(list(x)) == 6:
                hs_section.append(x[:2])
            elif len(list(x)) == 5:
                hs_section.append('0' + x[:1])
        data_dictio[year]['hs_chap'] = pd.Series(hs_section).astype(int)
        data_dictio[year]['section'] = pd.cut(data_dictio[year]['hs_chap'], 
                                              bins=[0, 5, 14, 15, 24, 27, 38, 40, 
                                                    43, 46, 49, 63, 67, 70, 71, 
                                                    83, 85, 89, 92, 93, 95, 97],
                                              labels=['Live animals; animals products', 
                                                      'Vegetable products', 
                                                      'Animal or vegetable fats and oils',
                                                      'Prepared foodstuffs; beverages, spirits; tobacco', 
                                                      'Mineral products',
                                                      'Products of the chemical or allied industries', 
                                                      'Plastics, rubber, articles thereof',
                                                      'Raw Hides, Skins, Leather', 
                                                      'Wood, articles of wood',
                                                      'Pulp of Wood, Paper', 
                                                      'Textiles and textile articles', 
                                                      'Footwear, headgear, etc.', 
                                                      'Articles of stone, plaster, cement, ceramics, glass', 
                                                      'Pearls, precious stones, precious metals', 
                                                      'Base metals and articles of base metal', 
                                                      'Machinery and mechanical appliances; electrical equipment', 
                                                      'Vehicles, aircraft, vessels', 
                                                      'Precisions Instruments', 
                                                      'Arms and ammunition', 
                                                      'Miscellaneous manufactured articles',
                                                      "Works of art, collectors' pieces and antiques"])
        
        data_dictio[year]['hs_sec'] = pd.cut(data_dictio[year]['hs_chap'], 
                                             bins=[0, 5, 14, 15, 24, 27, 38, 40, 
                                                   43, 46, 49, 63, 67, 70, 71, 
                                                   83, 85, 89, 92, 93, 95, 97],
                                             labels=list(range(1,22)))
        
    print('Mapping Country Code and HS Codes to each df completed...')
    print('Start getting Lat/long for each country...')
        
    # Get unique countries for exporter and importer
    exp = []
    imp = []
    for year in tqdm(data_dictio.keys()):
        exp1 = data_dictio[year]['exporter'].tolist()
        imp1 = data_dictio[year]['importer'].tolist()
        exp = exp + exp1
        imp = imp + imp1
    exp_list = set(exp)
    imp_list = set(imp)
    
    # Getting the Lat/Long of Exporting and Importing country and Save it to a Dictionary
    geolocator = geopy.geocoders.Nominatim(user_agent="bansa_explorer")
    
    exp_coord = {}
    imp_coord = {}
    for ec in tqdm(exp_list):
        try:
            co = geolocator.geocode(ec)
            exp_coord[ec] = {'latitude': co.latitude,
                             'longitude': co.longitude}
        except:
            exp_coord[ec] = np.nan
        
    for ic in tqdm(imp_list):
        try:
            co = geolocator.geocode(ic)
            imp_coord[ic] = {'latitude': co.latitude,
                             'longitude': co.longitude}
        except:
            exp_coord[ic] = np.nan
    
    for year in tqdm(data_dictio.keys()):
        data_dictio[year]['exp_coord'] = (data_dictio[year]['exporter']
                                          .map(exp_coord))
        data_dictio[year]['imp_coord'] = (data_dictio[year]['importer']
                                          .map(imp_coord))
        
    print('Mapping lat/long for each country in df completed...')
        
    return data_dictio


# In[ ]:




