# Audit Log Service - Book Store
## Overview

This audit log service has been implemented as a feature of a basic virtual book store. A new user can create his account providing his details and then order available books. He can see quantities of books and a simple reminder of the payment at the top of the page.<br>

On the other hand, the admin can deactivate user's accounts, update quantity of books, check 
The audit log service monitors four types of events:
* signing in,
* logging in,
* ordering and updating books,
* deactivating user accounts

and writes them to the database.

### Technologies
This API has been written in Python 3.9.7. using Flask, Sqlite and SQLAlchemy. Its endpoint appears as three HTML pages. <br>
To simplify the solution, the visual aspect of the application has been omitted.

## How to run the app on Linux

Clone the repository in any chosen folder and run the following command in the terminal:<br>
<code>cd audit_log_service && python3 app.py</code> <br>
Hold the `Ctrl` key and right click on http://127.0.0.1:3000/ in the terminal (or just simply click at this link)

If you are new to the shop, you can simply sign in. 

If you want to check the admin side, log in with following credentials:<br>
Login: `admin`, Password: `password`

### CURL testing
(TBD)

## Further improvements
* Secure user's password and store only hash functions in the database
* Add useful functionalities for users - deactivating their accounts, changing passwords
* Provide more information about books - create separate pages for them
* Introduce more admin roles and a super admin role, which could manage other administrators
* Add a CSS stylesheet
* Enable admins to manage books and orders
