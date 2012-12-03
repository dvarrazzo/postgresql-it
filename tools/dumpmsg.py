#!/usr/bin/env python
"""Dump all strings for bulk spellcheck.
"""

import sys
import glob
import polib

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s')


class ScriptError(Exception):
    """Controlled exception raised by the script."""

class CheckFailed(Exception):
    """Some translation check failed"""

def main():
    opt = parse_cmdline()

    rv = 0
    for fn in [fn for pat in opt.files for fn in glob.glob(pat)]:
        po = polib.pofile(fn)
        for entry in po:
			print entry.msgstr.encode('utf8')

    return rv

def parse_cmdline():
    import optparse

    parser = optparse.OptionParser(usage="%prog  file [...]")
    opt, args = parser.parse_args()
    opt.files = args

    return opt


if __name__ == '__main__':
    try:
        sys.exit(main())

    except ScriptError, e:
        logger.error("%s", e)
        sys.exit(1)

    except Exception, e:
        logger.error("Unexpected error: %s - %s",
            e.__class__.__name__, e, exc_info=True)
        sys.exit(1)

    except KeyboardInterrupt:
        logger.info("user interrupt")
        sys.exit(1)
