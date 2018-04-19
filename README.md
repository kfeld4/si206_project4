Overview of Project 4:
Analyzing Data: Top 100 Grossing Movies of All Time

The two data sources used for this project include:
  1. The Movie Database API (https://www.themoviedb.org/documentation/api)
     The Movie Database API requires an API key, which can be received at the above URL, and should be placed in a secrets.py file.

  2. A Single Scraped Page ((http://www.boxofficemojo.com/alltime/world/?pagenum=1&sort=rank&order=ASC&p=p=.htm),
     which shares worldwide, domestic, and overseas grosses for the top 100 grossing Movies of all time.

 Program Structure:
 An interactive command line that displays each type of graph.
 Outlined below is the 'help' option to get a sense of the program's structure and its presentation options.
 
         worldwide gross
         Follow up question: <number> of movie title
             1. displays the top 100 movies in rank of worldwide gross

             2. presents a stacked bar chart that compares the domestic
                and overseas grosses as portions of overall worldwide gross
                for each movie

         average budgets
             presents a bar chart comparing the average movie budget for
             each production company

         movies per year
         Follow up question: <year>
             presents a pie chart comparing the number of movies produced
             by their respective production companies grouped by year

         runtime and rating
             presents a scatterplot of runtime and rating for every
             movie

         create database
             creates and populates the databases

         exit
             exits the program

         help
             lists available commands (these instructions)

Setting Up Plot.ly for Graphs:
  1. First, you need to make a plotly account (visit https://plot.ly/).

  2. Second, make sure you have installed plotly on your machine.

  3. Next, grab your api key (Click your account name in the upper right > settings > navigate to API keys). From
     here, click regenerate key and copy the key.

  4. Now, you will need to setup your plotly credentials file.  To do this, go to your terminal and enter the
     python shell (type 'python' or 'python3' depending on what you normally use).  
     You will see something like this:

  5. First, type in:
     import plotly

  6. Next, type the following line in:
     plotly.tools.set_credentials_file(username='myusername', api_key='lr1c37zw8asdfasdf')

  7. Now your plot.ly credentials file is all set up!  You can type in 'exit()' to exit out of the python shell.

Steps to Collect Data:
  1. Scrape the table from Box Office Mojo and store in a list. (method: get_info_for_movies(web_base_url))
     This information will be stored in and populate a single table in your DB.

  2. Create a class, MovieRankings, to make objects and instantiate them with the attributes 'title' and 'year'.
     This is printed to the screen, using .__str__, during the interactive session.

  3. Use the title from the scraped page for the 'GET /search/movie' request on the API and return a list of movie ids.
     (method: search_movie(movie_title))

  4. With movie id as the parameter, use the GET '/movie/{movie_id}' request to retrieve details about each movie.
     (method: get_movie_data(movie_id))
     Pull the following information: production company, budget, genre, runtime, and voting average
     This information will be stored in and populate a single table in your DB.

  5. Connect the two DB tables on the title of the movie.
