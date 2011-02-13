AppEngine boilerplate with Jinja2 templates and html5-boilerplate.

* [html5-boilerplate](https://github.com/paulirish/html5-boilerplate/tree/master)
* [Jinja2 templating engine](https://github.com/mitsuhiko/jinja2)

To update jinja2, replace ``/jinja2`` with the newer version. For 
html5-boilerplate update ``/static_dev`` with the new version. The only 
modification to the standard html5-boilerplate is adding three blocks to 
index.html: {% block header|main|footer %}

To update your static folder with index.html, js and css, invoke the 
html5-boilerplate build script:

    $ cd static_dev/build 
    $ ant
    