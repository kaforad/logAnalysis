## LOG ANALYSIS PROJECT ##

**SUMMARY - Log Analysis**
 News paper site  internal reporting tool.This tool determines the article(s) site reader like or read the most. 

### Project Requirement ###
- Database server should run on Linux server
- Installation of Virtual Box VM Environment
- Vagrant Installation and Configuration
### REQUIRED TOOLS ###
- Vagrant
- Virtual Box

### LANGUAGES USED ###
- PYTHON
- SQL QUERY

### RUNNING THE REPORTING TOOL ###
- Install PYTHON 2.7. Check https://www.python.org/downloads/ for more details.
- Download or Clone the reporting tool source code(kaf_loganalysis.py) to you computer.
- Set up a vagrant/vitual machine environment.
- Download Udacity  newsdata.sql and unzip in your Vagrant environment.
	- newsdata.sql can be downloaded from :
	- https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip
- **Bring up your vagrant machine**

	- Type Vagrant up. When Vagrant is launched type Vagrant SSH to have access to the Vagrant environment.
	- cd into Vagrant.
	
### CONNECTING TO THE DATABASE ###
- Navigate to your vagrant path where the newsdata.sql was extracted  into and type the following commands(the command connect to the database server and load data to the database).
 
	1. psql -d news -f newsdata.sql.
	1. -d news 
	1. -f newsdata.sql

### CREATING VIEWS IN THE DATABASE ###
To run this report the following view should be created by running the script below on the database.
There are five views to be created in total.

### 1. VIEW NAME: VIEW_PathLog ###
#### **VIEW_PathLog SCRIPT:** 
    CREATE VIEW VIEW_PathLog AS
		SELECT  path,count(*) as popularity from log 
		group by path having path like '%article%' 
		order by popularity  desc; 
### 2. VIEW NAME: VIEW_ArticleLog ###
#### **VIEW_ArticleLog SCRIPT:**
	CREATE VIEW VIEW_ArticleLog AS
		Select title, VIEW_PathLog.popularity from articles join VIEW_PathLog on 
		VIEW_PathLog.path = concat('/article/', articles.slug) 
		order by VIEW_PathLog.popularity desc;
### 3. VIEW NAME: VIEW_ArticlesAuthor ###
#### **VIEW_ArticlesAuthor SCRIPT:**
	CREATE VIEW VIEW_ArticlesAuthor AS
		select authors.name as Author, Aarticles.title as Title from 
    	authors join 
		(select author,title from articles group by author,title) as Aarticles on 
		authors.id= Aarticles.author;
### 4. VIEW NAME : VIEW_TotalDailyRequest ###
####  **VIEW_TotalDailyRequest SCRIPT:**
		CREATE VIEW VIEW_TotalDailyRequest AS
            select cast(time as date),count(path) as count from log 
			group by cast(time as date);

### 5.	VIEW NAME : VIEW_DailyErrCount ### 
####  **VIEW_DailyErrCount SCRIPT:**
	CREATE VIEW VIEW_DailyErrCount AS 
		select cast(time as date),count(path) as count from log 
		where status<>'200 OK' 
		group by cast(time as date);

### RUNNING THE LOG ANALYSIS REPORT ###
- Use the command below to run the reporting tool.
	python kaf_loganalysis

NOTE: the report will be displayed on your console and a text file name(report.txt). report.txt file will be created in the same path where you have newsdata.sql extracted into.

### REFERENCE(S) ###
- UDACITY
- http://pep8online.com
