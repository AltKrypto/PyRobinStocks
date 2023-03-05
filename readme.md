# A slightly modified version of robin_stocks built to run on mobile 
 + The entire login process is handled automatically based on the credentials placed in the .env file
 + check the .env.sample for proper configuration
 + A guide to generate the 16 character code can be found here:
     https://authenticator.2stable.com/2fa-guides/robinhood/
     + the authenticator code is generated in place programatically during the login process
 
 Using Pyto for iOS
 After installing robin-stocks from pypi navigate to:
 Site packages/robin_stocks/robinhood/authentication.Py
 + change line 83 to:

''' python
home_dir = os.getcwd()
'''

This changes the pickle path to the root of the project folder for storing login sessions as needed. 