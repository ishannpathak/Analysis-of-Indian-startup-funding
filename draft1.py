
import dash                     # pip install dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px     # pip install plotly==5.2.2

import pandas as pd             # pip install pandas

#DATA CLEANING
startup_df = pd.read_csv("2020_data.csv")
print(startup_df.head())
dropcolumns = startup_df.drop(["What it Does", "Founder/s"], axis = 1)
startup_DC = dropcolumns.dropna()

startup_DC['currency'] = startup_DC.Amount.apply(lambda s: s[0])
startup_DC['amount'] = startup_DC.Amount.apply(lambda x: x[1:].split("/")[0])
startup_DC.amount = startup_DC.amount.str.replace(',', '').astype('float')

dropped = startup_DC.drop(startup_DC.index[startup_DC['Headquarters'].isin([  'Bihar', 'Faridabad, Haryana', 'The Nilgiris', 'Haryana', 'Telangana', 'Andhra Pradesh' , 
                                                                              'Trivandrum', 'Telungana', 'Manchester', 'Panaji', 'Andhra Pradesh'
                                                                               'Bhilwara', 'Silvassa'])])
t = dropped.replace({'Headquarters' : { 'Andheri' : 'Mumbai', 'Gujarat' : 'Ahmedabad', 'Thane' : 'Mumbai', 'Cochin':'Kochi', 'Gandhinagar' : 'Ahmedabad', 'Bhilwara' : 'Jaipur'}})
newlabel_industry = t.replace({'Industry' : { 'Femtech' : 'Fintech', 'Mobile Games' : 'Gaming', 'B2B Ecommerce' : 'Ecommerce',
                                               'BioTechnology' : 'Biotech', 'HealthTech' : 'Healthcare' , 'Health care' : 'Healthcare'}})
final_df = newlabel_industry[newlabel_industry['Company/Brand'] != 'VerSe Innovation']

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Funding for startups in India", style={"textAlign":"center"}),
    html.Hr(),
    html.P('A startup is a company begun by an entrepreneur seeking, developing, and validating a scalable idea that intends to grow large beyond the founder. Startups face high uncertainty and have high rates of failure, but some startups become unicorns. Unicorns are privately held startup companies valued at over US$1 billion. There has been an exponential growth in startups over the past few years in India. There are a lot of innovative startups coming up in near future and a lot of funding as well. In this notebook, we explore the Indian Startup data and understand more about the ecosystem and the changes over time.', style={"textAlign":"center"}),
    html.Hr(),
    html.P("Select Location:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Headquarters', clearable=False,
                     value="Bangalore",
                     options=[{'label': x, 'value': x} for x in
                              final_df["Headquarters"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div", children=[]),
    
    html.Hr(),
    html.P("Select Industry Head:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Industry Head', clearable=False,
                     value="FinTech",
                     options=[{'label': x, 'value': x} for x in
                              final_df["Industry Head"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div2", children=[]),

    html.Hr(),
    html.P("Select Year:"),
    html.Div(html.Div([
        dcc.Dropdown(id='Founded', clearable=False,
                     value="2018",
                     options=[{'label': x, 'value': x} for x in
                              final_df["Founded"].unique()]),
    ],className="two columns"),className="row"),

    html.Div(id="output-div3", children=[])
])

@app.callback(Output(component_id="output-div", component_property="children"),
              Input(component_id="Headquarters", component_property="value"),
)
def make_graphs(location_chosen):
   
   
   
    # HISTOGRAM
    df_hist = final_df[startup_df["Headquarters"]==location_chosen]
    fig_hist = px.histogram(df_hist, x="Industry Head", title = "Number of Startups that received funding", color = "Industry")
    fig_hist.update_xaxes(categoryorder="total descending")

    # Scatter CHART
    fig_strip = px.strip(df_hist, x="amount", y="Stage", hover_name = ("Company/Brand"), title = "Funding classified by Stage", color = "Company/Brand")

    # Scatter industry head
    fig_industryhead = px.scatter_3d(final_df, x="Founded", y="Headquarters", z= "amount", color="Headquarters", title = "Funding classified by industry heads", hover_name = ("Company/Brand") , hover_data=['amount'])
    # Scatter headquarters
    
    fig_headquarters = px.scatter_matrix(final_df, dimensions = ("Founded", "Stage", "amount"), color="Headquarters", title = "Funding classified by location", hover_name = ("Company/Brand") , hover_data=['amount'])

    # Scatter industry
 
    fig_industry = px.scatter(final_df, x="Industry", y="amount", color="Headquarters", title = "Funding classified by industry", hover_name = ("Company/Brand") , hover_data=['amount'])

     # SUNBURST
    df_sburst = final_df.dropna(subset=['Industry Head'])
    df_sburst = df_sburst[df_sburst["Headquarters"].isin(["Mumbai", "Bangalore", "New Delhi", "Noida", "Gurgaon", "Chennai", "Hyderabad", "Ahmedabad", "Chandigarh"])]
    df_sburst1 = df_sburst[df_sburst["Industry Head"].isin(["FinTech", "Food", "Hospitality", "AI", "Automotive", "Logistics", "Edtech", "Finance", "IT", "Health", "Fashion"])]
    fig_sunburst = px.sunburst(df_sburst1, path=["Industry Head", "Headquarters", "Stage"] , title = "Proportion of Startups by Location, Industry and Stage")




    return [
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip)], className="six columns"),
        ], className="row"),
        html.H2("Funding classification", style={"textAlign":"center"}),
        html.Hr(),
        html.Div([
            html.Div([dcc.Graph(figure=fig_industryhead)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_headquarters)], className="six columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_industry)], className="twelve columns"),
        ], className="row"),
        html.Div([
            html.Div([dcc.Graph(figure=fig_sunburst)], className="twelve columns"),
        ], className="row"),
       
    ]

    
