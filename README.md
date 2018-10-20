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
- Navigate to your vagrant path where the newsdata.sql was extracted and type the following commands(the command connect to the database server and load data to the database).
 
	1. psql -d news -f newsdata.sql.
	1. -d news 
	1. -f newsdata.sql
- Connect to the database using the command psql -d news
- Use the command below to run the reporting tool.
	python kaf_loganalysis

NOTE: the report will be displayed on your console and a text file name(report.txt). report.txt file will be created in the same path where you have newsdata.sql extracted into.

###REFERENCE(S)
UDACITY
