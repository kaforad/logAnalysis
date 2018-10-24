#!/usr/bin/env python2.7
import psycopg2
POPULAR_ARTICLE = "\n\n MOST POPULAR THREE ARTICLES OF ALL TIME \n "
POPULAR_AUTHOR = "\n\n MOST POPULAR ARTICLE AUTHORS OF ALL TIME \n "
POPULAR_ERROR = "\n\n DAYS WHEN MORE THAN 1% of\
REQUESTS LEAD TO  ERRORS \n "
DASH_LINE = "_" * 50 + "\n\n"


def writeToFile(report, reportType):
    # Write report output to text file
    # create a text file for writing and updating data into.
    with open("report.txt", "a+") as printReport:
        emptyStri = " "
        # loop through list to concantenate report string
        printReport.write(reportType)
        printReport.write(DASH_LINE)
        for value in report.values():
            emptyStri = " "
            for data in value:
                emptyStri += str(data)
            # write line to output file
            printReport.write(emptyStri + "\n")
            printReport.write("\n")
        printReport.close()


def articlePopularity():
    """"Function  outputs the most popular three articles of all time\
    from a news database that lead to errors"""
    conn = psycopg2.connect(dbname="news")
    cursor = conn.cursor()
    myquery = """select title, logs.popularity from articles join
     (select reverse(split_part(reverse(path), '/', 1)) as
     path,count(*) as popularity from log
     group by path having path like
     '%article%'order by popularity  desc limit 3) as logs on
     articles.slug = logs.path order by logs.popularity desc"""
    cursor.execute(myquery)
    results = cursor.fetchall()
    report = {}
    i = 0
    print(POPULAR_ARTICLE)
    print(DASH_LINE)
    for result in results:
        i = i + 1
        print result[0], "____", result[1], "views \n"
        report[i] = result[0], "____", result[1], "views"
    print("\n\n")
    writeToFile(report, POPULAR_ARTICLE)
    conn.close()


def authorPopularity():
    """"Function  outputs the most popular article authors of all time\
    from a news database that lead to errors        """
    conn = psycopg2.connect(dbname="news")
    cursor = conn.cursor()
    myquery = """ SELECT VIEW_ArticlesAuthor.author,sum(popularity) as
    popularity from VIEW_ArticlesAuthor join VIEW_ArticleLog on
    VIEW_ArticlesAuthor.title =VIEW_ArticleLog.title
    group by VIEW_ArticlesAuthor.author
    order by Popularity desc; """
    cursor.execute(myquery)
    results = cursor.fetchall()
    report = {}
    i = 0
    print(POPULAR_AUTHOR)
    print(DASH_LINE)
    for result in results:
        i = i + 1
        print result[0], "____", result[1], "views \n"
        report[i] = result[0], "____", result[1], "views"
    print("\n\n")
    writeToFile(report, POPULAR_AUTHOR)
    print("\n\n")
    conn.close()


def errorPopularity():
    """"Function outputs more 1% of articles requests from a news
    database that lead to errors    """
    conn = psycopg2.connect(dbname="news")
    cursor = conn.cursor()
    myquery = """WITH errCount AS(
                    Select * from VIEW_DailyErrCount
                ),totalRequest As(
                    select  errCount.count as count ,
                    cast(errCount.time as date),total.count as total,
                    ROUND((errCount.count*100/total.count),2) as PERCENT
                    from errCount join
                    (Select * from VIEW_TotalDailyRequest) as total on
                        cast(errCount.time as date)= cast(total.time as date)

                )
                select TO_CHAR(time, 'FMMonth FMDDth, YYYY') as time,percent
                from totalRequest where percent>1;  """
    cursor.execute(myquery)
    results = cursor.fetchall()
    report = {}
    i = 0
    print(POPULAR_ERROR)
    print(DASH_LINE + "\n\n")
    for result in results:
        i = i + 1
        print result[0], "____", result[1], "% \n"
        report[i] = result[0], "____", result[1], "%"
    print("\n\n")
    writeToFile(report, POPULAR_ERROR)
    print("\n\n")
    conn.close()

if __name__ == '__main__':

    articlePopularity()
    authorPopularity()
    errorPopularity()
