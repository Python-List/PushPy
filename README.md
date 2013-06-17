[![Foo](http://img407.imageshack.us/img407/8403/logoasaf.jpg)](http://google.com.au/)

# Pushpy 1.0

Pushpy is a push notification server based on Python. It's composed by a users database to store users token ( and more information that the server owner wants ), a web interface with Google Login to send notifications using a web platform. The Google emails accounts allowed to send notifications are stored in another database

## Technologies
* **Flask Microframework**: The Python Framework used to the web user interface.
* **Python**: For the entire backend. Is a general-purpose, high-level programming language whose design philosophy emphasizes code readability.
* **Flask-WTF**:Flask-WTF offers simple integration with WTForms. This integration includes optional CSRF handling for greater security.
* **Flask-Logins**:Flask-Login provides user session management for Flask. It handles the common tasks of logging in, logging out, and remembering your users’ sessions over extended periods of time.

## Prerequisites
Ensure evereything bellow is installed. Otherwise PushPy won't work propertly.
* Python
* MySQL or SQLite
* Flask:
> 	pip install flask==0.9
* Werkzeug:
>	pip install werkzeug==0.8.3
* Flask-WTF:
>	pip install Flask-WTF
* Flask-Login
>	pip install Flask-Login==0.1.3
* Flask-OpenID
>	pip install flask-openid
* Flask-SQLAlchemy
>	pip install flask-sqlalchemy
* Flask-Admin
>	pip install flask-admin

## Setup
Inside /app folder you'll finde a file called config.py .  This file contains all configuration of Pushpy. The parameters you have to setup are:

Related with DB configuration:
> dbname= 'pushpy'
> 
> DB_URI= 'sqlite:///'+ dbname + '.db'

Where you introduce your dbname and DB_URI has the URI to connect database

**Note: In case you use MySQL remember to create database and specify its name in dbname**

Then you have to config **CSFR_ENABLED** and **SECRET_KEY**. Both parameters are related with Flask-WTF. You'll find information about them here: [http://pythonhosted.org/Flask-WTF/](http://)
> CSRF_ENABLED = True
> 
> SECRET_KEY = ''
> 
> basedir = os.path.abspath(os.path.dirname(__file__))
> 
> OPENID_PROVIDERS = [
>     { 'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id' }]

The last one OPENID_PROVIDERS has all providers allowed for openID login. Pushpy is designed to works with Google accounts but take a look at OpenID, you can add more openID providers. [http://openid.net/get-an-openid/](http://)

####Allowed users

In the lines bellow you must config the users that have permissions to send notifications. You only have o introduce their nickname and their email.

>  Allowed users to send notifications ( using gmail accounts )

> adminusers=[{'nickname':'nick1','email':'user@gmail.com'},
            ]

### Generate push certificate
For sending notifications you need a certificated generated by the App Dev Center. If you don't know how to generate it please follow this tutorial:

[https://code.google.com/p/apns-php/wiki/CertificateCreation](http://)

I called both dev.pem and dist.pem ( development and production certificates ). Please, put both in root PushPy folder

**Depending if you are sending notifications in development or distribution mode you have to select it in web interface. Take care if you have many users in your database cause they could received not expected notifications.**


## Run
If everything is ok run server:
> python server.py

Then enter to the url bellow and a Login page will appear. Login with your Google account and if it's on the database as allowed you'll enter to the Send Notifications page.

[http://127.0.0.1:5000/pushpy/push
](http://)

The rest is explained in the page

[![Foo](http://img43.imageshack.us/img43/3857/capturadepantalla201303n.png)](http://google.com.au/)


## iOS App
The last thing is setup iOS client app to update users information in database. We have added a Obj-c class to simplify the proccess. Everything you have to do is firstly register you app for push notifications.

Add this line in your **- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)launchOptions**

 `[[UIApplication sharedApplication] registerForRemoteNotificationTypes: (UIRemoteNotificationTypeBadge | UIRemoteNotificationTypeSound | UIRemoteNotificationTypeAlert)];`

Moreover config PPy ios library with this lines just under bellow:
`[[PPyController sharedPPy] initializeWithAddress:@"mydomain.com" andPort:@"5000"]`

**Important: You have to change mydomain.com and 5000 for your domain and your port where Pushpy server si being executed**

Then we have to register the user as soon as a token from Apple APN server is received. Put this code fragment in your App Delegate:

`- (void)application:(UIApplication*)application didRegisterForRemoteNotificationsWithDeviceToken:(NSData*)deviceToken
{

	NSLog(@"My token is: %@", deviceToken);
	NSString* devicetoken = [[[[token description] stringByReplacingOccurrencesOfString: @"<" withString: @""] stringByReplacingOccurrencesOfString: @">" withString: @""] stringByReplacingOccurrencesOfString: @" " withString: @""] ;                                  
    BOOL enabled=TRUE; //It's depend on your app user configuration
    NSString * language = [[NSLocale preferredLanguages] objectAtIndex:0];
    NSDictionary
    NSDictionary *dict=[[NSDictionary alloc] initWithObjectsAndKeys:devicetoken,@"token",language,@"language",[NSNumber numberWithBool:enabled],@"enabled", nil];
                               
}`

**Note: if erverything is correct you should receive a message from log alerting the data was updated in server. Otherwise take a repeat the last steps**

*SecureUDID: is the library used by PPy to generate a private UDID for the user. You'll find more information [here](http://www.secureudid.org/)*

If you want to show the received notifications in the app you only have to implement the following method of your app delegate:

`-(void)application:(UIApplication *)application didReceiveRemoteNotification:(NSDictionary *)userInfo{

    NSLog(@"Notification received");
    NSDictionary *apsInfo = [userInfo objectForKey:@"aps"];
    UIAlertView *alertView=[[UIAlertView alloc] initWithTitle:@"Notification" message:[apsInfo objectForKey:@"alert"] delegate:self cancelButtonTitle:@"Cancel" otherButtonTitles: @"OK", nil];
        [alertView show];
}`

**Remember, to use the iOS PPy library you only have to import PPyController and SecureUDID from the library folder**



