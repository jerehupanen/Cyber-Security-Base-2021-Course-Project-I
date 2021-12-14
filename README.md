# Cyber Security Base 2021 - Course Project I

This is the code for the demo website, which includes 5 security flaws from the [OWASP 2021 top ten list](https://owasp.org/www-project-top-ten/).

I provided fixes for all the issues only in this text document below, not within the project files, for easier comparison and testing.

While working on the website, I got a little excited and added some unnecessary extra functionality and pages that are not needed in testing and might have some flaws or bugs, but I made sure to provide fixes for all 5 flaws explained below.

The repository can be found here: https://github.com/jerehupanen/Cyber-Security-Base-2021-Course-Project-I/

To use the website, extract the files and run the following command in your prompt of choice:
```
python manage.py runserver
```
The database should be included, but if it isn't working, run the following commands as well:
```
python manage.py makemigrations
python manage.py migrate
```

Once the server is running, navigate to the following url to access the homepage: http://127.0.0.1:8000/ (this should redirect you to http://127.0.0.1:8000/owasp)

If you wish to use the Django admin interface to modify tables, go to the following address:
http://127.0.0.1:8000/admin/

You should be able to login with:
Username: admin
Password: admin

To create normal non-admin users for the actual app itself, you can do so at http://127.0.0.1:8000/owasp/singup/

## FLAW 1: [Broken Access Control](https://owasp.org/Top10/A01_2021-Broken_Access_Control/)  
URL: http://127.0.0.1:8000/owasp/profile/admin  
Location in code: owasp/views.py (row 86, profile_view() function)

Broken access control is a very commonly seen issue and crucial aspect to fix especially for website with sensitive or personal information.
To replicate this flaw, I added the ability to add an e-mail address and a phone number to your user by going to http://127.0.0.1:8000/owasp/profile/admin (replace admin with any username), and fill the form at the bottom of the page.
However, currently you do not need to be the same user to see the sensitive data (phone/email), as you could enter any username into the URL and it would show you that users information if it exists.

To fix this, we can add a check to the profile_view function, to see whether the current user is logged in, as well as if they should be able to see the current profile.
To do this, we should first add a requirement to be logged in in general, above the function on line 85:
```django
@login_required(login_url="/owasp/login/") # added this line
def profile_view(request, username):
```
Then add the following code in the beginning of the function on line 87 to redirect the visitor to the homepage if they are not the owner of that profile:
```django
if request.user.username != username:
	return redirect('owasp:index')
```
This way you will not be able to view other peoples profile information, or submit forms on their behalf.

## FLAW 2: [Identification and Authentication Failures](https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/)  
URL: http://127.0.0.1:8000/owasp/signup/  
Location in code: owasp/forms.py (row 23, UserRegistrationForm())

Previously known Broken Authentication, it is one of the most important things to get right on a website, which includes making sure passwords are secure and can't be guessed randomly with ease. On the OWASP list, broken authentication involves the need for prevention of brute force attacks and credential stuffing, as they make it easy to bypass simple passwords. Currently the Signup form notifies the user that the password can't be lests than 8 characters and a few other requirements, however even if you enter a password such as 'abcd', it will still be allowed and will be compromised with a brute force attack instantly.

To fix this, we need to add proper validation for the password field, within the signup form. To accomplish this, we need to add the following 'clean_password1' function to the bottom of the UserRegistrationForm on line 30:
```django
class Meta: # this part is already in the code
        model = UserModel
        fields = ('username', 'password1')

def clean_password1(self): # add this part
	password1 = self.cleaned_data.get('password1')
	try:
		password_validation.validate_password(password1, self.instance)
	except forms.ValidationError as error:

		self.add_error('password1', error)

	return password1
```
The validation rules/logic itself is already built into Django, we're just implementing it here in order to validate the password that was written in the form.

## FLAW 3: [Insecure Design](https://owasp.org/Top10/A04_2021-Insecure_Design/)  
Location in code: tests.py

While this is not a specific flaw, being number 3 on the fresh OWASP list, I felt like it needed to be included here as well. The category discusses good design principles and testing within websites and their internal logic and user-interfaces. Alongside following best coding and security practices during development, insecure design is often a sideproduct of lackluster testing.

One way to fix, or at least improve, the design of our demo website would be to add tests to the project. This can be done by following Djangos [official testing tutorial] (https://docs.djangoproject.com/en/4.0/topics/testing/overview/) and figuring out what would be good things to test. We could for example test what happens if a user posted too many videos to the website (for example thousands), which could cause it to crash or have unintended behavior. We could also use various testcases to validate different inputs.

To make tests, just add the following to the already existing tests.py
```django
from owasp.models import ProfileInformation

class ProfileInfoTests(TestCase):

    def profile_has_valid_email(self):
        """
        has_at_sign() returns True if string contains '@' symbol
        """
        profileInfo = ProfileInformation(username=test)
        self.assertIs(profileInfo.has_at_sign(), True)
```

## FLAW 4: [Security Logging and Monitoring Failures](https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/)  
URL: http://127.0.0.1:8000/owasp/profile/admin  
Location in code: settings.py & owasp/views.py

Lack of proper security logging and monitoring is often overlooked, as many developers feel like it is only necessary for development purposes. Currently the website has no logging whatsoever and we need to add a record to some auditable events such as logins and form submits to monitor any suspicious activity.

In order to add logging functionality to the application, we can use Django's built-in logging system. First we must set-up the logging in the settings.py file by adding the following to the bottom of the file:
```django
LOGGING = {
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': './security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'owasp_logger': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```
This allows us to use a logger named owasp_logger and get a clear formatted message into a file named 'security.log'. We could modify the format of the logs but for this purpose, the above is fine.
To use this logger in the code to record critical events, we have to first initialize the logger in the file we use it in, in this case the views.py -file.
```django
import logging
logger = logging.getLogger('owasp_logger')
```
Finally we just add log messages to any events within the views.py, such as login_view after a unsuccesful login:
```django
login(request, user)
if 'next' in request.POST:
	return redirect(request.POST.get('next'))
else:
	logger.debug("User login failed with username: %s", user.username) # added this line
	return redirect('owasp:index')
```
or perhaps after a successful signup?
```django
form = forms.UserRegistrationForm(request.POST)
if form.is_valid():
	user = form.save()
	logger.debug("Successful signup with username: %s", user.username) # added this line
```
You can see any added logs in the owasp project folder in a file called 'security.log'. While it is still a local file, the file could be stored a secure server or even logged into a database if this were an actual website.

## FLAW 5: [Vulnerable and Outdated Components](https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/)  
Location: settings.py  

This one is sixth on the list and second in the community list, outdated libraries and applications can always have unexpected vulnerabilities and any outdated files and dependencies shoudl always be updated or deleted. Our app has an [outdated logging plugin] (https://github.com/maykinmedia/django-timeline-logger) that was last updated in 2018 and is no longer used in our project, so we should remove it.

We could update any outdated apps using pip in the commandline, but since our old logger library is no longer updated and we don't use it, we should delete it completely by removing the following the last line from settings.py onm line 41:
```django
INSTALLED_APPS = [
    'owasp.apps.OwaspConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  # 'timeline_logger', # remove this line
]
```
**NOTE: Some packages were so outdated when adding this to Github that I couln't even build the project, so imagine it was installed and just remove the already commented out line.**

After removing the outdated app, make migrations if necessary and restart the app.
