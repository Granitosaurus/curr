import click
import re
import json
import os
from datetime import datetime
from urllib import request
import logging
from urllib.error import HTTPError, URLError
from pathlib import Path

import toml

logging.basicConfig(level=logging.INFO)
log = logging.getLogger('curr')
log.setLevel(logging.INFO)

CONFIG = Path(os.path.expanduser(os.environ.get('XDG_CONFIG_HOME') or '~/.config')) / 'curr'


class ConfigManager:
    default_conf = {
        'update_days': 5,
        'output_format': '{result:.2f}',
    }

    def __init__(self, basedir=CONFIG):
        self.dir = Path(basedir)
        self.rc = self.dir / 'currrc'
        self.conf = self.load_config()

    def load_config(self):
        """return config dictionary and initiate default directories and files if they don't exist"""
        conf = self.default_conf
        if not os.path.exists(self.dir):
            os.makedirs(self.dir)
        if os.path.exists(self.rc):
            conf.update(toml.loads(open(self.rc).read()))
        else:
            with open(self.rc, 'w') as f:
                toml.dump(conf, f)
        return conf

    def get_currency_data(self, currency):
        """update currency data files if outdated"""
        # only update if cached file is expired
        currency = currency.upper()
        filename = CONFIG / f'{currency}.json'
        if os.path.exists(filename):
            data = json.loads(open(filename).read())
            if (datetime.now() - datetime.strptime(data['date'], '%Y-%m-%d')).days < self.conf['update_days']:
                return data
        # download and update cached file
        try:
            source = request.urlopen(f'http://api.fixer.io/latest?base={currency.upper()}').read()
        except HTTPError as err:
            if err.code == 422:
                exit(f'ERROR: unknown currency {currency}')
        except (ConnectionError, URLError):  # todo figure out which errors are no internet errors
            if os.path.exists(filename):
                log.warning(f'No internet connection: outdated currency for {currency}: {data["date"]}')
                return data
            else:
                exit(f"Error: No internet connect and cached data doesn't exist")
        else:
            data = json.loads(source)
            log.info(f'updated {currency} @ {data["date"]}')
            with open(CONFIG / f'{currency}.json', 'wb') as f:
                f.write(source)
            return data

    def __getitem__(self, item):
        return self.conf[item]


@click.command()
@click.argument('from_what')
@click.argument('to_what')
@click.option('--basedir', help=f'directory where configuration and cached data is stored, default: {CONFIG}')
@click.option('-v', '--verbose', help='show info messages', is_flag=True)
def cli(from_what, to_what, verbose, basedir):
    """
    Simple currency converter.
    e.g. "curr 100usd eur" -> 85.164
    """
    if not verbose:
        log.setLevel(logging.ERROR)
    try:
        from_num, from_cur = re.split('(\d+\.*\d*)', from_what)[1:]
        from_num = float(from_num)
    except Exception:
        exit('Invalid input values')
    from_cur = from_cur.strip().upper()
    conf = ConfigManager(basedir=basedir or CONFIG)
    data = conf.get_currency_data(from_cur)
    output_format = conf['output_format']
    click.echo(output_format.format(
        result=data['rates'][to_what.upper()] * int(from_num),
        amount=from_num,
        currency=from_cur,
        result_cur=to_what))
    log.info(f'{from_cur} last updated: {data["date"]}')


if __name__ == '__main__':
    cli()
