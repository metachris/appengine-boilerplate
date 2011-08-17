App Engine Boilerplate is a versatile yet minimalistic setup for new App Engine projects.

* [html5-boilerplate 2.0](https://github.com/paulirish/html5-boilerplate)
(including it's automated build toolchain for minification and concatenation of js+css)
* Beautiful OpenID login with [openid-selector](http://code.google.com/p/openid-selector/)
* Flexible user-preferences model with auto-caching (plus Gravatar link)
* `BaseRequestHandler` for simplified rendering and access to user preferences
* `@login_required` decorator
* Memcaching setup
* Templates and template addons
* Tools such as `is_testenv()` and `slugify(url)`
* Automatically subscribe users to your MailChimp newsletter
* `app.yaml` configuration for admin areas, static files
* Released under the [BSD license](http://www.opensource.org/licenses/bsd-license.php)

This project does not contain a lot of code. To get the best understanding of it's features 
we recommend to simply **browse through the files**! You can see a rather minimalistic live version [here](http://www.appengine-boilerplate.com).


OpenID Authentication
---------------------

User authentication with OpenID works out of the box, including a nice user interface via the [openid-selector] [1] jQuery plugin (also used by [stackoverflow] [2]). Be sure to enable OpenID authentication in your app settings on app engine.

![Alt text](http://lh4.ggpht.com/_IfEh7XYTTeE/STA1yGHn79I/AAAAAAAAADc/IXKrRpick4w/step1.png)

More infos about appengine and openid:

* [http://code.google.com/appengine/articles/openid.html](http://code.google.com/appengine/articles/openid.html)
* [http://blog.notdot.net/2010/05/Using-OpenID-authentication-on-App-Engine](http://code.google.com/appengine/articles/openid.html)
    
   [1]: http://code.google.com/p/openid-selector/
   [2]: http://stackoverflow.com/users/login


Memcaching
----------

Returning cached data usually improves the performance of a website. App Engine provides 
a custom  version of memcache to store various data types, which can be used to efficiently 
cache the results of datastore queries, or commonly used elements on the homepage.

[`app/mc/cache.py`](https://github.com/metachris/appengine-boilerplate/blob/master/app/mc/cache.py) contains an exemplary method of querying data from
memcache with a datastore fallback if not yet cached. Simply adapt as you need it!


HTML5-Boilerplate
-----------------

[html5 boilerplate] [1] is a great base setup for building the website frontend, and furthermore 
includes a build script which minifies and compresses html, css, javascript and images. 

html5-boilerplate is located in ``/static_dev``, and it's build script outputs an optimized release version to ``/static_dev/publish``.The only modification to the standard html5-boilerplate is adding a few blocks to  ``/static_dev/index.html``: ``{% block header|main|scripts|footer %}``

During development the symlink ``/static`` points to ``/static_dev``. On publishing 
the project ``upload_to_appengine.sh`` invokes the html5-boilerplate build script 
and changes the symlink ``/static`` to ``/static_dev/publish``, in order to upload 
the optimized version. 


upload_to_appengine.sh
----------------------

`upload_to_appengine.sh` is a tiny shell script which simplifies invoking the html5-boilerplate build tools before testing and uploading your app to app engine. To use it you need to set ``CMD_APPCFG`` to your local `dev_appserver.py`.

Exact steps of `./upload_to_appengine.sh`:

- Asks if it should run the build process with ``ant minify``
- Changes the /static symlink to the production version
- Waits for you to test and confirm
- Uploads the app to appengine
- Reverts /static to the development environment

These would be the manual steps:

    # go into html5-boilerplate's build directory    
    $ cd static_dev/build 
    
    # run ant, which compiles an optimized version into static_dev/publish
    $ ant minify
    
    # go back into the main directory
    $ cd ../../
    
    # change reference of /static symlink to optimized version
    $ rm static
    $ ln -s static_dev/publish static
    
    # Test the optimized version
    # Publish to web with appcfg.py
    
    # After publishing you can change back to static_dev
    $ rm static
    $ ln -s static_dev static
     
   [1]: https://github.com/paulirish/html5-boilerplate


Adding CSS Files
----------------

CSS files are no longer imported from `index.html` but exclusively through using
`@import` in style.css.

html5 boilerplate automatically includes, minifies and concatenates css files
which are imported via an `@import` statement from within `style.css`. Add
references to your custom stylesheets from there, never from within index.html.


Working in Windows
-------------------
There are a couple of posix symlinks within the project that will need to be updated to work with Windows.

* "/static" which points to "/static_dev" during development
* "/templates/base.html" which points to "/static/index.html"

To create the new links, delete the existing links and use the mklink command from an command prompt run with Administration privileges.

* [mklink](http://technet.microsoft.com/en-us/library/cc753194\(WS.10\).aspx) [[/D] | [/H] | [/J]] Link Target

Making these two changes will enable you to launch the project using the Google App Engine SDK Launcher.  During deployment the current .sh script changes the /static link to /static_dev/publish and a forthcoming .bat script will include this functionality.


Enjoy
----------

Feedback, improvements and critique are greatly appreciated. **Fork away!**


Ideas
-----

Some ideas for future improvements:

* Check for unique username
* Email verification
* Update openid-selector
* OAuth login: Twitter, Facebook, LinkedIn, Dropbox, etc.
* About page with feedback form
* Feedback dialog
* akismet, twitter, bit.ly modules?