@app.callback(Output(component_id="output-div2", component_property="children"),
              Input(component_id="Industry Head", component_property="value"),
)


def make_graphs02(industry_chosen):
   
   
   
    # HISTOGRAM
    df_hist02 = final_df[startup_df["Industry Head"]==industry_chosen]
    fig_hist02 = px.histogram(df_hist02, x="Headquarters", title = "Number of Startups that received funding")
    fig_hist02.update_xaxes(categoryorder="total descending")

    # Scatter CHART
    fig_strip02 = px.strip(df_hist02, x="amount", y="Stage", hover_name = ("Company/Brand"), title = "Funding classified by Stage", color = "Company/Brand")

    return [
       
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist02)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip02)], className="six columns"),
        ], className="row"),
        
    ]


@app.callback(Output(component_id="output-div3", component_property="children"),
              Input(component_id="Founded", component_property="value"),
)


def make_graphs03(year_chosen):
   
   
   
    # HISTOGRAM
    df_hist03 = final_df[startup_df["Founded"]==year_chosen]
    fig_hist03 = px.histogram(df_hist03, x="Industry Head", title = "Number of Startups that received funding")
    fig_hist03.update_xaxes(categoryorder="total descending")

    # Scatter CHART
    fig_strip03 = px.strip(df_hist03, x="amount", y="Stage", hover_name = ("Company/Brand"), title = "Funding classified by Stage", color = "Company/Brand")

    return [
       
        html.Div([
            html.Div([dcc.Graph(figure=fig_hist03)], className="six columns"),
            html.Div([dcc.Graph(figure=fig_strip03)], className="six columns"),
        ], className="row"),
        html.H2("Dataset Acknowledgement", style={"textAlign":"center"}),
        html.P('The data used in this project is from Trak. in and we would like to sincerely thank them for making the data available to the public for free. This dataset has funding information for the Indian startups from January 2015 to August 2021. It includes columns with the date funded, the city the startup is based, the names of the funders, the type of funding, and the amount invested (in USD).', style={"textAlign":"center"}),
    ]
if __name__ == '__main__':
     app.run_server('localhost', 4448)(debug=True)