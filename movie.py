import sqlite3
import requests
import secrets
import json
import time
from bs4 import BeautifulSoup
import plotly.plotly as py
import plotly.graph_objs as go

TMDB_api_key = secrets.TMDB_api_key
web_base_url = 'http://www.boxofficemojo.com/alltime/world/?pagenum=1&sort=rank&order=ASC&p=.htm'
DBNAME = 'movies.db'
studio_dict = {
    'BV' : 'Buena Vista',
    'DW' : 'DreamWorks',
    'Fox' : 'Fox',
    'HC' : 'H Collective',
    'LG/S' : 'LionsGate / Summit',
    'LGF' : 'LionsGate',
    'P/DW' : 'Paramount / DreamWorks',
    'Par.' : 'Paramount',
    'Sony' : 'Sony',
    'Sum.' : 'Summit',
    'Uni.': 'Universal',
    'NL' : 'New Line',
    'WB' : 'Warner Bros.',
    'WB (NL)' : 'Warner Bros / New Line'
}

try:
    cache_file = open('cach_movie_db.json', 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    MOVIE_DB_CACHE_DICTION = {}

def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_".join(res)

def get_movie_DB_data_using_cache(baseurl, params):
    unique_key = params_unique_combination(baseurl,params)
    if unique_key in MOVIE_DB_CACHE_DICTION:
        return MOVIE_DB_CACHE_DICTION[unique_key]
    else:
        resp = requests.get(baseurl, params)
        MOVIE_DB_CACHE_DICTION[unique_key] = resp.text
        fref =  open('CACHE_DB_MOVIE', 'w')
        dumped_data = json.dumps(MOVIE_DB_CACHE_DICTION)
        fref.write(dumped_data)
        fref.close()
        return MOVIE_DB_CACHE_DICTION[unique_key]

try:
    cache_file = open('cach_movie_.json', 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    MOVIE_WEB_CACHE_DICTION = {}

def get_movie_web_data_using_cache(web_base_url):
    unique_key = web_base_url
    if unique_key in MOVIE_WEB_CACHE_DICTION:
        return MOVIE_WEB_CACHE_DICTION[unique_key]
    else:
        resp = requests.get(web_base_url)
        MOVIE_WEB_CACHE_DICTION[unique_key] = resp.text
        fref =  open('CACHE__WEB_MOVIE', 'w')
        dumped_data = json.dumps(MOVIE_WEB_CACHE_DICTION)
        fref.write(dumped_data)
        fref.close()
        return MOVIE_WEB_CACHE_DICTION[unique_key]

class MovieRankings:
    def __init__(self, Title, Year):
        self.Title = Title
        self.Year = Year

    def __str__(self):
        result = "{} ({})".format(self.Title, self.Year)
        return result

def get_info_for_movies(web_base_url):
    page_text = get_movie_web_data_using_cache(web_base_url)
    page_soup = BeautifulSoup(page_text, 'html.parser')

    content_div = page_soup.find_all('table')
    total_data = []
    for table in content_div[2:]:
        rows = table.find_all('tr')[1:]
        for tr in rows:
            cols = tr.find_all('td')[1:]
            td_list = []
            for td in cols:
                td_list.append(td.text)
            total_data.append((td_list))
    return (total_data)

def search_movie(movie_title):
    baseurl = 'https://api.themoviedb.org/3/search/movie?'
    params = {'api_key': TMDB_api_key, 'query': movie_title}
    req = get_movie_DB_data_using_cache(baseurl, params=params)
    search_movie_data = json.loads(req)
    movie_id = search_movie_data['results'][0]['id']
    return (movie_id)

def get_movie_data(movie_id):
    baseurl = 'https://api.themoviedb.org/3/movie/' + movie_id + '?'
    params = {'api_key': TMDB_api_key}
    req = get_movie_DB_data_using_cache(baseurl, params=params)
    movie_data = json.loads(req)
    return (movie_data)


def init_db():
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")
    # Drop table
    statement = '''
        DROP TABLE IF EXISTS 'Movie_Revenue';
    '''
    cur.execute(statement)

    statement = '''
        DROP TABLE IF EXISTS 'Movie';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Movie_Revenue' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Title' TEXT NOT NULL,
            'Studio' TEXT NOT NULL,
            'WorldwideGross' INTEGER NOT NULL,
            'DomesticGross' INTEGER NOT NULL,
            'OverseasGross' INTEGER NOT NULL,
            'Year' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Movie' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'MovieId' INTEGER NOT NULL,
            'ProductionCountry' TEXT NOT NULL,
            'Budget' INTEGER NOT NULL,
            'Genre' TEXT NOT NULL,
            'RunTime' INTEGER NOT NULL,
            'VoteAverage' INTEGER NOT NULL
        );
    '''
    cur.execute(statement)
    conn.commit()
    conn.close()


def insert_stuff():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    informations = get_info_for_movies(web_base_url)
    scrap_movie_titles = []
    for inst in informations:
        Web_Title = inst[0]
        if ("(") in Web_Title:
            Web_Title = Web_Title[:-7]
            scrap_movie_titles.append(Web_Title)
        elif Web_Title == "Marvel's The Avengers":
            Web_Title = "The Avengers"
            scrap_movie_titles.append(Web_Title)
        elif "Hallows" in Web_Title:
            Web_Title = Web_Title.replace("Hallows","Hallows:")
            scrap_movie_titles.append(Web_Title)
        elif Web_Title == "The Dark Knight":
            Web_Title = "The Dark Knight Rises"
            scrap_movie_titles.append(Web_Title)
        elif "Breaking" in Web_Title:
            Web_Title = Web_Title.replace("Dawn", "Dawn -")
            scrap_movie_titles.append(Web_Title)
        elif "Fantastic" in Web_Title:
            Web_Title = Web_Title.replace("To","to")
            scrap_movie_titles.append(Web_Title)
        elif Web_Title == "E.T.: The Extra-Terrestrial":
            Web_Title = ("E.T. the Extra-Terrestrial")
            scrap_movie_titles.append(Web_Title)
        else:
            scrap_movie_titles.append(Web_Title)
        Studio = inst[1]
        WorldwideGross = inst[2]
        if WorldwideGross.__contains__(","):
            WorldwideGross = WorldwideGross.replace(",","")
        if WorldwideGross.__contains__("."):
            WorldwideGross = WorldwideGross.replace(".","")
        WorldwideGross += "00000"
        DomesticGross = inst[3]
        if DomesticGross.__contains__(","):
            DomesticGross = DomesticGross.replace(",","")
        if DomesticGross.__contains__("."):
            DomesticGross = DomesticGross.replace(".","")
        DomesticGross += "00000"
        OverseasGross = inst[5]
        if OverseasGross.__contains__(","):
            OverseasGross = OverseasGross.replace(",","")
        if OverseasGross.__contains__("."):
            OverseasGross = OverseasGross.replace(".","")
        OverseasGross += "00000"
        Year = inst[7]
        if len(Year) == 5:
            Year = Year[:4]
        insertion = (None, Web_Title, Studio, WorldwideGross[1:], DomesticGross[1:], OverseasGross[1:], Year)
        statement = 'INSERT INTO "Movie_Revenue" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

    query = 'SELECT * FROM Movie_Revenue'
    cur.execute(query)

    Id_dict = {}
    for movie in cur:
        Id = movie[0]
        Web_Title = movie[1]
        Id_dict[Web_Title] = Id

    movie_ids =[]
    count = 1
    for movie in scrap_movie_titles:
        if count == 39 or count == 78:
            time.sleep(11)
        id = search_movie("'" + movie + "'")
        movie_ids.append(id)
        count += 1
    time.sleep(11)
    informations2 = []
    count = 1
    for movie_id in movie_ids:
        if count == 39 or count == 78:
            time.sleep(11)
        data = get_movie_data(str(movie_id))
        informations2.append(data)
        count += 1
    DB_Title = []
    for inst in informations2:
        try:
            Title = inst["title"]
            DB_Title.append(Title)
        except:
            "No Title"
        try:
            Production = inst["production_countries"][0]["name"]
        except:
            "No production country"
        try:
            Budget = inst["budget"]
        except:
            "No budget"
        try:
            Genre = inst["genres"][0]["name"]
        except:
            "No Genre"
        try:
            RunTime = inst["runtime"]
        except:
            "Runtime Error"
        try:
            VoteAverage = inst["vote_average"]
        except:
            "Vote Error"

        insertion = (None, Id_dict[Title], Production, Budget, Genre, RunTime, VoteAverage)
        statement = 'INSERT INTO "Movie" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)
    conn.commit()

def stacked_bar_graph(movie_title):
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")

    statement = 'SELECT DomesticGross, OverseasGross FROM Movie_Revenue'
    statement += ' WHERE Title = ' + "'" + movie_title + "'"

    cur.execute(statement)
    conn.commit()
    for row in cur:
        y = row[0]
        y1 = row[1]

    trace1 = go.Bar(
        y = y,
        name='Domestic Gross'
    )
    trace2 = go.Bar(
        y = y1,
        name='Overseas Gross'
    )

    data = [trace1, trace2]
    layout = go.Layout(
        barmode='stack',
        title="Worldwide Gross ($) for " + movie_title, xaxis={'title':'Movie'},
        yaxis={'title':'Total Gross ($)'},
    )
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='gross-bar-graph')


def production_bar_graph():
    studio_data = []
    budget_data = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")

    statement = 'SELECT Movie_Revenue.Studio, AVG(Movie.Budget) FROM Movie_Revenue JOIN MOVIE ON Movie_Revenue.Id = Movie.MovieId GROUP BY Studio ORDER BY AVG(Budget) ASC'

    cur.execute(statement)
    conn.commit()
    for row in cur:
        studio_data.append(studio_dict[row[0]])
        budget_data.append(row[1])

    x = studio_data
    y = budget_data

    trace0 = go.Bar(
        x = x,
        y = y,
        name='Primary',
        marker=dict(
            color='rgb(49,130,189)'
        )
    )
    data = [trace0]
    layout = go.Layout(
        xaxis=dict(tickangle=-45),
        barmode='group',
        title="Average Movie Budget for Production Companies",
        yaxis={'title':'Budget ($)'},
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='angled-text-bar')

def movies_produced(Year):
    year_data = []
    studio_data = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")

    statement = "SELECT Studio, COUNT (*) FROM Movie_Revenue WHERE Year = " + str(Year)
    statement += " GROUP BY Studio ORDER BY COUNT(*) DESC"

    cur.execute(statement)
    conn.commit()
    for row in cur:
        year_data.append(row[0])
        studio_data.append(row[1])
    labels = year_data
    values = studio_data

    trace = go.Pie(labels=labels, values=values)

    py.plot([trace], filename='basic_pie_chart')

def runtime_rating():
    title_data = []
    run_data = []
    rating_data = []
    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")

    statement = "SELECT Movie_Revenue.Title, Movie.RunTime, Movie.VoteAverage FROM Movie_Revenue JOIN MOVIE ON Movie_Revenue.Id = Movie.MovieId"

    cur.execute(statement)
    conn.commit()
    for row in cur:
        title_data.append(row[0])
        run_data.append(row[1])
        rating_data.append(row[2])

    # Create a trace
    trace = go.Scatter(
        x = run_data,
        y = rating_data,
        text= title_data,
        mode = 'markers'
    )

    data = [trace]
    # layout = go.Layout(
    #     title="Scatterplot for Runtime and Ratings",
    #     yaxis={'title':'Average Rating'},
    #     xaxis={'title':'Runtime (Minutes)'},
    # )

    layout = go.Layout({
      "autosize": False,
      "font": {"family": "Balto"},
      "height": 500,
      "hovermode": "closest",
      "plot_bgcolor": "rgba(240,240,240,0.9)",
      "title": "Scatterplot for Runtime and Ratings",
      "width": 700,
      "xaxis": {
        "gridcolor": "rgb(255,255,255)",
        "mirror": True,
        "showline": True,
        "ticklen": 4,
        "range": [70, 215],
        "title": "Runtime (Minutes)",
        "zeroline": False
      },
      "yaxis": {
        "gridcolor": "rgb(255,255,255)",
        "mirror": True,
        "showline": True,
        "ticklen": 4,
        "range": [5, 9],
        "title": "Average Rating",
        "zeroline": False
      }
      }
    )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='basic-scatter')

