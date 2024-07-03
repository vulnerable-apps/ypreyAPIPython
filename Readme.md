# YrpreyAPIPython

![yprey](https://i.imgur.com/atJ6k90.png)

**Created by [Fernando Mengali](https://www.linkedin.com/in/fernando-mengali-273504142/)**

YrpreyAPIPython is a framework that explains 8 (eight) vulnerabilities of the OWASP TOP 10 API 2023 in a clear and objective way. The framework was developed to teach and learn details in Pentest (penetration testing) and Application Security. In the context of Offensive Security, vulnerabilities contained in web applications can be identified, exploited and compromised. For application security professionals and experts, the framework provides an in-depth understanding of code-level vulnerabilities. Yrprey, making it valuable for educational, learning and teaching purposes in the field of Information Security.

#### API1:2023 Broken Object Level Authorization

![yprey](https://i.imgur.com/6A5D5ir.png)

Note that all requests based on a name do not have hierarchy, organization, segmentation, or profiling. In other words, you can view the names of all users from any team.

#### API2:2023 Broken Authentication

![yprey](https://i.imgur.com/eGoxe2f.png)

Change the token value, even if you enter the wrong username and password, you can authenticate with the token.



#### API3:2023 Broken Object Property Level Authorization

![yprey](https://i.imgur.com/430Bkdb.png)

Enter the wrong username and password to obtain a valid token and use it on the API2:2023 tab to authenticate in the system.



#### API4:2023 Unrestricted Resource Consumption

![yprey](https://i.imgur.com/t54w3FB.png)

Send an image number to the backend, for example 1,000,000. The frontend will receive the response and attempt to render it, causing an application exhaustion.


#### API5:2023 Broken Function Level Authorization

![yprey](https://i.imgur.com/ZL5UhUG.png)

Change the role value and send it to the server; if you set it to 'admin,' you will receive a response indicating administrator access to the system.



#### API7:2023 Server Side Request Forgery

![yprey](https://i.imgur.com/f9mihfv.png)

Send an HTTP request to port 80 to the server and inspect the element; this way, you will obtain data from the web server. If there are more IPs running web servers on the network, you will receive headers from those web servers.

### API8:2023 Security Misconfiguration

![yprey](https://i.imgur.com/G7k2NAx.jpeg)

Identify which headers are in red, indicating security issues that need to be mitigated.


### API9:2023 Improper Inventory Management

![yprey](https://i.imgur.com/WHjvfig.jpeg)

Change the route from v2 to v1, thus exploiting the vulnerability in the validation of the API v1. This issue pertains to obsolete API versions that should be shut down, removed from the production environment, or never published in the first place.



#### Features
 - Based on OWASP's top 10 vulnerabilities for API.

 ## The framework was written with the following technologies:

* 1º - Python
* 3º - Bootstrap - CSS
* 4º - JavaScript
* 5º - MariaDB
* 5º - Ajax

yrpreyAPIPython are not recommended for personal or commercial use, only for laboratory use and learning about exploiting and patching vulnerabilities.

#### List of Vulnerabilities


## How Install

* 1º - Install and configure Apache, PHP and MariaDB on your Linux
* 2º - Import the YRpreyPHP files to /var/www/
* 3º - Create a database named "yrpreyapi"
* 4º - Import the yrprey.sql into the database.
* 5º - Access the address http://localhost in your browser
* 6º - In php ini change allow_url_include to "On".
* 7º - Add the app.py file. Necessary packages for app.py to run successfully.
* 8º - In the Gitbash terminal or Windows Command Prompt, install the packages.


```python

pip install Flask

pip install flask-cors

pip install pymysql

```

9º - In the Gitbash terminal or Windows Command Prompt, start the server with command.
```python
python app.py
```

## Observation
You can test on Xampp or any other platform that supports PHP and MariaDB.

## Reporting Vulnerabilities

Please, avoid taking this action and requesting a CVE!

The application intentionally has some vulnerabilities, most of them are known and are treated as lessons learned. Others, in turn, are more "hidden" and can be discovered on your own. If you have a genuine desire to demonstrate your skills in finding these extra elements, we suggest you share your experience on a blog or create a video. There are certainly people interested in learning about these nuances and how you identified them. By sending us the link, we may even consider including it in our references.
