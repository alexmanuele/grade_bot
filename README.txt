Grades Bot v0.1
Features:
 This is simply a bot which will log into DalOnline for you five times per day until July and check for new grades from the winter semester. If you have any new grades, it will email them to you.

Dependencies:
  Requires Python3, Selenium, and Google Chrome Headless. The script will try to install Selenium for you, but you'll need to get chrome on your own.

How to use it:
  Simply download this repository into a folder, change the permissions on config.sh and stop.sh to allow execution, and run config.sh using bash.

What will happen:
  You'll be prompted to enter your dal id and password. The dal id needs to be the full email format, i.e ab123456@dal.ca. You will then be asked to provide an email address to which the bot will send emails with your grades. The script will create a task called grades.sh which will run the python script using these credentials as params. grades.sh is the only place where these credentials will be saved. 

  The script will schedule grades.sh to be executed 5 times a day (beginning at 6am and every 3 hours until 6pm) until July 1 at the latest. The most recent results will be stored in the directory where config.sh was run. You will only recieve an email if you have recieved a new grade. 

  If you want to stop this process from running, you can simply run stop.sh. This will remove the scheduled execution of grades.sh.

I didn't get an email??
  You should have recieved an email after running config.sh for the first time. Check your spam folder for emails from dalgradesbot@gmail.com.
