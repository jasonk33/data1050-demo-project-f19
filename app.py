import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.graph_objects as go

from database import fetch_all_weather
from data_acquire import CITIES

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']
TEMPERATURE = "Temperature"
WIND = "Wind"
PRESSURE = "Pressure"
HUMIDITY = "Humidity"

# Define the dash app first 
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Define component functions
def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
        html.A([html.Img(id='logo', src=app.get_asset_url('github.png'),
                         style={'height': '35px', 'paddingTop': '7%'}),
                html.Span('Git Repo', style={'fontSize': '2rem', 'height': '35px', 'bottom': 0,
                                                'paddingLeft': '4px', 'color': '#a3a7b0',
                                                'textDecoration': 'none'})],
               className="two columns row",
               href='https://github.com/jasonk33/data1050-demo-project-f19'),
    ], className="row")

def what_if_tool_weather():
    """
    Returns the What-If tool as a dash `html.Div`. The view is a 8:3 division between
    demand-supply plot and rescale sliders.
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='what-if-figure-weather')], className='nine columns'),

        html.Div(children=[
            html.H5("Change Measurement", style={'marginTop': '2rem'}),
            html.Div(children=[  
                dcc.RadioItems(id='measurement-radio-items', 
                options=[{'label': TEMPERATURE, 'value': TEMPERATURE}, {'label': WIND, 'value': WIND}, {'label': PRESSURE, 'value': PRESSURE}, {'label': HUMIDITY, 'value': HUMIDITY}],
                className='row',
                value=TEMPERATURE)
            ], style={'marginTop': '5rem'}),

            html.Div(id='measurement-text', style={'marginTop': '1rem'}),

            html.H5("Change City", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.Checklist(
                    id='city-radio-items',
                    options=[{'label': city, 'value': city} for city in CITIES],
                    className='row',
                    value=[CITIES[0]]
                )
            ], style={'marginTop': '3rem'}),
            html.Div(id='city-text', style={'marginTop': '1rem'}),
        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database (with de-duplication). An abstract layer is built in `database.py` so all queries
            can be done via function call. For a more complicated app, the layer will also be
            responsible for schema consistency. A `plot.ly` & `dash` app is serving this web page
            through. Actions on responsive components on the page is redirected to `app.py` which will
            then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


def about_page():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # About
            ### Project Summary 
            Hello! You have reached the website engineered by 4 Data Science students at Brown University! 
            ** Our project is a visualization website, that uses a live weather API to visualize different features of the weather data. **
            The most prominent features are choosing among 4 cities: Providence, Miami, Dallas and Seattle. 
            Once selected, the visualization will show 4 main variables for the city, with almost no lag time! 
            The 4 variables we display are: ** temperature, wind speed, % of humidity and pressure. **
            The web-app allows the simultaneous plotting of multiple variables on the same visualization for detailed analysis. 
            The project also comes with its own set of outlooks. If we had the resources to build a more thorough project, 
            we would have incorporated the live traffic data from TOMTOM.com, to create a predictive model on how weather effects traffic! 
            ### Datasets used
            ** Main Product: ** We used a weather dataset from openweathermap.org, a live API. 
            The dataset has the following  features: wind speed, % of humidity, temperature in Farenheits, and pressure. 
            In terms of visualization, we were lucky that all of the value were more or less capped at 100, 
            allowing a single scale to be deployed for all visualizations. 

            ** Enhancements: ** Our main goal in the enhancements section is to engineer a ML model that uses the weather features to 
            predict traffic volume (UNIT: cars on the road) for a given hour. Thus, we needed to find a live API that would feed 
            us the Traffic Volume for a given geography at any given time. However, most of such APIs charge the user per pull. 
            Thus, we had to settle for a static project. We used the traffic data from 2014 for the DC Area, provided hourly by 
            [ArcGIS Hub](https://hub.arcgis.com/datasets/882515f07d3346c0a0c6c9672a93b8f1_8). 
            After an initial cleaning of the data, it became clear that we had approximately 50 days that didn’t have not-missing 24 hour data. 
            We used the weather API to pull out data from 2014, for the DC area. However, the weather dataset also had missing data. 
            Thus, after comparing the days with uninterrupted hourly data from both traffic and weather datasets, we pulled out the days that 
            had uninterrupted data (which was 6 days).
            ### Summary of performance with respect to the baseline model(s)
            There are three models deployed in our predictive analysis: ARIMA Forecasting, Random Forest and XGBoost Regression. 
            The baseline model for ARIMA forecast is the mean value of the target variable, giving us a 26,949.49 as MSE. 
            RandomForest and XGBoost use a dummy regression as the baseline model. Dummy MSE is 586,990,934.56 or 24,227.90 if we take 
            the square root of it. When we take the square roots of the RandomForest and XGBoost algorithm MSEs, we get 4,352.76 
            and 6,211.07, respectively. Therefore we can conclude that while ARIMA under performs (worse than the dummy regression), 
            both RandomForest and XGBoost performs significantly better than the baseline model.
            ### Possible next steps
            Some possible next steps are:

            Using the upcoming GITPOD feature that will allow you to run your pod uninterrupted as long as you want. 
            This would allow the data to be pulled out of the API seamlessly. 

            Using a live traffic data API to pull out live traffic data. 
            This would allow the website to make predictions about traffic volume about the coming hour, given this hour’s data points. 
            ### References to related work
            #### [Bad weather and flight delays: The impact of sudden and slow onset weather events](https://www.sciencedirect.com/science/article/pii/S2212012218300753)
            This paper analyzes how weather affects flight departures, and has over 2 million rows of data. 
            A “difference-in-difference” method was used to make predictions at the hourly level. 
            This paper concluded the weather and disturbance-intensity can delay departures up to 23 minutes. 
            #### [Impact of Weather Conditions on Macroscopic Urban Travel Times](https://www.sciencedirect.com/science/article/pii/S0966692312002694)
            This paper not only proved that rain and snow increase travel times, but even took it one step further by looking at how 
            the intensities of rain and snow can make a difference. For example, “light” rain, “moderate” rain, and “heavy rain” 
            increase travel time respectively, by: 0.1 - 2.1%, 1.5 - 3.8%, and 4.0 - 6.0%. Similarly, “light” snow and “heavy” snow 
            lead to an increase of: 5.5 - 7.6% and 7.4 - 11.4%, respectively. 
            #### [A Deep Hybrid Model for Weather Forecasting](https://aditya-grover.github.io/files/publications/kdd15.pdf)
            This paper explains how they forecast weather with meteorological data by looking at features that relate to space and time. 
            #### [Climate coupling between temperature, humidity, precipitation, and cloud cover over the Canadian Prairies](http://www.uvm.edu/~bbeckage/Manuscripts/Bettsetal2014b-10.1002_2014JD022511.pdf)
            This paper has over 50 years of atmospheric data to analyze climate coupling in warm seasons at a monthly, seasonal, 
            and long-term level. 
            ### Names of all team members 
            David Kebudi
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),
        html.Img(src=app.get_asset_url('team_member_images/David.png'),className='row'),
        dcc.Markdown('''Jason Katz'''),
        html.Img(src=app.get_asset_url('team_member_images/Jason.png'),className='row'),
        dcc.Markdown('''Kevin Qualls'''),
        html.Img(src=app.get_asset_url('team_member_images/Kevin.png'),className='row'),
        dcc.Markdown('''Guanhua Zhu'''),
        html.Img(src=app.get_asset_url('team_member_images/Peter.png'),className='row')], 
        className='row')


def additional_description_page():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Additional Project Details
            ### Development Process and Final Technology Stack
            The site was created by taking the example demo project, and slowly replacing all the components with our own. 
            Python was used for all development, plotly for visualizations, mongodb for storing data, and dash for creating the site.
            ### Data Acquisition, Caching, ETL Processing, Database Design
            The data is accessed by scraping [Open Wather](https://openweathermap.org/api) every minute. 
            It is stored in a mongodb, inserting datapoints only if they are new data. 
            We filter the raw data before inserting into the databse.
            We are using a classic mongodb, using one database and mutliple collections.
            Since our data is nested by nature, we are have a collection for each city's data.
            ### [EDA](https://drive.google.com/open?id=1IkowKFI3xCayZHchbcofgmqnkyPbh-fv)
            ### [Enhancements](https://drive.google.com/file/d/12yFPiA6Nh6PEcan_W5L-uHG68bkeciH2/view?usp=sharing)

        ''', className='row eleven columns', style={'paddingLeft': '5%'})], className='row')


tabs_styles = {
    'height': '69px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'backgroundColor': 'gray',
    'fontSize': '30px'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#119DFF',
    'color': 'white',
    'padding': '6px',
    'fontWeight': 'bold',
    'fontSize': '30px'
}

# Sequentially add page components to the app's layout
app.layout = html.Div([
    page_header(),
    html.Hr(),
    dcc.Tabs([
        dcc.Tab(
            label="Project", children=[what_if_tool_weather()], style=tab_style, selected_style=tab_selected_style
        ),
        dcc.Tab(
            label="About", children=[about_page()], style=tab_style, selected_style=tab_selected_style
        ),
        dcc.Tab(
            label="Addition Description", children=[additional_description_page(), architecture_summary()], style=tab_style, selected_style=tab_selected_style
        )
    ], style=tabs_styles),    
], className='row', id='content')


# Defines the dependencies of interactive components
@app.callback(
    dash.dependencies.Output('measurement-text', 'children'),
    [dash.dependencies.Input('measurement-radio-items', 'value')])
def update_measurement_radio_items(value):
    """Changes the display text of the wind slider"""
    return "Measurement: {}".format(value)

@app.callback(
    dash.dependencies.Output('city-text', 'children'),
    [dash.dependencies.Input('city-radio-items', 'value')])
def update_city_radio_items(value):
    """Changes the display text of the hydro slider"""
    return "City: {}".format(value)


_what_if_data_cache = None

@app.callback(
    dash.dependencies.Output('what-if-figure-weather', 'figure'),
    [dash.dependencies.Input('measurement-radio-items', 'value'),
     dash.dependencies.Input('city-radio-items', 'value')])
def what_if_handler_weather(measurement, cities):
    """Changes the display graph of supply-demand"""
    fig = go.Figure()
    measurement_to_color_dict = {TEMPERATURE: "255,0,0", WIND: "0,255,0", PRESSURE: "100,0,100", HUMIDITY: "0,0,255"}
    city_to_color_dict = {CITIES[0]: "purple", CITIES[1]: "black", CITIES[2]: "white", CITIES[3]: "yellow"}

    if cities == []:
        cities = [CITIES[0]]
    for city in cities:
        weather_dicts = fetch_all_weather(city=city)
        weather_dicts = sorted(weather_dicts, key=lambda weather_dict: weather_dict['dt'])
        if measurement == TEMPERATURE:
            measurement_values = [weather_dict['main']['temp'] for weather_dict in weather_dicts]
        elif measurement == WIND:
            measurement_values = [weather_dict['wind']['speed'] for weather_dict in weather_dicts]
        elif measurement == PRESSURE:
            measurement_values = [weather_dict['main']['pressure'] for weather_dict in weather_dicts]
        elif measurement == HUMIDITY:
            measurement_values = [weather_dict['main']['humidity'] for weather_dict in weather_dicts]
        x = [weather_dict['dt'] for weather_dict in weather_dicts]
        
        fig.add_trace(go.Scatter(x=x, y=measurement_values, mode='lines+markers', name=city, line={'width': 2, 'color': "rgb({})".format(measurement_to_color_dict[measurement])},
                  fill='tozeroy', fillcolor="rgba({},0.25)".format(measurement_to_color_dict[measurement]), marker={'color': city_to_color_dict[city]}))


    title = "{} in {}".format(measurement, cities[0])
    if len(cities) > 1:
        for city in cities[1:]:
            title = title + " and {}".format(city)
    fig.update_layout(template='plotly_dark', title=title,
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title=measurement,
                      xaxis_title='Date/Time')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
