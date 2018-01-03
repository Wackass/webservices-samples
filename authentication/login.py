"""
Examples of authenticating to the API.

Usage:
  login <username> <password> <server>
  login -h
Arguments:
  username  ID to provide for authentication
  password  Password corresponding to specified userid.
  server    API endpoint.
Options:
  -h --help     Show this screen.
  --version     Show version.

Description:
    There are two ways that you can authenticate to the Web Services API. Both options are viable and are demonstrated
     below with examples.

    Basic-Authentication is probably the most popular option, especially for shorter/simpler usages of the API, mostly
     because of its simplicity. The credentials are simply provided with each request.

    There is a login endpoint (POST /devmgr/utils/login), that will allow you to explicitly authenticate with the API.
     Upon authenticating, a JSESSIONID will be provided in the Response headers and as a Cookie that can be utilized
     to create a persistent session (that will eventually timeout).
"""

import logging

import docopt
import requests

LOG = logging.getLogger(__name__)


def login(server, username, password):
    # Define a re-usable Session object and set some standard headers
    con = requests.Session()
    con.headers.update({'Accept': 'application/json', 'Content-Type': 'application/json'})

    # Here we do a login that will define a persistent session on the server-side upon successful authentication
    result = con.post(server + "/devmgr/utils/login", json={'userId': username, 'password': password})

    # You'll notice the JSESSIONID as a part of the Response headers
    LOG.info("Headers: %s", result.headers)

    # Notice how the JSESSIONID is now set as a cookie on the Session object?
    LOG.info("Cookie Set: JSESSIONID: %s", con.cookies.get('JSESSIONID'))

    # Now we make a subsequent request to a different Resource. Notice how the JESSIONID is persisted on the connection?
    #  Requests is intelligent enough to perist the cookie that is sent back in the Response on the requests.Session()!
    result = con.get(server + "/devmgr/v2/storage-systems")
    assert result.cookies.get('JSESSIONID') == con.cookies.get('JSESSIONID')

    # Now let's avoid using a persistent session with the login
    result1 = requests.post(server + "/devmgr/utils/login", json={'userId': username, 'password': password})
    # Okay, now we have a different JSESSIONID, that's okay, that's what we expected.
    assert result1.cookies.get('JSESSIONID') != con.cookies.get('JSESSIONID')

    result2 = requests.get(server + "/devmgr/v2/storage-systems", auth=(username, password))
    # Uh oh, we got an authentication error!?! That's because the JESSIONID wasn't set on a persistent session,
    #  and we didn't use Basic-Auth to authenticate directly!
    LOG.warn("Request without a session or auth: %s", result2.status_code)

    # This time we'll provide credentials using Basic-Authentication
    result2 = requests.get(server + "/devmgr/v2/storage-systems", auth=(username, password))
    # It works, but we got a new session.
    assert result1.cookies.get('JSESSIONID') != result2.cookies.get('JSESSIONID')

    # We can do something similar to what requests does for us by manually persisting the cookie. This may be necessary
    #  for less full-featured clients.
    result1 = requests.post(server + "/devmgr/utils/login", json={'userId': username, 'password': password})

    result2 = requests.get(server + "/devmgr/v2/storage-systems", cookies=result1.cookies)
    # See, they match, and we don't have to provide authentication for this request!
    assert result1.cookies.get('JSESSIONID') == result2.cookies.get('JSESSIONID')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)dms %(levelname)s %(module)s.%(funcName)s:%(lineno)d\n %(message)s')
    args = docopt.docopt(__doc__)
    login(args.get('<server>'), args.get('<username>'), args.get('<password>'))
