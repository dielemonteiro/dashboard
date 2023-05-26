# Importing the libraries 

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from PIL import Image

# Setting page configurations
st.set_page_config(page_title = 'Dashboard Book Recomendation', layout='wide', initial_sidebar_state='expanded')

#
# Creating initial apresentation 
st.markdown("<h1 style = 'text-align: center;'> Analysing Book Rating Dataset </h1>", unsafe_allow_html = True)
col1_, col2_, col3_ = st.columns(3)
image = Image.open('book.png')
col2_.image(image, use_column_width=True)


# Reading the dataset
dataviz = pd.read_csv('dataviz.csv')


# ---------SIDEBAR--------
st.sidebar.title('Menu')

#---------MENU---------
selectPage = st.sidebar.selectbox('Select a option', ['Home Page', 'Dashboard', 'Dataframe'])

st.sidebar.markdown('''
---
Created 👩‍🎓 by [Diele Monteiro](https://www.linkedin.com/in/diele-monteiro/).
''')

#----------HOME PAGE--------------
if selectPage == 'Home Page':
    st.header(':books: Welcome to my App')
    st.markdown("<h4 style = 'text-align: left;'> A Web App by <b><a href = 'https://github.com/dielemonteiro'> Diele Monteiro </a></b></h4>", unsafe_allow_html = True)
    st.write(f"""
             This application's purpose is to analyze a dataset about books based on Data Visualization in order to develop a recommendation system, using Content and Collaborative filtering.

             This application aims to analyze the dashboard and collect relevant insights that can contribute to building the recommendation system.

             The dashboard has been modelled for a target audience of young adults (18 - 35 years old), so you'll find a modern, visually appealing design with an intuitive, easy-to-use interface. 

             *Please browse the Menu tab to find all features of this App* """)


