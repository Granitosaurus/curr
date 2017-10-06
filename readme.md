curr
====

`curr` is a minimalistic and simple currency converter command line application:

    Usage: curr [OPTIONS] FROM_WHAT TO_WHAT

      Simple currency converter. e.g. "curr 100usd eur" -> 85.164

    Options:
      -v, --verbose  show info messages
      --help         Show this message and exit.

## Install

curr requires python3.6 or later, to install simply run:

    pip install --user git+https://github.com/Granitosaurus/curr@v1.0

on arch linux `curr` can be found on AUR:

    pacaur -S curr
    # or
    yaourt -S curr

## Example

    $curr 100usd eur
    85.16

## Configure

curr saves config files can be found at `$XDG_CONFIG_HOME/curr/` directory (which is usually `~/home/user/curr`)
you can configure `currrc` for curr details:

    update_days = 5
    output_format = "{result:.3f}"

`update_days` = amount of days cache should be kept
`output_format` = pythonic format of output where result will be filled in with resulting number

