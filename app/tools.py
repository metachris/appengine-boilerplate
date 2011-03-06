from os import environ


def is_textenv():
    """
    True if devserver, False if appengine server

    Appengine uses  'Google App Engine/1.4.2',
    Devserver  uses 'Development/1.0'
    """
    return environ.get('SERVER_SOFTWARE', '').startswith('Development')
