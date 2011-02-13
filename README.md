AppEngine boilerplate with several out of the box goodies:

* [html5-boilerplate](https://github.com/paulirish/html5-boilerplate)
* [Jinja2 templating engine](https://github.com/mitsuhiko/jinja2)
* OpenID login with [openid-selector](http://code.google.com/p/openid-selector/)

You can see the boilerplate live **[here](http://ae-boilerplate.appspot.com)**.

This project is freely available under the [BSD license] [1], all code included is also
covered by the BSD. You can do with it whatever you want!

   [1]: http://www.opensource.org/licenses/bsd-license.php

Jinja2 Templating Engine
------------------------
Alternative templating engine with similar syntax to AppEngine and Django
templates. ``{% cycle %}`` which is broken with AppEngine's templating works.

To update jinja2, replace ``/jinja2`` with the newer version. 

HTML5-Boilerplate
-----------------
[html5 boilerplate] [1] is a great base setup and toolkit for the frontend part of the 
project, including a build script which minifies and compresses html, css, javascript and 
images. The only modification to the standard html5-boilerplate is adding a 
few blocks to ``/static_dev/index.html``: ``{% block header|main|scripts|footer %}``

html5-boilerplate is located in ``/static_dev``, and it's build script 
outputs an optimized copy to ``/static_dev/publish``.

During development, ``/static`` is a symlink to ``/static_dev``, in order to 
not having to rebuild for testing every change. Before publishing the project, 
run the boilerplate build script and change the reference of ``/static`` from 
``/static_dev`` to ``/static_dev/publish``

    # go into html5-boilerplate's build directory    
    $ cd static_dev/build 
    
    # run ant, which compiles an optimized version into static_dev/publish
    $ ant
    
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
    
OpenID Integration
==================

User authentication with OpenID works out of the box, including a nice user 
interface with the [openid-selector] [1] jQuery plugin (also used by [stackoverflow] [2]).

![Alt text](http://lh4.ggpht.com/_IfEh7XYTTeE/STA1yGHn79I/AAAAAAAAADc/IXKrRpick4w/step1.png)

More infos about appengine and openid:

* [http://code.google.com/appengine/articles/openid.html](http://code.google.com/appengine/articles/openid.html)
* [http://blog.notdot.net/2010/05/Using-OpenID-authentication-on-App-Engine](http://code.google.com/appengine/articles/openid.html)
    
   [1]: http://code.google.com/p/openid-selector/
   [2]: http://stackoverflow.com/users/login

