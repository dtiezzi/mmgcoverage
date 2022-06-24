from flask import Flask, render_template, redirect
from modules.brmaps import *
from modules.ufIbge import UfBr
from modules.loadfiles import LoadFiles
import pandas as pd
import json
import os

app = Flask(__name__)

app.static_folder = 'static'

uf_dic = UfBr().state_dict
LoadFiles(['_geojson/brstates.geojson', '_geojson/br_mun_all.json']).loadjson()
LoadFiles(['csv/Supplemental_table_states_data.csv', 'csv/Supplemental_table_municipality_data.csv']).loadcsv()

geofileST = '_geojson/brstates.geojson'
geofileCT = '_geojson/br_mun_all.json'

DATA_STATES = "csv/Supplemental_table_states_data.csv"
DATA_MUNICIP = "csv/Supplemental_table_municipality_data.csv"
st_df = pd.read_csv(DATA_STATES, index_col=False)
st_df = st_df[['ibge_uf_id','uf', 'avg_mmg_coverage_50_69_ans_adj','avg_mmg_coverage_40_49_ans_adj','ebc_det_ratio_50_69','ebc_det_ratio_40_49', 'avg_population']]
st_json = open(geofileST)
states = json.load(st_json)
ct_df = pd.read_csv(DATA_MUNICIP, index_col=False)
ct_df = ct_df[['uf', 'name_uf', 'ibge_munic_id', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_50_69', 'ebc_det_ratio_40_49', 'total_number_mmg_50_69', 'total_number_mmg_40_49', 'avg_population']]
ct_json = open(geofileCT)
counties = json.load(ct_json)


uf_unique_df = ct_df[ct_df['uf'] == 'SP']
uf = uf_dic['SP']
uniq_json_file = '_geojson/munic/geojs-{}-mun.json'.format(uf)
uniq_json = open(uniq_json_file)
uniq_municipalities = json.load(uniq_json)   
lon, lat = latlon(uniq_municipalities)

fig1 = plotmapCounties(uf_unique_df, uniq_municipalities, ctitle='Mamográfica Média de 2010-2019 (50-70 anos)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'], zoom=4, lat=lat, lon=lon)
div = fig1.to_html(full_html=False)

figBr1 = plotmapCounties(ct_df, counties, ctitle='Mamográfica Média de 2010-2019 (50-70 anos)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'])

figBr2 = plotmapCounties(ct_df, counties, ctitle='Mamográfica Média de 2010-2019 (40-50 anos)', colname='mmg_coverage_40_49_ans_adj_max100', chover=['uf', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_40_49'], age=40)
divBr1 = figBr1.to_html(full_html=False)
divBr2 = figBr2.to_html(full_html=False)

@app.route('/')
def index():
    return render_template('/index.html', figure = div)

@app.route('/brmaps')
def brmaps():
    return render_template('/brmaps.html', figure = [divBr1, divBr2])

@app.route('/aboutProject')
def about():
    return render_template('/aboutProject.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6747)

