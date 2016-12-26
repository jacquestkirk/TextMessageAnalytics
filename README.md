# TextMessageAnalytics
Desctrption: Pull a test message database from phone and plot some data from it

Instructions:
- Use SMS Backup and Restore to create and xml of your text messages
   - Note: choose the SMS only option. This code doesn't yet know how to deal with MMS
   -https://play.google.com/store/apps/details?id=com.riteshsahu.SMSBackupRestore&hl=en
- Place the xml file in the Configs folder. Probably shouldn't push this file to a repo since all your text messages will be on the web. This should be managed through gitignore if you are using git. 
- Setup the config file. 
	- Refer to Configs_template.py to see what variables to put in. 
	- Save modified Configs_template.py as Configs.py. You probably shouldn't push Configs.py since it'll contain peoples phone numbers. This should be managed through gitignore if you are using git. 
	- Variables in Configs.py
		- filename: the xml file that contains your text database
		- phone_nums: A dictionary. The key is how you want to refer to the person. The value is their phone number. 
