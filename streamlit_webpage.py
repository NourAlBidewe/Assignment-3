import streamlit as st
import pandas as pd 
import plotly.graph_objects as go
import plotly_express as px
# import numpy as np
# import helper as mylib
# import matplotlib.pyplot as plt

@st.cache(allow_output_mutation=True)
def read_data():
    df= pd.read_csv("IMDb movies.csv")
    df.replace("TV Movie 2019", 
           "2019", 
           inplace=True)
    df["year"]= df.year.astype('str')
    df.dropna(subset=['country'], axis=0, inplace= True)

    return df
header = st.container()
visualization1= st.container()
visualization2= st.container()
visualization3= st.container()
visualization4= st.container()
visualization5= st.container()

with header:
    st.title("General Analysis of IMDb Movies ")
    data= read_data()

with visualization1:
    st.header('Top Genres in the dataset using Pie chart')
    # created movies genres 
    genres_top_df = (data[['genre','title']].groupby(['genre'])
             .count().reset_index()
             .rename(columns={'title':'number_of_movies'}))

    #Sort them in descending order so we can extract the 10 genres 
    #with the most movies made
    genres_top_df = genres_top_df.sort_values(by='number_of_movies', ascending=False)
    
    genres_10_df= genres_top_df.iloc[:10]

    labels= list(genres_10_df['genre'])
    values= list(genres_10_df['number_of_movies'])
    fig1= go.Figure(
        data=[
            go.Pie(labels=labels, values=values, 
                pull=[0.1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        ]
    )
    fig1.update_layout(
        title_text="Top 10 genres in terms of number of movies",
    )
    st.plotly_chart(fig1)
    st.text('From the pie chart above, we can see that drama is the most repeated genre.\nIt is found in other genres like comedy and romance')

with visualization2:
    st.header('Genre of movies over the years using bar plot')
    # created movies genres in each year
    genres_df = (data[['genre','title','year']].groupby(["year",'genre'])
                .count().reset_index()
                .rename(columns={'title':'number_of_movies'}))

    #Sort them in descending order so we can extract the 10 genres 
    #with the most movies made
    genres_df = genres_df.sort_values(by='number_of_movies', ascending=False)
    yearsli= ['2000', '1900',]

    years= st.selectbox('Choose the generation:', options= yearsli)
    genres_select_df = (genres_df
                        [genres_df['year']>=years]
                            [genres_df['number_of_movies']>=50]
                    )
    if years == '1900':
        genres_select_df = (genres_df
                        [(genres_df['year']>=years) & (genres_df['year']<'2000')]
                            [genres_df['number_of_movies']>=50]
                    )
    genres_select_df = genres_select_df.sort_values(by='year')
    genres_bar = px.bar(genres_select_df, 
                    x = 'year', 
                    y = 'number_of_movies', 
                    title = 'Movies Produced in the '+ years + '\'s classifed by genres',
                    text = 'number_of_movies', 
                    labels = dict(year = 'Year', 
                                  number_of_movies = 'Number of movies'),
                    color = 'genre',
                    # animation_frame="year",
                    # animation_group="genre",
                    # range_y= [0,1500],
                    # range_x=[0,20]
                    )     
    st.plotly_chart(genres_bar)

with visualization3:
    st.header('Top 10 Countries with highest movies production using map')
    movies_countries_df = (data[['country','title']]
                       .groupby(['country'])
                       .count().reset_index()
                       .rename(columns={'title':'number_of_movies'}))
    movies_countries_df =( movies_countries_df.sort_values(
                                by='number_of_movies',
                                ascending=False))
    movies_countries_df= movies_countries_df.iloc[:10]
    country_code= {'USA':'USA','UK':'GBR', 'India':'IND','Japan':'JPN','France':'FRA','Italy':'ITA',
              'Canada':'CAN','Germany':'DEU','Turkey':'TUR','Hong Kong':'CHN'}
    def country_code_fun(country_name):
        if country_name in  country_code.keys():
            return country_code[country_name]

    movies_countries_df['country_code']= movies_countries_df['country'].apply(lambda x:country_code_fun(x))

    movies_countries_fig= px.choropleth(movies_countries_df,
                                    locations= "country_code",
                                    color="number_of_movies", 
              hover_name= "country",
             color_continuous_scale= px.colors.sequential.Plasma,
             projection= "natural earth")
    movies_countries_fig.update_layout(title='Top 10 countries with highest movies production')

    st.plotly_chart(movies_countries_fig)

with visualization4:
    st.header('Total votes of movies over the years using scatter plot')
    votes_df = (data[
        ['year','title', 'votes',]]
                .groupby(['year'])
            .sum().reset_index()
           )
    years_votes_li= ['1900','1910','1920','1930','1940','1950',
     '1960','1970','1980','1990','2000', '2010','2020', ]

    years_selector= st.slider(
    'Select the generation of movies you want to check',
    min_value=1900, max_value=2020, value=(1900, 1920))
    # st.write(years_selector)
    start,end= years_selector
    # years_selector= st.selectbox('Choose the start year you want to start from:', options= years_votes_li)
    # st.text('For better visualization, kindly choose years where the difference is no more than 20 years')
        
    votes_df['year']=votes_df['year'].astype('int')
    vote_20= votes_df[(votes_df['year']>=start) & (votes_df['year']<=end)]
    maxim= max(vote_20['votes'])
    vote_20['year']=vote_20['year'].astype('str')
    votes_fig= px.scatter(vote_20, x= "year", y= "votes", 
        color= "year", size= "votes", size_max=70, hover_name= "votes",
            animation_frame= "year", animation_group="votes", 
                    range_x=[0,(end-start)], range_y=[0,maxim]
                    )
    votes_fig.update_layout(title= f'Total number of votes from {start} till {end} ',
                            showlegend=False,)
    st.plotly_chart(votes_fig)

    votes_fig2= px.scatter(vote_20, x= "year", y= "votes", 
        color= "year", size= "votes", size_max=70, hover_name= "votes",
                    )
    votes_fig2.update_layout(title= f'Total number of votes from {start} till {end} ',
                            showlegend=False,)
    st.plotly_chart(votes_fig2)

with visualization5:
    st.header(' Duration of movies over some specified years using box plot')
    year_multi= data['year'].unique()
    years_ar= st.multiselect('kindly add the years you want to comapre its duration:',
             options= year_multi)
    # st.write(years_ar)
    st.text('For better visualization, kindly add to 5 years')
    if len(years_ar) > 0:
        arr = ""
        for i in range(len(years_ar)):
            arr += (f" (data['year'] == years_ar[{i}])")
            if i != len(years_ar)-1:
                arr+= " | "
        
        movies_duration_df= data[['title', 'duration','year']][
            eval(arr)
            ]
        
        duration_fig = px.box(movies_duration_df, 
                y="duration", 
                #  title= 'Duration(min) of movies change by year',
                facet_col = 'year', 
                points = False,
                color = 'year')
        st.plotly_chart(duration_fig)
    else:
        st.text('Please select the years for better visulization')

        

