# MIT licensed
# Copyright (c) 2013-2017 lilydjwg <lilydjwg@gmail.com>, et al.

import structlog

from . import session, conf_cacheable_with_name

logger = structlog.get_logger(logger_name=__name__)

URL = 'https://www.archlinux.org/packages/search/json/'

get_cacheable_conf = conf_cacheable_with_name('archpkg')

REPO_MAP = {
  'stable': ['Core', 'Extra', 'Community', 'Multilib'],
  'testing': ['Testing', 'Community-Testing', 'Multilib-Testing'],
  'kde-unstable': ['KDE-Unstable'],
}

async def get_version(name, conf, **kwargs):
  pkg = conf.get('archpkg') or name
  strip_release = conf.getboolean('strip-release', False)
  provided = conf.get('provided')

  # TODO: undocumented in aiohttp - passing params as a sequence
  params = [("name", pkg)]

  repos = REPO_MAP[conf.get('channel', 'stable')]
  for repo in repos:
      params.append(("repo", repo))

  async with session.get(URL, params=params) as res:
    data = await res.json()

  if not data['results']:
    logger.error('Arch package not found', name=name)
    return

  r = [r for r in data['results'] if r['repo'] != 'testing'][0]

  if provided:
    provides = dict(x.split('=', 1) for x in r['provides'])
    version = provides.get(provided, None)
    if strip_release:
      version = version.split('-', 1)[0]
  elif strip_release:
    version = r['pkgver']
  else:
    version = r['pkgver'] + '-' + r['pkgrel']

  return version
