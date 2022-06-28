from cProfile import label
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
        mapbox_style = "carto-positron",
        center={"lat":-14, "lon": -55},
        zoom=2.5,
        opacity=0.5,
        color_continuous_scale = 'Blackbody_r',
        labels={'uf': 'UF', 'avg_mmg_coverage_50_69_ans_adj': 'Média' , 'avg_mmg_coverage_40_49_ans_adj': 'Média', 'ebc_det_ratio_50_69': 'Taxa de Detecção' },
        title=ctitle
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})

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
        mapbox_style = "carto-positron",
        center={"lat": lat, "lon": lon},
        zoom=zoom,
        opacity=0.5,
        featureidkey="properties.id",
        color_continuous_scale = 'Blackbody_r',
        labels={'uf': 'UF', 'ibge_munic_id': 'IBGE_ID', 'name_munic':'Nome Município', age_label: 'Media(%)'},
        title=ctitle
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0})
    fig.update_traces(marker_line_width=0, marker_line_color="rgba(91,21,21,0.8)")
    
    return fig


def load_home_graph(ct_st):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=ct_st['uf'],
                            y=ct_st['avg_mmg_coverage_50_69_ans_adj'].values,
                            text=ct_st['avg_mmg_coverage_50_69_ans_adj'].values,
                            name='Cobertura Mamográfica',
                            marker_color='rgb(55, 83, 109)'
                            ))
    fig.add_trace(go.Bar(x=ct_st['uf'],
                            y=ct_st['ebc_det_ratio_50_69'].values,
                            text=ct_st['ebc_det_ratio_50_69'].values,
                            name='Taxa de detecção de câncer de mama inicial',
                            marker_color='rgb(26, 118, 255)'
                            ))
    fig.update_layout(
        width=1450,
        height=600,
        title='Dados dos estados brasileiros 2010-2019',
        xaxis_tickfont_size=14,
        xaxis=dict(
            title='Estados',
            titlefont_size=22,
        ),

        yaxis=dict(
            title='Porcentagem (%)',
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


def countiesGraph(ct_df, st_df, uf, nameCT=None):
    with st.spinner('Gerando Gráficos'):
        years = ['2010', '2011', '2012', '2013', '2014',
                 '2015', '2016', '2017', '2018', '2019']
        map1, map2 = st.columns((2, 2))
        title = 'Cobertura mamográfica e a taxa de detecção de câncer de mama inicial (2010-2019)'

        ct_df['avg_population'] = np.log2(ct_df['avg_population'])
        fig = px.scatter(ct_df, x="mmg_coverage_50_69_ans_adj_max100", y="ebc_det_ratio_50_69", color="total_number_mmg_50_69", height=600,
                            trendline="ols", template="plotly", title=title,
                            labels={'ratio': 'Detecção de câncer de mama inicial(%)', 'mmg_coverage_50_69_ans_adj_max100': 'Cobertura Mamográfica(%)', 'avg_population': 'População (log2)'})

        fig2 = px.scatter(ct_df, x="mmg_coverage_40_49_ans_adj_max100", y="ebc_det_ratio_40_49", color="total_number_mmg_40_49", height=600,
                            title=title,
                            trendline="ols", template="plotly", labels={'ebc_det_ratio_40_49': 'Detecção de câncer de mama inicial(%)', 'mmg_coverage_40_49_ans_adj_max100': 'Cobertura Mamográfica(%)', 'mmg_40_total': 'Total de Mamografias'})

        map1.plotly_chart(fig)
        map2.plotly_chart(fig2)

        col, col1, col2 = st.columns((2, 4, 6))
        with col:
            st.write('')

        with col1:
            print(st_df['avg_mmg_coverage_50_69_ans_adj'], st_df['avg_mmg_coverage_40_49_ans_adj'])
            st.metric(label="Cobertura Mamográfica - 50 a 70 anos (2010-2019)", value=str(
                st_df['avg_mmg_coverage_50_69_ans_adj'].values[0]) + "%")

            st.metric(label="Cobertura Mamográfica - 40 a 50 anos (2010-2019)", value=str(
                st_df['avg_mmg_coverage_40_49_ans_adj'].values[0]) + "%")

        with col2:
            st.metric(label="Taxa de Identificação de Câncer de Mama Inicial - 50 a 70 anos (2010-2019)", value=str(
                st_df['ebc_det_ratio_50_69'].values[0]) + "%")

            st.metric(label="Taxa de Identificação de Câncer de Mama Inicial - 40 a 50 anos (2010-2019)", value=str(
                st_df['ebc_det_ratio_40_49'].values[0]) + "%")


def load_state_csv(st_df):
    csv_df = st_df.rename(columns={'avg_mmg_coverage_50_69_ans_adj': 'Cobertura Mamográfica (50-70)', 'avg_mmg_coverage_40_49_ans_adj': 'Cobertura Mamográfica (40-50)', 
                                    'ebc_det_ratio_50_69': 'Taxa Câncer Inicial (50-70)', 'ebc_det_ratio_40_49': 'Taxa Câncer Inicial (40-50)', 'avg_population': 'Nº habitantes'})
    return csv_df

def load_countie_csv(ct_df, uf=None, nameCT=None):
    csv_df = ct_df.rename(columns={'uf': 'UF', 'cod_municipio': 'Codigo IBGE', 'nome_munic': 'Municipio', 'coverage': 'Cobertura Mamográfica (50-70yo)', 'coverage_40': 'Cobertura Mamográfica (40-50)', 'ratio': 'Taxa Câncer Inicial (50-70yo)', 'ratio_40': 'Taxa Câncer Inicial (40-50)', 'mean_pop': 'Nº habitantes'})
    return csv_df
