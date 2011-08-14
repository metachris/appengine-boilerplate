import logging
import urllib2
import settings

try:
    import simplejson as json
except ImportError:
    import json


def mailchimp_subscribe(email, list_id=None, double_optin=True):
    """
    Subscribes this email to your mailchimp newsletter. If list_id is not
    set it will default to settings.MAILCHIMP_LIST_ID.
    """
    ms = MailSnake(settings.MAILCHIMP_API_KEY)
    list_id = list_id or settings.MAILCHIMP_LIST_ID
    res = ms.listSubscribe(id=list_id, email_address=email, \
            double_optin=double_optin)
    logging.info("MailChimp: Subscribed user %s to list %s. Result: %s", email,
            list_id, res)


def mailchimp_unsubscribe(email, list_id=None, delete_member=False,
        send_goodbye=True, send_notify=True):
    """
    Unsubscribes this email from your mailchimp newsletter. If list_id is not
    set it will default to settings.MAILCHIMP_LIST_ID.
    """
    ms = MailSnake(settings.MAILCHIMP_API_KEY)
    list_id = list_id or settings.MAILCHIMP_LIST_ID
    res = ms.listUnsubscribe(id=list_id, email_address=email,
            delete_member=delete_member, send_goodbye=send_goodbye,
            send_notify=send_notify)

    logging.info("MailChimp: Unsubscribed user %s from list %s. Result: %s",
            email, list_id, res)


class MailSnake(object):
    """
    MailSnake is a simple MailChimp API Wrapper.
    - URL: https://github.com/leftium/mailsnake
    - Author: John-Kim Murphy (https://github.com/leftium)
    """
    def __init__(self, apikey='', extra_params={}):
        if not apikey:
            raise ValueError("MailChimp API Key not valid. Set in settings.py")

        self.apikey = apikey

        self.default_params = {'apikey': apikey}
        self.default_params.update(extra_params)

        dc = 'us1'  # Overwritten if part of the API key
        if '-' in self.apikey:
            dc = self.apikey.split('-')[1]
        self.base_api_url = 'https://%s.api.mailchimp.com/1.3/?method=' % dc

    def call(self, method, params={}):
        url = self.base_api_url + method
        params.update(self.default_params)

        post_data = json.dumps(params)
        headers = {'Content-Type': 'application/json'}
        request = urllib2.Request(url, post_data, headers)
        response = urllib2.urlopen(request)

        return json.loads(response.read())

    def __getattr__(self, method_name):
        def get(self, *args, **kwargs):
            params = dict((i, j) for (i, j) in enumerate(args))
            params.update(kwargs)
            return self.call(method_name, params)

        return get.__get__(self)
