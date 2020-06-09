CS1999: Buggy Race Editor
=========================

> This is the "buggy editor" component of the Foundation Year Computer Science
> project at RHUL.


Overview
--------
This is a web app designed to create buggies. It runs as a webserver so you
can edit the configuration of a buggy in your browser. The editor can then
generate the data, in JSON format, that you need in order to enter races on
the [race server](http://rhul.buggyrace.net).

The application is written in Python3 using the
[Flask](https://palletsprojects.com/p/flask/) microframework.

GitHub repo: [RHUL-CS-Projects/CS1999-buggy-race-editor](https://github.com/RHUL-CS-Projects/CS1999-buggy-race-editor])


Developing in a browswer: repl.it
---------------------------------
You can access this on [https://repl.it](https://repl.it).

* fork this repo into your own GitHub account
* log into repl.it
* click on "+ new repl"
* click on "Import from GitHub"
* enter the URL of your forked repo
* click **Import from GitHub**
* when it's finished, click **Run**

You've got a file browser, editor, website pane and shell window all in your
browser. Because you forked from your copy of the repo, you can `git push`
any changes you make back there.


Installation & set up
---------------------

Getting the editor running on your own machine differs depending on which
operating system you're using. The principles are the same, but the way to
execute them is slightly different.


### Summary

The recommended way to run this app this on your own machine is to first 
install it:

* install the software (clone this repo)
* create a virtual evironment
* install the dependencies (e.g., Flask) in that environment

Then, to run the application:

* activate the virtual environment
* run the app
* kill the app with Ctl-C
* deactivate the virutal environment

This varies a little depending on which platform you are using.

### Prerequisites

You must have these two things installed before you can start:

* [Python 3](https://www.python.org) for programming
* [Git](https://git-scm.com) for version control

If they are not already installed on your machine, see the
downloads/installation instructions on their respevtive websites.


#### Installation

When you first install the buggy editor webserver you need to install some
Python modules. Instead of installing them on your whole machine (which might
be a problem if other applications need different versions of the same
libraries) it's best to create a virtual environment just for this project, and
work inside that.

On Windows you can follow these instructions in the PowerShell. Alternatively
if you use the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10)
(WSL) you can follow the instructions as Linux.

For Mac or Unix-like systems, open a Terminal window.

To create the virtual environment, first `cd` to the directory which contains
the application files (you might have use `git clone` to create it). Then do:

    python3 -m venv venv

This creates a directory, called `venv`, where Python will keep the library
files this virtual environment uses.

Python has created a file inside that directory that you can execute at any
time to activate the virtual environment. Once you've activated it, all
subsequent python commands operate within the scope of this environment
(instead of your whole machine).

Activate the virtual environment. On Windows, do:

    .\venv\Scripts\activate
    
On Linux or Mac:

    source venv/bin/activate

Next, install the libraries the app needs. Because you activated `venv`, they
will be installed in this virtual environment:

    pip install -r requirements.txt

Finally, set up the database:

The database is already configured when cloning the program. To begin,
create an account from the link in the header and this will allow buggies
to be created, modified and submitted using the editor. One admin account
is configured on loading the program which has full admin capabilities
including password resetting, account deletion and giving other users
admin capabilities. This account is set to be undeletable to ensure there
is always one admin account in the system. It is important to ensure that
this database is not deleted as this contains values used in the methods
in the app.


#### Running the server

`cd` into the project directory and then activate the virtual environment.

On Windows, do:

    .\venv\Scripts\activate
    
On Linux or Mac:

    source venv/bin/activate

Set the environment variable to `development`. On Windows do:

    $env:FLASK_ENV = 'development'

On Linux or Mac:

    export FLASK_ENV=development

Now you can run the application:

    FLASK_APP=__init__.py python -m flask run

The webserver is running on port 5000 (the default for Flask apps).

Go to [http://localhost:5000](http://localhost:5000) in your web browser.
You haven't specified which file you want, so you'll get the `/` route, which
(you can see this by looking in `app.py`) invokes the `index.html` template.

#### Development Mode

Development mode allows changes to automatically apply to the server without
needed to be restarted. This also means that any errors in the code are shown
and a traceback is given instead of a blank error page. To enable this, ensure
the following two commands are run after initialising the virtual environment
and before starting the flask server.
    
    export FLASK_ENV=devlopment
    export FLASK_DEBUG=1   


#### Shutting down the server

In the terminal where the webserver is running, press Control-C. This
interrupts the server and halts the execution of the program.

If you've finished, you can deactivate the virtual environment:

    deactivate

You're done!
