#!/bin/bash
result=`python3 dependencies.py`
path_to_chrome="/usr/bin/chromedriver"
cwd=`pwd`
if [ "$result"=="0" ]; then
	echo "Selenium is installed"
else
	`pip install selenium`
fi
if [ -e "$path_to_chrome" ]; then
	echo "Chrome is installed"
else
	echo "Error: need to install chrome. If chrome is installed, you will need to edit both this script and grade_scrape.py to identify the path to chromedriver"
	exit
fi
`echo {} > courses.json`
echo "Configuring credentials. Enter your dal id:"
read dalid
echo "Enter your password. This will be stored locally"
read dalpw
echo "Entered your recipient email address"
read email
echo "cd $cwd" > grades.sh
echo "python3 $cwd/grade_scrape.py $dalid $dalpw $email" >> grades.sh
chmod 700 grades.sh
crontab -l > tempfile
echo "0 6,9,12,15,18 * * * bash $cwd/grades.sh" >> tempfile
echo "0 0 1 07 * bash $cwd/stop.sh" >> tempfile
echo "" >> tempfile
crontab tempfile
rm tempfile
echo "Configured to run 5 times a day from 6:00pm until 6:00pm"
echo "Process will be removed from crontab on July 1. Or, manually remove it by running stop.sh"
echo "Running initial check. Grades will only be emailed if any are posted."
`./grades.sh`
echo "Done. Please check you email."
