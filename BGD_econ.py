import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt


st.set_page_config(page_title="Bangladesh Market",page_icon="",layout="wide")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

bdg_exports = pd.read_excel('BDG_Exports.xlsx')
bdg_imports = pd.read_excel('BDG_Imports.xlsx')

bdg_exports.iloc[:,2:] = bdg_exports.iloc[:,2:] / 1000
bdg_imports.iloc[:,2:] = bdg_imports.iloc[:,2:] / 1000

bdg_exports = bdg_exports.rename(columns={
    "2018 (Billions)": "2018",
    "2019 (Billions)": "2019",
    "2020 (Billions)": "2020",
    "2021 (Billions)": "2021",
    "2022 (Billions)": "2022",
    "2023 (Billions)": "2023",
    })

bdg_imports = bdg_imports.rename(columns={
    "2018 (Billions)": "2018",
    "2019 (Billions)": "2019",
    "2020 (Billions)": "2020",
    "2021 (Billions)": "2021",
    "2022 (Billions)": "2022",
    "2023 (Billions)": "2023",
    })

exports = bdg_exports.iloc[:,1:]
imports = bdg_imports.iloc[:,1:]

exports_melted = exports.melt(id_vars='Country', var_name='Year', value_name='Exports')
imports_melted = imports.melt(id_vars='Country', var_name='Year', value_name='Imports')

st.write("###")

selected_option = option_menu(
        menu_title= None,
        options= ['Economic Data', 'Companies Data'],
        menu_icon= None,
        default_index=0,
        orientation= 'horizontal',
        styles={
        "container": {
            "padding": "10px",
            # "background-color": "#352f44",
            "box-shadow": "0px 0px 5px 0px rgba(0, 0, 0, 0.25)",
        },
        "icon":{
            "display": "none",
        },
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "margin": "0px 0px",
            # "color": "#ffffff",
            "text-decoration": "none",
            "padding-right": "0px",
            ":hover": {
                # "background-color": "#cccccc",
                # "color": "#ffffff",
                "cursor": "pointer",
            },
        },
        "nav-link.active": {
            # "background-color": "#352f44",
            # "color": "#ffffff",
        },
    }
)

def generate_link_icon(url, icon_path):
    return f'<a href="{url}"><img src="{icon_path}" alt="Link icon"></a>'

def percent_change(data):
    return (data - data.shift(1)) / data.shift(1) * 100

def gdp_yby_change(data):
    return (data - data.shift(1)) 

BGD_df = pd.read_excel("BGD_econ_indicators.xlsx", header=0)
BGD_df = BGD_df.rename(columns=lambda x: x.strip())
BGD_df['date'] = pd.to_datetime(BGD_df['date'], format='%Y').dt.year
BGD_df[['Population','Annual % Change']] = BGD_df[['Population','Annual % Change']].astype('float')
pop = BGD_df[['date', 'Population', 'Annual % Change']]
pop['Population'] = pop['Population'] / 1000000

gdp = BGD_df[['date', 'GDP ( Billions of US $)', 'GDP Per Capita (US $)',
       'GDP Per Capita Annual Growth Rate(%)']]

gdp=gdp.sort_values(by='date')

gdp['annual_gdp_percent'] = percent_change(gdp['GDP ( Billions of US $)'])
gdp['year_by_year_gdp_change'] = gdp_yby_change(gdp['GDP ( Billions of US $)'])

gdp['annual_gdp_percent']=gdp['annual_gdp_percent'].interpolate(limit_direction="both")
gdp['year_by_year_gdp_change'] = gdp['year_by_year_gdp_change'].interpolate(limit_direction="both")

labour = BGD_df[['date','Unemployment Rate (%)','Unemployment Annual Change']]
labour['label_unemployment_rate'] = labour['Unemployment Rate (%)'].apply(lambda x: f'{x:.2f}')