elif selectPage == 'Dashboard':
        st.title('Overview:')
        st.markdown('##') 
        #TOP KPI's
        total_book = int(dataviz['Book-Title'].count())
        averange_rating = round(dataviz['Book-Rating'].mean(), 1)
        star_rating = ':star:' * int(round(averange_rating, 0))

        left_column_mainpage, right_column_mainpage = st.columns(2)
        with left_column_mainpage:
            st.subheader('Total of Books:')
            st.subheader(f'{total_book:,}')
        with right_column_mainpage:
            st.subheader('Averange Rating:')
            st.subheader(f'{averange_rating}{star_rating}')
        st.markdown('---')

    # ROW 1
    # Plotting the distribution of 'Country'
        st.title(':bar_chart: Dashboard')
        st.markdown('## **#Country Distribuition**')
        country_counts_map = dataviz['Country'].value_counts()
        country_data = pd.DataFrame({'Country': country_counts_map.index, 'Count': country_counts_map.values})
        fig1 = px.choropleth(country_data, locations = 'Country',
                    locationmode='country names',
                    color = 'Count',
                    hover_name = 'Country',
                    scope="north america",
                    color_continuous_scale = px.colors.sequential.Viridis)
        fig2 = px.bar(dataviz.value_counts('Country', ascending = False),
                 x = dataviz.value_counts('Country', ascending = False).index,
                 y = dataviz.value_counts('Country', ascending = False),
                 color = 'count',
                 color_continuous_scale = px.colors.sequential.Viridis,
                 title = "The Country with more ratings rated", 
                 text_auto='.2s')
        fig2.update_layout(height = 600, width = 1000, xaxis_title = 'Rating Count',
                      yaxis_title = 'Location')
        fig2.update_yaxes(automargin = True, title_standoff = 10)

    # Creating the streamlit layout
        col1, col2 = st.columns(2)
        with col1:
            st.subheader('Map Visualization')
            st.plotly_chart(fig1)
        with col2:
            st.subheader('Total of Book per Country')
            st.plotly_chart(fig2)

    # ROW 2
    # Plotting the distribution of 'Age'
        st.markdown('## **#Age Distribuition**')
        def set_age_category(v):
            if (v<= 10):
                return "age group 0-10"
            elif (v>10)&(v<=19):
                return "age group 11-19"
            elif (v>19)&(v<=29):
                return "age group 20-29"
            elif (v>29)&(v<=39):
                return "age group 30-39"
            elif (v>39)&(v<=49):
                return "age group 40-49"
            elif (v>49)&(v<=59):
                return "age group 50-59"
            elif(v>60):
                return "age group > 60"
        temp = dataviz.copy()
        temp.dropna(subset=['Age'], inplace=True)
        temp['age_category'] = temp['Age'].apply(set_age_category)
        age_group = temp.groupby('age_category').size().reset_index(name='count')
        age_group = age_group.sort_values(by='age_category', ascending=False)

        fig3 = px.bar(age_group,
              x='age_category',
              y='count',
              color='count',
              color_continuous_scale = px.colors.sequential.Viridis,
              title="Distribution of Books by Age Category",
              text_auto='.2s', width=1400, height=600)
        fig3.update_layout(
            xaxis_title='Age Category',
            yaxis_title='Count',
            title_font=dict(size=24),
            xaxis=dict(tickfont=dict(size=18)),
            yaxis=dict(tickfont=dict(size=18))
        )
        st.plotly_chart(fig3)

    # ROW 3
    # Plotting the Book Ratings
        st.markdown('## **#Book Ratings**')
        st.markdown('#### **Top 10 of books with more ratings**')
        top_books = dataviz['Book-Title'].value_counts().nlargest(10)
        top_books_df = pd.DataFrame({'title': top_books.index, 'occurances': top_books.values})

        fig4 = px.bar(top_books_df, 
                      x='occurances', 
                      y='title',
                      color='occurances',
                      color_continuous_scale = px.colors.sequential.Viridis,
                      orientation='h', 
                      labels={'occurances': 'Number of Occurrence', 'title': 'Books'})
        fig4.update_layout(
            height=700,
            width=850,
            xaxis=dict(tickfont=dict(size=18)),
            yaxis=dict(tickfont=dict(size=18)),
            title_font=dict(size=14)
        )

        # Adicionar título e subtítulo ao gráfico
        fig4.update_layout(
            title={
                'text': 'Top 10 Books with More Occurrences',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            },
        )

    # Plotting the top10 books per country
        st.subheader('You can filter per Country:')
        all_countries_book = dataviz['Country'].unique()
        default_country_book = all_countries_book[0]
        countries = st.multiselect(
            'Select the Country:',
            options=all_countries_book,
            default=default_country_book,
            key='countries_multiselect'
        )

        if not countries:
            countries = all_countries_book

        top_books_by_country = dataviz.groupby(['Country', 'Book-Title']).size().groupby(level=0).nlargest(10).reset_index(level=0, drop=True).reset_index(name='Occurances')
        selection_country = top_books_by_country[top_books_by_country['Country'].isin(countries)]

    # Creating the streamlit layout
        column1, column2 = st.columns([0.6, 0.4])
        with column1:
            st.plotly_chart(fig4)
        with column2:
            st.write('Top 10 Book per Country')
            st.dataframe(selection_country)


    # ROW 4 
    # Plotting the Author Ratings
        st.markdown('## **#Author Ratings**')
        import plotly.graph_objects as go
        most_books = dataviz.groupby('Book-Author')['Book-Title'].count().reset_index().sort_values('Book-Title', ascending=False).head(5)
        fig5 = go.Figure(data=[go.Bar(
            x=most_books['Book-Title'],
            y=most_books['Book-Author'],
            orientation='h',
            marker=dict(
                color=most_books['Book-Title'],
                colorscale='viridis', 
                line=dict(color='rgba(31, 119, 180, 1.0)', width=1),
        )
    )])
        fig5.update_layout(
            title="Top 5 authors with most books",
            xaxis_title="Total number of books",
            yaxis_title="Authors",
            height=600,
            width=800,
            bargap=0.2,  
            bargroupgap=0.1,  
            template='plotly_white',
            xaxis=dict(tickfont=dict(size=18)),
            yaxis=dict(tickfont=dict(size=18)),
            title_font=dict(size=14)  
    )
        st.plotly_chart(fig5)

    # ROW 6
    # Plotting the Top Author
        st.markdown('### **Top 5 books by author Stephen King**')
        author_1 = ['Stephen King']
        search_author_1 = dataviz[dataviz['Book-Author'].str.contains('|'.join(author_1))]
        author_1_top5 = search_author_1.sort_values(by='Book-Rating', ascending=False).head(5)
        author_1_top5 = author_1_top5.reset_index()
        columns_to_keep = ['Book-Title', 'ISBN', 'Year-Of-Publication', 'Publisher', 'Image-URL-L', 'Book-Rating']
        author_1_top5 = author_1_top5.loc[:, columns_to_keep]
        st.dataframe(author_1_top5)

        st.markdown('### **Top 5 books by author Nora Roberts**')
        author_2 = ['Nora Roberts']
        search_author_2 = dataviz[dataviz['Book-Author'].str.contains('|'.join(author_2))]
        author_2_top5 = search_author_2.sort_values(by='Book-Rating', ascending=False).head(5)
        author_2_top5 = author_2_top5.reset_index()
        columns_to_keep = ['Book-Title', 'ISBN', 'Year-Of-Publication', 'Publisher', 'Image-URL-L', 'Book-Rating']
        author_2_top5 = author_2_top5.loc[:, columns_to_keep]
        st.dataframe(author_2_top5)

        st.markdown('### **Top 5 books by author ames Patterson**')
        author_3 = ['James Patterson']
        search_author_3 = dataviz[dataviz['Book-Author'].str.contains('|'.join(author_3))]
        author_2_top3 = search_author_3.sort_values(by='Book-Rating', ascending=False).head(5)
        author_2_top3 = author_2_top3.reset_index()
        columns_to_keep = ['Book-Title', 'ISBN', 'Year-Of-Publication', 'Publisher', 'Image-URL-L', 'Book-Rating']
        author_2_top3 = author_2_top3.loc[:, columns_to_keep]
        st.dataframe(author_2_top3)

        st.markdown('### **Top 5 books by author ohn Grisham**')
        author_4 = ['John Grisham']
        search_author_4 = dataviz[dataviz['Book-Author'].str.contains('|'.join(author_4))]
        author_2_top4 = search_author_4.sort_values(by='Book-Rating', ascending=False).head(5)
        author_2_top4 = author_2_top4.reset_index()
        columns_to_keep = ['Book-Title', 'ISBN', 'Year-Of-Publication', 'Publisher', 'Image-URL-L', 'Book-Rating']
        author_2_top4 = author_2_top4.loc[:, columns_to_keep]
        st.dataframe(author_2_top4)

        st.markdown('### **Author - Mary Higgins Clark**')
        author_5 = ['Mary Higgins Clark']
        search_author_5 = dataviz[dataviz['Book-Author'].str.contains('|'.join(author_5))]
        author_2_top5 = search_author_5.sort_values(by='Book-Rating', ascending=False).head(5)
        author_2_top5 = author_2_top5.reset_index()
        columns_to_keep = ['Book-Title', 'ISBN', 'Year-Of-Publication', 'Publisher', 'Image-URL-L', 'Book-Rating']
        author_2_top5 = author_2_top5.loc[:, columns_to_keep]
        st.dataframe(author_2_top5)

elif selectPage == 'Dataframe':
    st.title('Dataframe')
    st.sidebar.header('Please filter here:')
    all_countries = dataviz['Country'].unique()
    default_country = all_countries[0]
    countries = st.sidebar.multiselect(
        'Select the Countries:',
        options=all_countries,
        default=default_country
    )
    dataviz_selection = dataviz[dataviz['Country'].isin(countries)]
    st.dataframe(dataviz_selection)
