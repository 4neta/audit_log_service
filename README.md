# Audit Log Service - Book Store
## Overview

This audit log service has been implemented as a feature of a basic virtual book store. A new user can create his account providing his details and then order available books. He can see quantities of books and a simple reminder of the payment at the top of the page.<br>

On the other hand, the admin can deactivate user's accounts, update quantity of books, check owning payments and the audit log.

The audit log service monitors four types of events:
* signing in,
* logging in,
* ordering and updating books,
* deactivating user accounts

and writes them to the database.

### Technologies
This API has been written in Python 3.9.7. using Flask, Sqlite and SQLAlchemy. Its endpoint appears as three HTML pages.

To simplify the solution, the visual aspect of the application has been omitted.

![(Here the screenshot should appear)](https://i.ibb.co/X3jF50G/screenshots.png)

## How to run the app on Linux

Clone the repository in any chosen folder and run the following command in the terminal:<br>
<code>cd audit_log_service && python3 app.py</code> <br>
Hold the `Ctrl` key and right click on http://127.0.0.1:3000/ in the terminal (or just at this link).

If you are new to the shop, you can simply sign in. 

If you want to check the admin side, log in with following credentials:<br>
Login: `admin`, Password: `password`

## CURL testing
You might want to test the solution using cURL. <br>
To begin with it, make sure that the server is running. Open a new terminal in another tab or window.

### Logging in
If you want to make a simple GET call on the home page, run: <br>
`curl -v http://127.0.0.1:3000/`

You should see the main page in html. If it doesn't happen, check if you are running the server. (For example, try to visit the link and refresh the page.)

You can also test logging in with uncorrect credentials: <br>
<code>curl -d 'login=nonexistinguser&password=badpassword' http://127.0.0.1:3000/login</code>

You should see the main page again.

And with correct: <br>
<code>curl -d 'login=sbrand&password=password' http://127.0.0.1:3000/login</code>, <br>

which should guide you to the store page. Pay attention to the line <br>
```
Your owning payment is <b>£26</b>. Please send it to: <br>
```

After running this command (which buys the first book): <br>
<code>curl -d 'book_id=1' http://127.0.0.1:3000/buy</code> <br>
you should get the same page with the owning payment increased.

### Admin panel
After that you might want to try testing the admin side.

In this case you can log in using admin credentials:<br>
<code>curl -d 'adminlogin=admin&adminpass=password' http://127.0.0.1:3000/adminlog</code> <br>

(Or check the incorrect credentials which should return the same main page: <br>
<code>curl -d 'adminlogin=admin&adminpass=badpassword' http://127.0.0.1:3000/adminlog</code>)

Within the admin's panel you can test the book quantity update: <br>
<code>curl -d 'book_id=1&add=10' http://127.0.0.1:3000/updatequantity</code>

The number in the following line: <br>
```
1. Zeland Vadim - <b>Reality Transurfing</b> - 169</code> <br>
```
should increase to 179.

You can also try to delete an user.
If you are inside the admin panel, you can see the list of users:
```
<li><b>1.</b>  Admin  - <b>£0</b> - 0 </span></a></li>
<li><b>2.</b>  Arthur Garcia - <b>£27</b> - 722638462 </span></a></li>
<li><b>3.</b>  Sarah Woods - <b>£12</b> - 75332134673 </span></a></li>
```
Then you should run the following command which deletes the account of Arthur Garcia. <br>
`curl -d 'person_id=2' http://127.0.0.1:3000/deleteperson`

And the beginning of the list should change to:
```
<li><b>1.</b>  Admin  - <b>£0</b> - 0 </span></a></li>
<li><b>3.</b>  Sarah Woods - <b>£12</b> - 75332134673 </span></a></li>
```

The last admin's activity is showing the audit log.

Let's show all logs using this command: <br>
`curl -d 'id=1&choice=5' http://127.0.0.1:3000/showlog`

You should see a list of events similar to:
```
<li>admin - <i>Admin login success</i> &nbsp 01/04/2022 19:52:39</li>
```

### Signing in
To test the signing functionality, type: <br>
```
curl -d 'name=name&surname=surname&newlogin=username&newpass=password&phone=777&address=world' http://127.0.0.1:3000/signin
```

You should see the store page starting with:
```
<html>
    <body>
        <h1>Hi, username!</h1>
```

In a case of failure (e.g. non-numerical number), the main page is returned.

## Further improvements
* Secure user's password and store only hash functions in the database
* Add useful functionalities for users - deactivating their accounts, changing passwords
* Provide more information about books - create separate pages for them
* Introduce more admin roles and a super admin role, which could manage other administrators
* Add a CSS stylesheet
* Enable admins to manage books and orders
