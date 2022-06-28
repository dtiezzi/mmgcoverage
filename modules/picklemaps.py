import pickle
from brmaps import *
from ufIbge import UfBr
from loadfiles import LoadFiles
import pandas as pd
import json
import os

uf_dic = UfBr().state_dict
uf_names_dic = UfBr().state_name_dict
uf_area_dic = UfBr().state_area_dict
uf_area_dic = {k: 1 - (uf_area_dic[k] - min(uf_area_dic.values())) / (max(uf_area_dic.values()) - min(uf_area_dic.values())) for k in uf_area_dic}

states, counties = LoadFiles(['/var/www/mmgcov.com/_geojson/brstates.geojson', '/var/www/mmgcov.com/_geojson/br_mun_all.json']).loadjson()
st_df, ct_df = LoadFiles(['/var/www/mmgcov.com/csv/Supplemental_table_states_data.csv', '/var/www/mmgcov.com/csv/Supplemental_table_municipality_data.csv']).loadcsv()

## Filt columns
st_df = st_df[['ibge_uf_id','uf', 'avg_mmg_coverage_50_69_ans_adj','avg_mmg_coverage_40_49_ans_adj','ebc_det_ratio_50_69','ebc_det_ratio_40_49', 'avg_population']]
ct_df = ct_df[['uf', 'name_uf', 'ibge_munic_id', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_50_69', 'ebc_det_ratio_40_49', 'total_number_mmg_50_69', 'total_number_mmg_40_49', 'avg_population']]

figBr1 = plotmapCounties(ct_df, counties, ctitle='Mammogram coverage 2010-2019 (50-70 years)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'])
figBr2 = plotmapCounties(ct_df, counties, ctitle='Mammogram coverage 2010-2019 (40-50 years)', colname='mmg_coverage_40_49_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_40_49'], age=40)
#divBr1 = figBr1.to_html(full_html=False)
#divBr2 = figBr2.to_html(full_html=False)

with open('../pickle_files/figBr1.pickle', 'wb') as f:
    pickle.dump(figBr1, f)

with open('../pickle_files/figBr2.pickle', 'wb') as f:
    pickle.dump(figBr2, f)
