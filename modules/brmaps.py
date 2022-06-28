# from cProfile import label
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np

def latlon(geojs):
    lat_list = []
    lon_list = []
    for k in geojs['features']:
        for lat, lon in k['geometry']['coordinates'][0]:
            lat_list.append(lat)
            lon_list.append(lon)
    return ((min(lat_list) + max(lat_list))/2, (min(lon_list) + max(lon_list))/2)
        
def plotmapStates(df, geojson, ctitle, colname, chover):
    fig = px.choropleth_mapbox(
        df,
        locations='ibge_uf_id',
        geojson=geojson,
        color=colname,
        width=400,
        height=400,
        hover_data=chover,
        mapbox_style = 'carto-positron',
        center={'lat':-14, 'lon': -55},
        zoom=2.5,
        opacity=0.5,
        color_continuous_scale = 'Blackbody_r',
        labels={'uf': 'UF', 'avg_mmg_coverage_50_69_ans_adj': 'Média' , 'avg_mmg_coverage_40_49_ans_adj': 'Média', 'ebc_det_ratio_50_69': 'Taxa de Detecção' },
        title=ctitle
    )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0,'t':30,'l':0,'b':0})

    return fig

def plotmapCounties(df, geojson, ctitle, colname, chover, age=50, zoom=2.5, lat=-14, lon=-55): 
    age_label = 'mmg_coverage_40_49_ans_adj_max100' if age != 50 else 'mmg_coverage_50_69_ans_adj_max100'
    fig = px.choropleth_mapbox(
        df,
        locations='ibge_munic_id',
        geojson=geojson,
        color=colname,
        width=400,
        height=400,
        hover_data= chover,
        mapbox_style = 'carto-positron',
        center={'lat': lat, 'lon': lon},
        zoom=zoom,
        opacity=0.5,
        featureidkey='properties.id',
        color_continuous_scale = 'Blackbody_r',
        labels={'uf': 'UF', 'ibge_munic_id': 'IBGE_ID', 'name_munic':'Nome Município', age_label: 'Media(%)'},
        title=ctitle
    )
    fig.update_geos(fitbounds='locations', visible=False)
    fig.update_layout(margin={'r':0,'t':30,'l':0,'b':0})
    fig.update_traces(marker_line_width=0, marker_line_color='rgba(91,21,21,0.8)')
    
    return fig


def load_home_graph(ct_st):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ct_st['uf'],
                            y=ct_st['avg_mmg_coverage_50_69_ans_adj'].values,
                            text=ct_st['avg_mmg_coverage_50_69_ans_adj'].values,
                            name='Mammogram Coverage',
                            marker_color='rgb(55, 83, 109)'
                            ))
    fig.add_trace(go.Bar(x=ct_st['uf'],
                            y=ct_st['ebc_det_ratio_50_69'].values,
                            text=ct_st['ebc_det_ratio_50_69'].values,
                            name='Early breast cancer detection ratio',
                            marker_color='rgb(26, 118, 255)'
                            ))
    fig.update_layout(
        width=1450,
        height=600,
        title='Brazilian States (2010-2019)',
        xaxis_tickfont_size=14,
        xaxis=dict(
            title='States',
            titlefont_size=22,
        ),

        yaxis=dict(
            title='Percentage (%)',
            titlefont_size=22,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.2,  # gap between bars of adjacent location coordinates.
        # gap between bars of the same location coordinate.
        bargroupgap=0.05
    )
    fig.update_traces(texttemplate='%{text:.3s}', textposition='outside')
    return fig


def statesCorplot(st_df):
    st_df['avg_pop_log'] = np.log2(st_df['avg_population'])
    st_df['mmg_coverage_50_69_ans_adj_max100'] = st_df['avg_mmg_coverage_50_69_ans_adj']
    st_df['mmg_coverage_40_49_ans_adj_max100'] = st_df['avg_mmg_coverage_40_49_ans_adj']
    st_df['mmg_coverage_50_69_ans_adj_max100'][st_df['mmg_coverage_50_69_ans_adj_max100']>100] = 100
    st_df['mmg_coverage_40_49_ans_adj_max100'][st_df['mmg_coverage_40_49_ans_adj_max100']>100] = 100
    fig1 = px.scatter(st_df, x='mmg_coverage_50_69_ans_adj_max100', y='ebc_det_ratio_50_69', color='avg_pop_log', width=450, height=450,
                        trendline='ols', template='plotly', title='State coverge vs EBC detection (50-70 years)',
                        labels={'ebc_det_ratio_50_69': 'EBC detection (%)', 'mmg_coverage_50_69_ans_adj_max100': 'Coverage (%)', 'avg_population': 'Population (log2)'})

    fig2 = px.scatter(st_df, x='mmg_coverage_40_49_ans_adj_max100', y='ebc_det_ratio_40_49', color='avg_pop_log', width=450, height=450,
                        title='State coverge vs EBC detection (40-50 years)',
                        trendline='ols', template='plotly', labels={'ebc_det_ratio_40_49': 'EBC detection (%)', 'mmg_coverage_40_49_ans_adj_max100': ' Coverage(%)', 'avg_population': 'Population (log2)'})

    return [fig1, fig2]

def countiesCorplot(ct_df):
    ct_df['avg_pop_log'] = np.log2(ct_df['avg_population'])
    ct_df = ct_df[ct_df['total_number_breast_cases_40_49'] + ct_df['total_number_breast_cases_50_69'] > 30]
    fig1 = px.scatter(ct_df, x='mmg_coverage_50_69_ans_adj_max100', y='ebc_det_ratio_50_69', color='avg_pop_log', width=500, height=500,
                        trendline='ols', template='plotly', title='Municipalities coverge vs EBC detection (50-70 years)',
                        labels={'ebc_det_ratio_50_69': 'EBC detection(%)', 'mmg_coverage_50_69_ans_adj_max100': 'Coverage(%)', 'avg_population': 'Population (log2)'})

    fig2 = px.scatter(ct_df, x='mmg_coverage_40_49_ans_adj_max100', y='ebc_det_ratio_40_49', color='avg_pop_log', width=500, height=500,
                        title='Municipality coverge vs EBC detection (40-50 years)',
                        trendline='ols', template='plotly', labels={'ebc_det_ratio_40_49': 'EBC detection(%)', 'mmg_coverage_40_49_ans_adj_max100': 'Coverage (%)', 'avg_population': 'Population (log2)'})

    return [fig1, fig2]


def load_state_csv(st_df):
    csv_df = st_df.rename(columns={'avg_mmg_coverage_50_69_ans_adj': 'Cobertura Mamográfica (50-70)', 'avg_mmg_coverage_40_49_ans_adj': 'Cobertura Mamográfica (40-50)', 
                                    'ebc_det_ratio_50_69': 'Taxa Câncer Inicial (50-70)', 'ebc_det_ratio_40_49': 'Taxa Câncer Inicial (40-50)', 'avg_population': 'Nº habitantes'})
    return csv_df

def load_countie_csv(ct_df, uf=None, nameCT=None):
    csv_df = ct_df.rename(columns={'uf': 'UF', 'cod_municipio': 'Codigo IBGE', 'nome_munic': 'Municipio', 'coverage': 'Cobertura Mamográfica (50-70yo)', 'coverage_40': 'Cobertura Mamográfica (40-50)', 'ratio': 'Taxa Câncer Inicial (50-70yo)', 'ratio_40': 'Taxa Câncer Inicial (40-50)', 'mean_pop': 'Nº habitantes'})
    return csv_df
