# -*- coding: utf-8 -*-
""":mod:`libfeedly.utils`
~~~~~~~~~~~~~~~~~~~~~~~~~
"""
import sys
from .compat import quote_plus, urlparse, text

__all__ = 'APIError', 'user_id', 'feed_id', 'category_id', 'tag_id', \
          'escape', 'parse_oauth_code'


class APIError(IOError):
    pass


def user_id(uid):
    """Google user unique id to feedly ``:user_id`` format

    :param uid: Google unique account UUID
    :type uid: :class:`basestring`
    :returns:
    :rtype: :class:`basestring`

        >>> user_id('00000000-0000-0000-0000-000000000000')
        'user/00000000-0000-0000-0000-000000000000'

    """
    return 'user/%s' % uid

def feed_id(uri, escape=False):
    """`atom` or `feed` uri to feedly ``:feed_id`` format

    :param uri: `atom` or `rss` address
    :type uri: :class:`basestring`
    :param escape:
    :type escape: :class:`bool`
    :returns:
    :rtype: :class:`basestring`

        >>> feed_id('http://some/rss')
        'feed/http://some/rss'
        >>> feed_id('http://some/rss', escape=True)
        'feed%2Fhttp%3A%2F%2Fsome%2Frss'

    """
    fid = 'feed/%s' % uri
    return escape and quote_plus(fid) or fid

def category_id(user_id, label, escape=False):
    """category label to feedly ``:category_id`` format

    :param user_id: ``:user_id`` format data
    :type user_id: :class:`basestring`
    :param label:
    :type label: :class:`basestring`
    :param escape:
    :type escape: :class:`bool`
    :returns:
    :rtype: :class:`basestring`

        >>> category_id('user/abc', 'a')
        'user/abc/category/a'
        >>> category_id('user/abc', u'가나다')
        'user/abc/category/가나다'
        >>> category_id('user/abc', u'가나다', escape=True)
        'user%2Fabc%2Fcategory%2F%EA%B0%80%EB%82%98%EB%8B%A4'

    """
    cid = '%s/category/%s' % (user_id, text(label))
    return escape and quote_plus(cid.encode('utf-8')) or cid

def tag_id(user_id, tag, escape=False):
    """tag to feedly ``:tag_id`` format

    :param user_id: ``:user_id`` format data
    :type user_id: :class:`basestring`
    :param tag:
    :type tag: :class:`basestring`
    :param escape:
    :type escape: :class:`bool`
    :returns:
    :rtype: :class:`basestring`

        >>> tag_id('user/abc', 'a')
        'user/abc/tag/a'
        >>> tag_id('user/abc', u'가나다')
        'user/abc/tag/가나다'
        >>> tag_id('user/abc', u'가나다', escape=True)
        'user%2Fabc%2Ftag%2F%EA%B0%80%EB%82%98%EB%8B%A4'

    """
    tid = '%s/tag/%s' % (user_id, text(tag))
    return escape and quote_plus(tid.encode('utf-8')) or tid

def parse_oauth_code(end_auth_uri):
    """parse ``code`` param field from oauth chain URI

    :param end_auth_uri:
    :type end_auth_uri: :class:`basestring`
    :returns:
    :rtype: :class:`basestring`

        >>> parse_oauth_code('http://some/?code=abcde&scope=')
        'abcde'
        >>> parse_oauth_code('http://some/?code=abc%20de&scope=')
        'abc%20de'
        >>> parse_oauth_code('http://some/?code=abc+de&scope=')
        'abc+de'
    """
    parse = urlparse(end_auth_uri)
    start = parse.query.find('code=')
    if start < 0:
        return
    q = parse.query[start + 5:]
    end = q.find('&')
    if end < 0:
        return q
    return q[:end]

def escape(string):
    """Escape to html entity string
    """
    string = text(string)
    return quote_plus(string.encode('utf-8'))
