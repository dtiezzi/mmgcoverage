from flask import Flask, render_template, request
from modules.brmaps import *
from modules.ufIbge import UfBr
from modules.loadfiles import LoadFiles
import pandas as pd
import json
import os

app = Flask(__name__)

app.static_folder = 'static'

uf_dic = UfBr().state_dict
uf_names_dic = UfBr().state_name_dict
uf_area_dic = UfBr().state_area_dict
uf_area_dic = {k: 1 - (uf_area_dic[k] - min(uf_area_dic.values())) / (max(uf_area_dic.values()) - min(uf_area_dic.values())) for k in uf_area_dic}

states, counties = LoadFiles(['/var/www/mmgcov.com/_geojson/brstates.geojson', '/var/www/mmgcov.com/_geojson/br_mun_all.json']).loadjson()
st_df, ct_df = LoadFiles(['/var/www/mmgcov.com/csv/Supplemental_table_states_data.csv', '/var/www/mmgcov.com/csv/Supplemental_table_municipality_data.csv']).loadcsv()

## Filt columns
st_df = st_df[['ibge_uf_id','uf', 'avg_mmg_coverage_50_69_ans_adj','avg_mmg_coverage_40_49_ans_adj','ebc_det_ratio_50_69','ebc_det_ratio_40_49', 'avg_population']]
ct_df = ct_df[['uf', 'name_uf', 'ibge_munic_id', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_50_69', 'ebc_det_ratio_40_49', 'total_number_mmg_50_69', 'total_number_mmg_40_49', 'avg_population']]

figBr1 = plotmapCounties(ct_df, counties, ctitle='Mammogram coverage from 2010 to 2019 (50-70 years)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'])
figBr2 = plotmapCounties(ct_df, counties, ctitle='Mammogram coverage from 2010 to 2019 (40-50 years)', colname='mmg_coverage_40_49_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_40_49_ans_adj_max100', 'ebc_det_ratio_40_49'], age=40)
divBr1 = figBr1.to_html(full_html=False)
divBr2 = figBr2.to_html(full_html=False)



@app.route('/')
def index():
    return render_template('/index.html', figure = [divBr1, divBr2])

@app.route('/brstmaps')
def brmaps():
    figBrSt1 = plotmapStates(st_df, states, ctitle='Mammogram coverage from 2010 to 2019 (50-0 years)', colname='avg_mmg_coverage_50_69_ans_adj', chover=['uf', 'avg_mmg_coverage_50_69_ans_adj', 'ebc_det_ratio_50_69'])
    figBrSt2 = plotmapStates(st_df, states, ctitle='Mammogram coverage from 2010 to 2019 (40-50 years)', colname='avg_mmg_coverage_40_49_ans_adj', chover=['uf', 'avg_mmg_coverage_50_69_ans_adj', 'ebc_det_ratio_40_49'])
    divBrSt1 = figBrSt1.to_html(full_html=False)
    divBrSt2 = figBrSt2.to_html(full_html=False)
    return render_template('/brstmaps.html', figure = [divBrSt1, divBrSt2])

@app.route('/stmaps', methods=['GET', 'POST'])
def stmaps():
    if request.method == 'POST':
        uf = request.form.get('state')
    else:
        uf = 'SP'
    uf_unique_df = ct_df[ct_df['uf'] == uf]
    uf_cod = uf_dic[uf]
    uf_name = uf_names_dic[uf]
    uf_area = uf_area_dic[uf]
    uniq_json_file = f'/var/www/mmgcov.com/_geojson/munic/geojs-{uf_cod}-mun.json'
    uniq_json = open(uniq_json_file, "rb")
    uniq_municipalities = json.load(uniq_json)   
    lon, lat = latlon(uniq_municipalities)
    fig1 = plotmapCounties(uf_unique_df, uniq_municipalities, ctitle='Mammogram coverage from 2010 to 2019 (50-70 years)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'], zoom=4 + uf_area, lat=lat, lon=lon)
    fig2 = plotmapCounties(uf_unique_df, uniq_municipalities, ctitle='Mammogram coverage from 2010 to 2019 (40-50 years)', colname='mmg_coverage_50_69_ans_adj_max100', chover=['uf', 'name_munic', 'mmg_coverage_50_69_ans_adj_max100', 'ebc_det_ratio_50_69'], zoom=4 + uf_area, lat=lat, lon=lon)
    div1 = fig1.to_html(full_html=False)
    div2 = fig2.to_html(full_html=False)
    return render_template('/stmaps.html', figure = [div1, div2], uf_name = uf_name)

@app.route('/aboutProject')
def about():
    return render_template('/aboutProject.html')

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=6747)

