# About this tagging tool

# Warning/Disclaimer

**WARNING! Installing this requires some changes to your Synology server that could break it. Proceed with caution.**

If you are not comfortable using a linux command line, ssh or scripts, this may not be for you. I've tried to make it simple, but this does require some changes at a core level.

I'm using this method because the Synology API isn't very well documented and doesn't work for this particular use case. I'm also trying to minimise impact to things that Synology may overwrite in future upgrades.

If anyone has a proof of concept that shows how to use the Synology API to enumerate the tags in use, please let me know.

## About this project.

If you're like my family, you've been taking photos for decades, and have thousands of photos. If you've been using synology to handle all the photos taken over many years, it becomes hard to determine what photos you've reviewed and tagged, and to even remember what tags were being used.

These scripts will generate two helper webpages for Synology Photos to help with this.

## The bash script
### make_photo_tag_pages.sh
This generates the two pages for the tagging website.

On the index page, you can see all the tags in use in the shared photos section, or search for a particular tag.

![image](https://raw.githubusercontent.com/cormacj/synology-photo-tagging-assistant/refs/heads/main/Photo%20Tag%20Links.png)

Clicking on a tag will open you photo server page with the tag search pre-populated.

----
The second page is the list of untagged images and videos. It's sorted with the most recent untagged files at the top.

![image](https://raw.githubusercontent.com/cormacj/synology-photo-tagging-assistant/refs/heads/main/Untagged%20Photos%20by%20Date.png)

Clicking on an arrow next to the date will drop down to show you links to the images within synology photos. This also shows the folder where that photo is stored and the filename.

You can click the link and it will open that particular photo.


## Installation

In the following steps, replace "your-username" with the username you use to login into your NAS:

### Configure your NAS
* Login to your NAS command line: `ssh your-username@nas.address`, eg `ssh joeuser@192.0.0.5`

* Create sudoers<br> `sudo su -` This will ask for a password. Enter your password. <br>`echo "your-username ALL=NOPASSWD: /bin/psql" >/etc/sudoers.d/your-username`<br><br>If this worked, you'll have a file in /etc/sudoers.d this looks like this:<br>`root@nasserver:~# cat /etc/sudoers.d/joeuser`<br>`joeuser ALL=NOPASSWD: /bin/psql`
* Type `exit` twice to log out of ssh.

### Install and configure packages
* Log into your NAS gui.
* Open package center and ensure "Web Station","Python 3" and "PHP 8.2" are installed.
* Open "Web Station".
* Select "Web Service" and click "Create":<br>Select "Native script language website".<br>Select "PHP 8.2"<br>Click "Next"<br>Now fill out the name and description, and select the document root.
* Select "Web Portal" and select the service you just created and set up the port according to your preferences. See this for more details: https://kb.synology.com/en-au/DSM/help/WebStation/application_webserv_virtualhost?version=7
* Edit `config.sh`:<br>Change "/path/to/website" to the volume root you selected in the previous step.<br>Change the URL variable to the name of the site you defined.
* Finally run validate.sh and correct any errors that might show.

### Configure scheduled tasks

Further documentation: https://kb.synology.com/en-my/DSM/help/DSM/AdminCenter/system_taskscheduler?version=7

* Log into your NAS gui.
* Open Control Panel and click on "Task Scheduler"
* Click on "Create", then "Scheduled Task" and then "User Defined Script"
* Keep the "General Settings", table at the default.
* Click on "Schedule" and pick your refresh intervals. I have mine set as "Daily" and repeat every hour.
* Click on "Task Settings" and in the user-defined script box enter:<br>`bash /path/to/your/script/make_photo_tag_pages.sh`<br> Remember to replace `/path/to/your/script` with your actual path to your script.
* Finally, make sure you update the `last run` time with something close to the end of the day otherwise it will just run once per day.