if selected_option == 'Economic Data':

    st.sidebar.title("Bangladesh Economic Research")
    with st.sidebar:
       econimic_menu =  option_menu(
            menu_title= None,
            options= ['Population', 'GDP', 'Labour', 'Trade'],
            menu_icon=None,
            default_index=0,
            styles={
            "container": {
                "padding": "20px",
                # "background-color": "#352f44",
                "box-shadow": "0px 0px 5px 0px rgba(0, 0, 0, 0.25)",
            },
            "icon":{
                "display": "none",
            },
            "nav-link": {
                "font-size": "12px",
                "text-align": "center",
                "margin": "0px 0px",
                # "color": "#ffffff",
                "text-decoration": "none",
                "padding-right": "20px",
                ":hover": {
                    # "background-color": "#cccccc",
                    # "color": "#ffffff",
                    "cursor": "pointer",
                },
            },
            "nav-link.active": {
                # "background-color": "#352f44",
                # "color": "#ffffff",
            },
        }
        )

    if econimic_menu == "Population":
        
        
        # st.markdown("""
        #     **Step into the world of Bangladesh's economy. Our Market Research Analysis breaks down the numbers and trends
        #     that will shape its future. Through easy-to-understand charts and clear explanations, we invite you to explore 
        #     the key indicators that will define Bangladesh's economic narrative in the years to come, navigate through challenges and shape
        #     them as opportunities, pinpoint the major contributors and anticipate what each brings to the table.
        #     Join us on this journey to understand what lies ahead for this dynamic nation.**
        #     """)    
        
        st.markdown("##")
        st.markdown("""
                    **Explore Bangladesh's economic landscape with the Market Research Analysis provided. The data and trends
                    shaping its future are meticulously dissected for your benefit. Gain comprehensive insights into key indicators
                    defining Bangladesh's economic narrative. Navigate challenges and seize opportunities, all while pinpointing major 
                    contributors and anticipating their impact. Additionally, a detailed list of key players in the building and
                    construction materials sector is included. This curated list, sortable by sectors such as 'Construction and
                    Engineering', 'Industry and Manufacturing', 'Real Estate and Development', and 'Business and Supply Chain',
                    provides valuable information including company URLs, names, and notable projects. Embark on this enlightening
                    journey to gain valuable insights into the path ahead for this dynamic nation.**
                    """)
        st.markdown("##")

        st.title("Population")

        left_pop, right_pop = st.columns(2)
        
        with left_pop:
        
            st.subheader("Population by Year")
            fig_pop = go.Figure()

            fig_pop = make_subplots(shared_xaxes=False)

            fig_pop.add_trace(go.Bar(x=pop['date'], y=pop['Population'], name='Population', marker_color='orange')) # text=pop['Population'],textposition="outside", texttemplate='%{text:.0f}',

            fig_pop.update_xaxes(title_text='Year', tickfont=dict(size=15))
            fig_pop.update_yaxes(title_text='Population (Millions)', tickfont=dict(size=15), range=[125, 175])#matches='y', constrain='domain', range=[100000000, 200000000]

            fig_pop.update_layout(
                dragmode=False, selectdirection=None,
                template='plotly_dark',
                height=350,
                showlegend=True,
                font=dict(
                size=9,  
            ),
                legend=dict(x=0.02, y=1.1, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=0)  
            )

            st.plotly_chart(fig_pop,use_container_width=True)
            
        with right_pop:
            
            st.subheader("Annual % Change by Year")
            fig_pop = go.Figure()

            fig_pop = make_subplots(shared_xaxes=False)

            fig_pop.add_trace(go.Scatter(x=pop['date'], y=pop['Annual % Change'], mode='lines+markers+text', name='Annual % Change', line=dict(color='royalblue', width=3) ,line_shape='spline')) # text=pop['Annual % Change'],textposition="top left", texttemplate='%{text:.1f}'

            fig_pop.update_xaxes(title_text='Year', tickfont=dict(size=15))
            fig_pop.update_yaxes(title_text='Population % Change', tickfont=dict(size=15), range=[0.8,2.2])

            fig_pop.update_layout(
                dragmode=False, selectdirection=None,
                template='plotly_dark',
                height=350,
                showlegend=True,
                font=dict(
                size=9,  
            ),
                legend=dict(x=0.02, y=1.1, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=0)  
            )

            st.plotly_chart(fig_pop,use_container_width=True)
        
        st.subheader("Findings")
        
        # st.markdown(
        #     """
        #     <h1 style='margin-top:80px;text-align:center;'></h1>
        #     """,
        #     unsafe_allow_html=True
        # )
        
        st.markdown("""
                    - Population has been steadily increasing from 129M
                    in 2000 to reach 171M in 2023 which represents a 32.5%
                    increase in population in the last 25 years.
                    - Population % change showed a gradual decrease from 1.92% in 2000 to 0.88% in 2009, 
                    then it started to increase with an avarage of 1.19% from 2010 till 2022.
                    - Despite the decreasing percentage change, the absolute growth in population 
                    has remained relatively steady. This suggests that while the rate of growth is slowing down, 
                    the population is still increasing significantly each year.
                    - Constantly increasing population leads to an increasing demand for infrastructure, market expansion, 
                    and urbanization, all of which benefit building material companies.
                    """)
        
        st.divider()
        
        st.subheader("Countries Population")
        st.subheader("")
        
        world_population = pd.read_csv("world_population.csv")
        p1_pop = world_population[:108]
        p2_pop = world_population[108:]
        
        p1_world_population, p2_world_population = st.columns([0.5,0.5])
        
        with p1_world_population:
            st.dataframe(p1_pop, use_container_width= True)
        with p2_world_population:
            st.dataframe(p2_pop, use_container_width= True)
            

    if econimic_menu == "GDP":
    
        # st.subheader("Real GDP - GDP YoY - GDP % Growth ")
        # st.markdown("""
        #             <h3 style="padding-bottom:0;">Real GDP - GDP YoY - GDP % Growth </h3>
        #             <small style="color:#59afe1;">--GDP year on year labeled--</small> """,
        #             unsafe_allow_html=True)

        
        st.title("Gross domestic product (GDP)")
        
        gdp_col1, gdp_col2 = st.columns([0.55,0.45])
        
        with gdp_col1:
        
            st.subheader("Real GDP by Year")
            st.markdown("""
                    <small style="color:#59afe1">--Real GDP: Left y-axis, GDP YoY: Right y-axis--</small> """,
                    unsafe_allow_html=True)
            fig_gdp = make_subplots(specs=[[{"secondary_y": True}]])

            fig_gdp.add_trace(go.Bar(x=gdp['date'], y=gdp['GDP ( Billions of US $)'], name='GDP', marker_color='#95e8d7'), secondary_y=False)
            fig_gdp.add_trace(go.Scatter(x=gdp['date'], y=gdp['year_by_year_gdp_change'], name='GDP YoY', line_shape='spline', mode='lines+markers',line=dict(color='#7dace4', width=2.7), marker=dict(size=5, color='#7dace4')), secondary_y=True) # text=gdp['year_by_year_gdp_change'], textposition='top center', texttemplate='%{text:.1f}'

            fig_gdp.update_xaxes(title_text="Year", tickfont=dict(size=15))

            fig_gdp.update_yaxes(title_text="Real GDP (Billions of US $)", secondary_y=False)
            fig_gdp.update_yaxes(title_text="GDP YoY (Billions of US $)", secondary_y=True,showgrid=False, overlaying='y')
            
            fig_gdp.update_layout(
                dragmode=False, selectdirection=None,
                template='seaborn',
                font=dict(size=9.5),
                height=350,
                showlegend=True,
                legend=dict(x=0.02, y=1.0, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=0)  # Adjust margin for better appearance
            )

            st.plotly_chart(fig_gdp, use_container_width=True, theme="streamlit")
        
        with gdp_col2:
            
            st.subheader("GDP % Growth by Year")
            st.markdown("#")
            fig_gdp_growth = make_subplots()

            fig_gdp_growth.add_trace(go.Scatter(x=gdp['date'], y=gdp['annual_gdp_percent'], name='GDP Annual % Growth', line_shape='spline', mode='lines+markers+text',line=dict(color='#8971d0', width=3), marker=dict(size=8, color='#8971d0'))) # text=gdp['annual_gdp_percent'], textposition='top left', texttemplate='%{text:.0f}'

            # fig_gdp.update_xaxes(tickfont=dict(size=16), row=1, col=1)
            fig_gdp_growth.update_xaxes(title_text = "Year",tickfont=dict(size=15))

            fig_gdp_growth.update_yaxes(title_text='GDP % Growth', tickfont=dict(size=15), range=[0, 45])
            
            fig_gdp_growth.update_layout(
                dragmode=False, selectdirection=None,
                title='GDP % Growth',
                template='plotly_dark',
                font=dict(size=9.5),
                height=350,
                showlegend=True,
                legend=dict(x=0.02, y=1.0, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=0)  # Adjust margin for better appearance
            )

            st.plotly_chart(fig_gdp_growth,use_container_width=True)
    
        st.subheader("Findings")
            
        st.markdown("""
                        - GDP has been steadily increasing from 52B in 2000 to 460B in 2022 with a 767% increase and 43% increase
                        from 2018 till 2022.
                        - Between 2000 and 2012, Bangladesh's GDP showed a slow but steady growth, averaging an annual increase of \\$6.2 billion. 
                        Things picked up significantly from 2012 to 2015, with an impressive total increase of \\$136 billion. 
                        After a brief slowdown, the GDP growth steadied at an average of \\$32.5 billion per year from 2017 to 2022.
                        - The year-on-year change clearly telling that 2015 stands out as a year of robust economic growth.
                        - Despite the dip in year-on-year growth, the GDP has continued to increase. This indicates that the economic boom experienced
                        in 2015 has been consistently maintained, as subsequent years have demonstrated a continuous rise in GDP.
                        - The consistent upward trajectory of GDP and a distinct economic surge serve as promising indicators for Bangladesh's economic future.
                        This suggests that the economy is well-prepared for sustained growth and development. These findings reflect a positive outlook for Bangladesh.
                        """)
            
        st.subheader("Countries GDP")
        st.subheader("")
        
        world_gdp = pd.read_csv("world_gdp.csv")
        p1_gdp = world_gdp[:104]
        p2_gdp = world_gdp[104:]
        
        p1_world_gdp, p2_world_gdp = st.columns([0.5,0.5])
        
        with p1_world_gdp:
            st.dataframe(p1_gdp, use_container_width= True)
        with p2_world_gdp:
            st.dataframe(p2_gdp, use_container_width= True)
        
        st.divider()
        
        st.title("GDP Per Capita")
        
        left_percap, right_percap = st.columns(2)
        
        with left_percap:
            st.subheader("GDP per Capita by Year")
            
            fig_dgp_capita = go.Figure()

            fig_dgp_capita = make_subplots(shared_xaxes=False)

            fig_dgp_capita.add_trace(go.Bar(x=gdp['date'], y=gdp['GDP Per Capita (US $)'], name='GDP Per Capita',marker_color='seagreen')) #  text=gdp['GDP Per Capita (US $)'], textposition='outside',texttemplate='%{text:.0f}',


            fig_dgp_capita.update_xaxes(title_text='Year', tickfont=dict(size=15))
            fig_dgp_capita.update_yaxes(title_text='GDP Per Capita (US $)', tickfont=dict(size=15), range=[0,3000])

            fig_dgp_capita.update_layout(
                dragmode=False, selectdirection=None,
                template='plotly_dark',
                xaxis = dict(tickfont=dict(size=16)),
                # width=900,
                height=350,
                font=dict(size=9),
                showlegend=True,
                legend=dict(x=0.03, y=1.05, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=20)  # Adjust margin for better appearance
            )
            
            st.plotly_chart(fig_dgp_capita,use_container_width=True)
            
        with right_percap:
            
            st.subheader("Per Capita % Growth by Year")
            
            fig_dgp_capita = go.Figure()

            fig_dgp_capita = make_subplots(shared_xaxes=False)

            fig_dgp_capita.add_trace(go.Scatter(x=gdp['date'], y=gdp['GDP Per Capita Annual Growth Rate(%)'], mode='lines+markers+text', name='GDP Per Capita Annual Growth Rate(%)', line=dict(color='orange', width=2),line_shape='spline')) # text=gdp['GDP Per Capita Annual Growth Rate(%)'], textposition='top center',texttemplate='%{text:.1f}'


            fig_dgp_capita.update_xaxes(title_text='Year', tickfont=dict(size=15))
            fig_dgp_capita.update_yaxes(title_text='Per Capita Growth Rate(%)', tickfont=dict(size=15), range=[-5,40])

            fig_dgp_capita.update_layout(
                dragmode=False, selectdirection=None,
                template='plotly_dark',
                xaxis = dict(tickfont=dict(size=16)),
                # width=900,
                height=350,
                font=dict(size=9),
                showlegend=True,
                legend=dict(x=0.03, y=1.05, bordercolor=None, borderwidth=1),
                margin=dict(l=0, r=0, b=0, t=20)  # Adjust margin for better appearance
            )
            
            st.plotly_chart(fig_dgp_capita,use_container_width=True)
        
        st.subheader("Findings")
        
        st.markdown("""
                    - The GDP per capita has demonstrated a consistent rise, climbing from \\$413 in 2000 to \\$2688 in 2022.
                    - In 2015, there was a significant 23% increase in per capita income, reflecting a notable growth.
                    - In 2016, despite the continued increase in GDP per capita, there was a slowdown in the growth rate, 
                    indicating that while the 2015 GDP increase was sustained, the pace of growth had moderated.
                    - A persistent rise in GDP per capita, coupled with continuous population and overall GDP growth, 
                    indicates a growing market full of potential for expansion, innovation, and heightened demand for their offerings and services.
                    """)
        
        st.divider()
        
        st.subheader("Countries GDP Per Capita")
        st.subheader("")
        
        world_gdp_per_capita = pd.read_csv("Countries_gdp_per_capita.csv")
        p1 = world_gdp_per_capita[:104]
        p2 = world_gdp_per_capita[104:]
        
        p1_world_per_capita, p2_world_per_capita = st.columns([0.5,0.5])
        
        with p1_world_per_capita:
            st.dataframe(p1, use_container_width= True)
        with p2_world_per_capita:
            st.dataframe(p2, use_container_width= True)
        
    if econimic_menu == "Labour":
        
        st.title("Unemployment")

        
        left_labour, right_labour = st.columns(2)
        
        with left_labour:
            
            st.subheader("Unemployment Rate by Year")
            
            fig_labour = make_subplots()

            fig_labour.add_trace(go.Scatter(x=labour['date'], y=labour['Unemployment Rate (%)'], mode='lines+markers+text', name='Unemployment Rate (%)', marker=dict(color='#41506b'))) # text=labour['Unemployment Rate (%)'], texttemplate='%{text:.1f}', textposition='top center'


        
            fig_labour.update_xaxes(title_text='Year', tickfont=dict(size=13))
            fig_labour.update_yaxes(title_text='Unemployment Rate (%)', tickfont=dict(size=13), range=[3.2,5.5])
            
            fig_labour.update_layout(
                            dragmode=False, selectdirection=None,
                            height=350,
                            showlegend=True,
                            # width=800,
                            font=dict(size=9),
                            legend=dict(x=0, y=1.05, bordercolor=None, borderwidth=1),
                            margin=dict(l=0, r=0, b=0, t=60)  # Adjust margin for better appearance
                            )

            st.plotly_chart(fig_labour, use_container_width=True)
            
            with right_labour:
                
                st.subheader("Unemployment Annual Change")
                
                fig_labour = make_subplots()


                fig_labour.add_trace(go.Bar(x=labour['date'], y=labour['Unemployment Annual Change'], name='Annual Change', marker=dict(color='#d55b3e'))) # text=labour['Unemployment Annual Change'], textposition='outside', texttemplate='%{text:.2f}'

            
                fig_labour.update_xaxes(title_text='Year', tickfont=dict(size=13))
                fig_labour.update_yaxes(title_text='Unemployment Annual Change', tickfont=dict(size=13),range=[-1.9,1.3])        
                
                fig_labour.update_layout(
                                dragmode=False, selectdirection=None,
                                height=350,
                                showlegend=True,
                                # width=800,
                                font=dict(size=9),
                                legend=dict(x=0, y=1.05, bordercolor=None, borderwidth=1),
                                margin=dict(l=0, r=0, b=0, t=60)  # Adjust margin for better appearance
                                )

                st.plotly_chart(fig_labour, use_container_width=True)
        st.markdown("""
            <h4 style="color:#59afe1">Healthy Unemployment Rate Global Standards</h4>
            
            |Global Standards|min|max|
            |---|---|---|
            |U.S. Federal Reserve|Less than or equal 4|5|
            |European Union|Less than 7|7| 
            
            <h3></h3>
            <h3>Findings</h3>
            
            - Considering 2015 as a year of robust economic expansion, the average unemployment rate from 2015 to 2019 stood at 4.4%, which is indicative of favorable economic growth.
            - The COVID-19 crisis in 2019 led to an uptick in unemployment, a trend experienced by numerous countries. chart showing that the situation is now gradually stabilizing.
            - The unemployment rate has consistently remained within the range of 3.3% to 5.2% from 2000 to 2022, aligning with global standards for unemployment levels.
            - The overall unemployment figures, in conjunction with population, GDP, and GDP per capita, all exhibit a positive correlation, portraying a favorable economic outlook for Bangladesh.
            """, unsafe_allow_html=True)
        
        st.subheader("Countries unemployment Rates")
        st.subheader("")
        
        world_unemployment = pd.read_csv("world_unemployment.csv")
        p1_world_unemployment = world_unemployment[:93]
        p2_world_unemployment = world_unemployment[93:]
        
        p1_unemployment, p2_unemployment = st.columns([0.5,0.5])
        
        with p1_unemployment:
            st.dataframe(p1_world_unemployment, use_container_width= True)
        with p2_unemployment:
            st.dataframe(p2_world_unemployment, use_container_width= True)
        
    if econimic_menu == 'Trade':
        
        fig_exports = px.area(exports_melted, x='Year', y='Exports', color='Country', 
              labels={'Year': 'Year', 'Exports': 'Exports'},
              title='Top 10 Bangladesh Exports by Country Over Time',
              color_discrete_sequence=px.colors.qualitative.Prism_r
              )

        fig_exports.update_yaxes(title_text="Exports Billions $US", tickfont=dict(size=15))
        fig_exports.update_xaxes(title_text="Year", tickfont=dict(size=15))

        fig_exports.update_layout(height=500,template='plotly_dark')

        st.plotly_chart(fig_exports, use_container_width=True)

        
        fig_imports = px.area(imports_melted, x='Year', y='Imports', color='Country',
              labels={'Year': 'Year', 'Imports': 'Imports'},
              title='Top 10 Bangladesh Imports by Country Over Time',
              color_discrete_sequence=px.colors.qualitative.Prism
              )
        
        fig_exports.update_yaxes(title_text="Imports Billions $US", tickfont=dict(size=15))
        fig_exports.update_xaxes(title_text="Year", tickfont=dict(size=15))
        
        fig_imports.update_layout(
                height = 500,

        )
        
        st.plotly_chart(fig_imports, use_container_width=True)

        
