"""
Volume Creator.

Usage:
  volume create [<id>] <name> [<pool>]
  volume -h | --help
  volume --version
  volume delete
Arguments:
  id     The unique identifier of the storage-system. Default: '1'
  name   The unique name of the volume to be defined
  pool   The name of the storage-pool to define the volume on. Default: Pick a random pool
Options:
  -h --help     Show this screen.
  --version     Show version.
"""
import requests
import docopt
import json
from pprint import pprint, pformat
import logging
from requests import HTTPError

from base import Properties, get_session

props = Properties()

LOG = logging.getLogger(__name__)


def get_pool_by_name(con, sys_id, name):
    result = con.get('http://{server}/devmgr/v2/storage-systems/{id}/storage-pools'.format(server=props.server,
                                                                                           id=sys_id))
    result.raise_for_status()
    pools = result.json()
    if name is None:
        return pools[0] if pools else None
    else:
        pool = [pool for pool in pools if pool['name'] == name]
        return pool[0] if pool else None


def create_volume(sys_id, vol_name, pool_name=None):
    """Issue a request to define a new volume
    :param sys_id: the unique identifier of the system
    :param vol_name: the name of the new volume
    :param pool_name: an optional pool name
    """
    con = get_session()
    pool = get_pool_by_name(con, sys_id, pool_name)
    if pool is None:
        LOG.error('Unable to locate a valid pool to use!')
        raise NameError('No such pool!')

    LOG.info("Defining a volume on [%s] with name [%s] in pool [%s]." % (sys_id, vol_name, pool['name']))

    data = {'name': vol_name,
            'size': '1',
            'poolId': pool['id']}

    result = con.post('http://{server}/devmgr/v2/storage-systems/{id}/volumes'.format(
        server=props.server, id=sys_id), data=json.dumps(data))

    if result.status_code == 422:
        resp = result.json()
        LOG.warn("Volume creation failed: %s" % resp.get('errorMessage'))
    elif result.status_code == 200:
        LOG.info("Volume [%s] created successfully" % vol_name)
        LOG.debug(pformat(result.json()))
    else:
        LOG.error(result.text)

    result.raise_for_status()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(relativeCreated)dms %(levelname)s %(module)s.%(funcName)s:%(lineno)d\n %(message)s')
    args = docopt.docopt(__doc__)
    vol_name = args.get('<name>')
    sys_id = args.get('<id>', '1')
    pool_name = args.get('<pool>')
    create_volume(sys_id, vol_name, pool_name)
