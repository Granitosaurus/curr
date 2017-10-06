import click
import re
import json
import os
from datetime import datetime
from urllib import request
import logging
from urllib.error import HTTPError
from pathlib import Path

import toml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('curr')
CONFIG = Path(os.environ.get('XDG_CONFIG_HOME') or '~/.config') / 'curr'
CONFIG_RC = CONFIG / 'currrc'
DEFAULT_CONF = {
    'update_days': 5,
    'output_format': '{result:.2f}',
}


class ConfigManager:
    def __init__(self):
        if not os.path.exists(CONFIG):
            os.makedirs(CONFIG)
        self.conf = DEFAULT_CONF
        if os.path.exists(CONFIG_RC):
            self.conf.update(toml.loads(open(CONFIG_RC).read()))
        with open(CONFIG_RC, 'w') as f:
            toml.dump(self.conf, f)

    def check_update(self, base):
        # only update if cached file is expired
        filename = CONFIG / f'{base}.json'
        if os.path.exists(filename):
            data = json.loads(open(filename).read())
            if (datetime.now() - datetime.strptime(data['date'], '%Y-%m-%d')).days < self.conf['update_days']:
                return
        # download and update cached file
        try:
            source = request.urlopen(f'http://api.fixer.io/latest?base={base.upper()}').read()
        except HTTPError as err:
            if err.code == 422:
                exit(f'ERROR: unknown currency {base}')
        except ConnectionError:
            log.warning('No internet connection: currency info might be outdated!')
        data = json.loads(source)
        log.info(f'updated {base} @ {data["date"]}')
        with open(CONFIG / f'{base}.json', 'wb') as f:
            f.write(source)

    def get_config(self, base):
        filename = CONFIG / f'{base}.json'
        self.check_update(base)
        return json.loads(open(filename).read())

    def __getitem__(self, item):
        return self.conf[item]


@click.command()
@click.argument('from_what')
@click.argument('to_what')
@click.option('-v', '--verbose', help='show info messages', is_flag=True)
def cli(from_what, to_what, verbose):
    """
    Simple currency converter.
    e.g. "curr 100usd eur" -> 85.164
    """
    if not verbose:
        log.setLevel(logging.ERROR)
    from_num, from_cur = re.split('(\d+)', from_what)[1:]
    from_cur = from_cur.strip().upper()
    conf = ConfigManager()
    data = conf.get_config(from_cur)
    output_format = conf['output_format']
    click.echo(output_format.format(result=data['rates'][to_what.upper()] * int(from_num)))
    log.info(f'{from_cur} last updated: {data["date"]}')


if __name__ == '__main__':
    cli()