elif selected_option == 'Companies Data':
    
    companies = pd.read_csv("all_companies_data.csv")
    
    st.title("Key Players")
    st.sidebar.title("Bangladesh Companies Research")
    with st.sidebar:
       comapnies_menu =  option_menu(
            menu_title= None,
            options= ['Construction and Engineering', 'Industry and Manufacturing', 'Real Estate and Development', 'Business and Supply Chain'],
            menu_icon=None,
            default_index=0,
                        styles={
            "container": {
                "padding": "20px",
                # "background-color": "#352f44",
                "box-shadow": "0px 0px 5px 0px rgba(0, 0, 0, 0.25)",
            },
            "icon":{
                "display": "none",
            },
            "nav-link": {
                "font-size": "12px",
                "text-align": "center",
                "margin": "0px 0px",
                # "color": "#ffffff",
                "text-decoration": "none",
                "padding-right": "20px",
                ":hover": {
                    # "background-color": "#cccccc",
                    # "color": "#ffffff",
                    "cursor": "pointer",
                },
            },
            "nav-link.active": {
                # "background-color": "#352f44",
                # "color": "#ffffff",
            },
        }
        )
    if comapnies_menu == "Construction and Engineering":

        st.subheader("Construction and Engineering")
        st.markdown("""
                    <small style="color:#59afe1;">--double click on the cell to view content--</small>\n
                    <small style="color:#59afe1;">--note column tells about top players--</small>""",
                    unsafe_allow_html=True)
        
        construction_and_engineering_keywords = [
            'General Contractor', 'MEP', 'Concrete', 'Solar energy', 'Clean Energy', 
            'Interior Design', 'Facade', 'Bridge', 'Decoration', 'Renovation', 
            'Blockwork', 'Civil Works', 'Glazing', 'Cladding', 'Power Plants', 
            'Roads', 'Transportation', 'Aviation', 'Installation', 'Construction Audit', 
            'Plumbing', 'Electrical', 'Building Material', 'Drilling', 'Diamond Coring'
        ]
        
        selected_construction_and_engineering_keywords = st.sidebar.multiselect("", construction_and_engineering_keywords)

        selected_construction_and_engineering_keywords = [keyword.lower() for keyword in selected_construction_and_engineering_keywords]

        # filtered_df = companies[companies['Found Keywords'].apply(lambda x: any(keyword in x for keyword in selected_keywords))]
        filtered_df = companies[
            companies['Works on'].apply(
                lambda x: any(keyword.lower() in str(x).lower() if not str(x).isnumeric() else False for keyword in selected_construction_and_engineering_keywords)
            )
        ]
        filtered_df = filtered_df.drop_duplicates(subset=['name'])
        filtered_df = filtered_df.drop(columns=['website','potential','description'])
        filtered_df = filtered_df.rename(columns={'more':'note'})
        st.dataframe(filtered_df, height=400, hide_index=True,
                         column_config={"URL": st.column_config.Column(width='small'),
                                        "URL": st.column_config.LinkColumn(),
                                        "name": st.column_config.Column(width='medium'),
                                        "Works on": st.column_config.Column(width='medium'),
                                        "projects": st.column_config.Column(width='medium'),
                                        "note": st.column_config.Column(width='small')},
                         use_container_width=True
         )



    if comapnies_menu == "Industry and Manufacturing":

        st.subheader("Industry and Manufacturing")
        st.markdown("""
                    <small style="color:#59afe1;">--double click on the cell to view content--</small>\n
                    <small style="color:#59afe1;">--note column tells about top players--</small>""",
                    unsafe_allow_html=True)
         
        industry_and_manufacturing_keywords = [
            'Mega Project', 'Steel', 'Industrial', 'Hospitality', 
            'Marine', 'Utility', 'Oil', 'Gas', 'Energy', 'Concrete'
        ]
        
        selected_industry_and_manufacturing_keywords = st.sidebar.multiselect("", industry_and_manufacturing_keywords)

        selected_industry_and_manufacturing_keywords = [keyword.lower() for keyword in selected_industry_and_manufacturing_keywords]
        
        # filtered_df = companies[companies['Found Keywords'].apply(lambda x: any(keyword in x for keyword in selected_keywords))]
        filtered_df = companies[
            companies['Works on'].apply(
        lambda x: any(keyword.lower() in str(x).lower() if not str(x).isnumeric() else False for keyword in selected_industry_and_manufacturing_keywords)
            )
        ]
        filtered_df = filtered_df.drop_duplicates(subset=['name'])
        filtered_df = filtered_df.drop(columns=['website','potential','description'])
        
        filtered_df = filtered_df.rename(columns={'more':'note'})
        st.dataframe(filtered_df, height=400, hide_index=True,
                         column_config={"URL": st.column_config.Column(width='small'),
                                        "URL": st.column_config.LinkColumn(),
                                        "name": st.column_config.Column(width='medium'),
                                        "Works on": st.column_config.Column(width='medium'),
                                        "projects": st.column_config.Column(width='medium'),
                                        "note": st.column_config.Column(width='small')},
                         use_container_width=True
         )

        
    if comapnies_menu == "Real Estate and Development":

        st.subheader("Real Estate and Development")
        st.markdown("""
                    <small style="color:#59afe1;">--double click on the cell to view content--</small>\n
                    <small style="color:#59afe1;">--note column tells about top players--</small>""",
                    unsafe_allow_html=True)
         
        real_estate_and_development_keywords = [
            'Real Estate', 'Project developer', 'Contractor', 
            'Commercial', 'Residential', 'Touristic', 'Tourism', 'Governmental',
            
        ]
        
        selected_real_estate_and_development_keywords = st.sidebar.multiselect("", real_estate_and_development_keywords)

        selected_real_estate_and_development_keywords = [keyword.lower() for keyword in selected_real_estate_and_development_keywords]
        
 
        filtered_df = companies[
            companies['Works on'].apply(
                lambda x: any(keyword.lower() in str(x).lower() if not str(x).isnumeric() else False for keyword in selected_real_estate_and_development_keywords)
            )
        ]
        filtered_df = filtered_df.drop_duplicates(subset=['name'])
        filtered_df = filtered_df.drop(columns=['website','potential','description'])

        filtered_df = filtered_df.rename(columns={'more':'note'})
        st.dataframe(filtered_df, height=400, hide_index=True,
                         column_config={"URL": st.column_config.Column(width='small'),
                                        "URL": st.column_config.LinkColumn(),
                                        "name": st.column_config.Column(width='medium'),
                                        "Works on": st.column_config.Column(width='medium'),
                                        "projects": st.column_config.Column(width='medium'),
                                        "note": st.column_config.Column(width='small')},
                         use_container_width=True
         )

        
    if comapnies_menu == "Business and Supply Chain":

        st.subheader("Business and Supply Chain")
        st.markdown("""
                    <small style="color:#59afe1;">--double click on the cell to view content--</small>\n
                    <small style="color:#59afe1;">--note column tells about top players--</small>""",
                    unsafe_allow_html=True)
        
        business_and_supply_chain_keywords = [
            'Key player', 'China', 'Worldwide', 'Europe', 'European', 
            'B2C', 'Commerce', 'Construct', 'Build', 'Distributor', 
            'Supplier', 'Manufacture', 'Supply Chain', 'Import', 
            'Export', 'Local', 'Exporter', 'Importer', 'International'
        ]
 
        selected_business_and_supply_chain_keywords = [keyword.lower() for keyword in business_and_supply_chain_keywords]

        selected_business_and_supply_chain_keywords = st.sidebar.multiselect("", business_and_supply_chain_keywords)

 
        filtered_df = companies[
            companies['Works on'].apply(
                lambda x: any(keyword.lower() in str(x).lower() if not str(x).isnumeric() else False for keyword in selected_business_and_supply_chain_keywords)
            )
        ]
        filtered_df = filtered_df.drop_duplicates(subset=['name'])
        filtered_df = filtered_df.drop(columns=['website','potential','description'])        

        filtered_df = filtered_df.rename(columns={'more':'note'})
        st.dataframe(filtered_df, height=400, hide_index=True,
                         column_config={"URL": st.column_config.Column(width='small'),
                                        "URL": st.column_config.LinkColumn(),
                                        "name": st.column_config.Column(width='medium'),
                                        "Works on": st.column_config.Column(width='medium'),
                                        "projects": st.column_config.Column(width='medium'),
                                        "note": st.column_config.Column(width='small')},
                         use_container_width=True
         )

        # fig = go.Figure(data=[go.Table(
        #     header=dict(values=filtered_df.columns.tolist(),
        #                 fill_color='paleturquoise',
        #                 align='left'),
        #     cells=dict(values=[filtered_df[col] for col in filtered_df.columns],
        #                 fill_color='lavender',
        #                 align='left'))
        # ])

        # fig.update_layout(
        #     autosize=False,
        #     width=900,
        #     height=600
        # )

        # st.plotly_chart(fig, use_container_width=True)

        