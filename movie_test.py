import unittest
from movie import *

class TestMovieRevenue(unittest.TestCase):

    def test_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Id, Title, Studio, WorldwideGross, DomesticGross,
                    OverseasGross, Year
            FROM Movie_Revenue
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)
        self.assertEqual(result_list[4][2], 'BV')

        conn.close()

    def test_table2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT * FROM Movie_Revenue
            WHERE Title = "Jurassic Park"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((1993), result_list[0])
        self.assertEqual(result_list[0][3], 1029200000)

        conn.close()

    def test_table3(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DISTINCT Studio
            From Movie_Revenue
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 14)

        conn.close()

    def test_table4(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Id
            From Movie_Revenue
            WHERE Title = "Shrek the Third"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue(71)

        conn.close()

    def test_table5(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT DomesticGross
            From Movie_Revenue
            WHERE Id = 92
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(result_list, 475700000)

        conn.close()

class TestMovie(unittest.TestCase):

    def test_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT ProductionCountry, COUNT(*)
            FROM Movie
            GROUP BY ProductionCountry
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 8)
        self.assertEqual(result_list[6][1], 15)

        conn.close()

    def test_table2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT * FROM Movie
            WHERE MovieId = "68"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((121), result_list[0])
        self.assertEqual(result_list[0][4], 'Fantasy')

        conn.close()

    def test_table3(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT VoteAverage
            From Movie
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 100)
        self.assertNotIn((3.1), result_list)

        conn.close()

    def test_table4(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT MAX(Budget)
            From Movie
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertTrue(380000000)

        conn.close()

    def test_table5(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT RunTime
            From Movie
            WHERE Id = 98
        '''

        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertNotEqual(result_list[0][0], 117)

        conn.close()

class TestJoins(unittest.TestCase):

    def test_both(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Movie_Revenue.Studio, AVG(Movie.Budget)
            FROM Movie_Revenue JOIN MOVIE ON Movie_Revenue.Id = Movie.MovieId
            GROUP BY Studio
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 14)
        self.assertEqual(result_list[2][1], 113900000.0)

        conn.close()

    def test_both2(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Movie_Revenue.Title, Movie.RunTime, Movie.VoteAverage
            FROM Movie_Revenue JOIN MOVIE ON Movie_Revenue.Id = Movie.MovieId
            WHERE RunTime = '136'
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn((136), result_list[0])
        self.assertEqual(result_list[2][2], 6.4)

        conn.close()

    def test_both3(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Movie_Revenue.Title
            FROM Movie_Revenue JOIN MOVIE ON Movie_Revenue.Id = Movie.MovieId
			WHERE Title LIKE  '%3'
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(len(result_list), 4)
        self.assertEqual(result_list[2][0], 'Despicable Me 3')

        conn.close()

class Testget_info_for_movies(unittest.TestCase):

    def test_scrap(self):
        results = get_info_for_movies('http://www.boxofficemojo.com/alltime/world/?pagenum=1&sort=rank&order=ASC&p=.htm')
        self.assertEqual(results[15][0], 'Captain America: Civil War')
        self.assertEqual(results[29][5], '$691.3')
        self.assertEqual(len(results[67]), 8)

class TestMovieRankings(unittest.TestCase):

    def testConstructor(self):
        m = MovieRankings("Avatar", 2009)
        m1 = MovieRankings("Finding Nemo", 2003)

        self.assertEqual(m.Title, "Avatar")
        self.assertEqual(m.Year, 2009)
        self.assertEqual(m1.Title, "Finding Nemo")
        self.assertEqual(m1.Year, 2003)

    def test__str__(self):
        m = MovieRankings("Avatar", 2009)
        m1 = MovieRankings("Finding Nemo", 2003)

        self.assertEqual(m.__str__(), "Avatar (2009)")
        self.assertEqual(m1.__str__(), "Finding Nemo (2003)")


unittest.main()
