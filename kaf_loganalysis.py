import psycopg2
POPULAR_ARTICLE = "\n\n MOST POPULAR THREE ARTICLES OF ALL TIME \n "
POPULAR_AUTHOR = "\n\n MOST POPULAR ARTICLE AUTHORS OF ALL TIME \n "
POPULAR_ERROR = "\n\n DAYS WHEN 1% of REQUESTS LEAD TO  ERRORS \n "


def writeToFile(report, reportType):
    # Write report output to text file
    # create a text file for writing and updating data into.
    printReport = open("report.txt", "a+")
    emptyStri = " "
    # loop through list to concantenate report string
    printReport.write(reportType)
    printReport.write("_________________________________________\n")
    for value in report.values():
        emptyStri = " "
        for data in value:
            emptyStri += str(data)
        # write line to output file
        printReport.write(emptyStri + "\n")
        printReport.write("\n")
    printReport.close()
    # establish connection


def articlePopularity():
	""""Function  outputs the most popular three articles of all time from a news database that lead to errors"""
	conn = psycopg2.connect(dbname="news")
	cursor = conn.cursor()
	myquery = """select title, logs.popularity from articles join (select reverse(split_part(reverse(path), '/', 1)) as path, count(*) as popularity from log  group by path having path like '%article%'order by popularity  desc limit 3) as logs on articles.slug = logs.path order by logs.popularity desc"""
	cursor.execute(myquery)
	results = cursor.fetchall()
	report = {}
	i = 0
	print(POPULAR_ARTICLE)
	print("_________________________________________\n")
	for result in results:
		i = i + 1 
		print result[0], "____", result[1], "views \n"
		report[i] = result[0], "____", result[1], "views"
	print("\n\n")
	writeToFile(report, POPULAR_ARTICLE)
	conn.close()


def authorPopularity():
	""""Function  outputs the most popular article authors of all time 	from a news database that lead to errors		"""
	conn = psycopg2.connect(dbname="news")
	cursor = conn.cursor()
	myquery = """ select authors.name as Author, sum(pTitle.popularity) as Popularity from 
    authors join (select author,title from articles group by author,title) as 
    Aarticles on authors.id= Aarticles.author join 
    (Select title, logs.popularity from articles join
    (select reverse(split_part(reverse(path), '/', 1)) as path, 
    count(*) as popularity from log  group by path having 
    path like '%article%'order by popularity  desc ) as logs  
    on articles.slug = logs.path order by logs.popularity desc) as pTitle 
    on pTitle.title =Aarticles.title 
    group by authors.name order by Popularity desc  """
	cursor.execute(myquery)
	results = cursor.fetchall()
	report = {}
	i = 0
	print(POPULAR_AUTHOR)
	print("_________________________________________\n")
	for result in results:
		i = i + 1
		print result[0], "____", result[1], "views \n"
		report[i] = result[0], "____", result[1], "views"
	print("\n\n")
	writeToFile(report, POPULAR_AUTHOR)
	print("\n\n")
	conn.close()


def errorPopularity():
	""""Function outputs more 1% of articles requests from a news database that lead to errors	"""
	conn = psycopg2.connect(dbname="news")
	cursor = conn.cursor()
	myquery = """select TO_CHAR(time, 'FMMonth FMDDth, YYYY') as time, 
	(ROUND(count(*)*100.0/(select count(*) from log where status<>'200 OK' group by status),2)) as percent 
	from log where status<>'200 OK' group by TO_CHAR(time, 'FMMonth FMDDth, YYYY'), method, status 
	having (count(*)*100.0/(select count(*) from log where status<>'200 OK' group by status))>1 order by time desc ;  """
	cursor.execute(myquery)
	results = cursor.fetchall()
	report = {}
	i = 0
	print(POPULAR_ERROR)
	print("_________________________________________\n")
	for result in results:
		i = i + 1
		print result[0], "____", result[1], "% \n"
		report[i] = result[0], "____", result[1], "%"
	print("\n\n")
	writeToFile(report, POPULAR_ERROR)
	print("\n\n")
	conn.close()

articlePopularity()
authorPopularity()
errorPopularity()

			