if __name__=="__main__":

    try:
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()
    except:
        print ("An error has occured.")

    print ("\nAnalyzing Data From the 100 Top Grossing Films of All Time")
    request = input("\nTo begin, enter 'list movies': ").lower()
    while True:
        if request == "list movies":
            movie_numbers = {}
            movie_rankings = []
            year_list = []
            movie_count = 0
            print ("\nTop 100 Movies\n")
            statement = "SELECT Title, Year FROM Movie_Revenue"
            cur.execute(statement)
            conn.commit()
            for row in cur:
                Title = row[0]
                Year = row[1]
                year_list.append(Year)
                movie_data = MovieRankings(Title, Year)
                movie_rankings.append(movie_data)
            for movie in movie_rankings:
                movie_count += 1
                movie_numbers[movie_count] = movie.Title
                print (str(movie_count) + ' ' + movie.__str__())
            request = input("\nEnter a command (or 'help' for options): ").lower()
            if request == "exit":
                break
            while True:
                if request == "exit":
                    break
                elif request == "worldwide gross":
                    request2 = input("\nSelect a number to learn more about a specific movie's worldwide gross: ")
                    if int(request2) in movie_numbers:
                        movie_title = movie_numbers[int(request2)]
                        print ("\nRetrieving graph for: " + movie_title)
                        stacked_bar_graph(str(movie_title))
                    else:
                        print ("Sorry, that is not a valid input.")
                elif request == "average budget":
                    print ("\nRetrieving bar graph for average budgets")
                    production_bar_graph()
                elif request == "films per year by company":
                    request2 = input("\nInput a year: ")
                    if int(request2) in year_list:
                        print ("\nRetrieving graph for " + request2)
                        movies_produced(request2)
                    else:
                        print ("No top film was produced that year.")
                elif request == "runtimes and ratings":
                    print ("\nRetrieving scatter plot for runtimes and ratings for each movie")
                    runtime_rating()
                elif request == "create database":
                    init_db()
                    insert_stuff()
                elif request == "help":
                    print ("""
                      worldwide gross
                      <movie title>
                           presents a stacked bar chart that compares the domestic
                           and overseas grosses as portions of overall worldwide gross
                           for each movie

                       average budget
                           presents a bar chart comparing the average film budget for
                           each production company

                       films per year by company
                       <year>
                           presents a pie chart comparing the number of films produced
                           by their respective production companies grouped by year

                       runtimes and ratings
                           presents a scatter plot of runtime and rating for every
                           movie

                       create database
                           creates and populates the databases

                       exit
                           exits the program

                       help
                           lists available commands (these instructions)
                    """)
                else:
                    print ("Sorry, that is not a valid request. If needed, enter 'help' for options.")
                request = input("\nEnter a command (or 'help' for options): ").lower()
        else:
            print ("I'm, sorry. That request is not recognized.")
            request = input("\nTo begin, enter 'list movies': ").lower()
