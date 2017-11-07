#!/usr/bin/env python
"""
Copy headers from source files to destination files.

Headers are defined as the comment and blank lines before the first line that
is not such a thing.

Source and destination could be files or dirs, in which case headers
will be copied across all files with the same name.
"""

import os
import re
import sys

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s')

opt = None


class ScriptError(Exception):
    """Controlled exception raised by the script."""


def main():
    global opt
    opt = parse_cmdline()

    errs = False

    if os.path.isdir(opt.src):
        for dst in opt.dst:
            try:
                sync_dirs(opt.src, dst)
            except ScriptError as e:
                logger.error("error: %s", e)
                errs = True

    else:
        for dst in opt.dst:
            try:
                sync_files(opt.src, dst)
            except ScriptError as e:
                logger.error("error: %s", e)
                errs = True

    return 1 if errs else 0


def sync_dirs(src, dst):
    for fn in (src, dst):
        if not os.path.isdir(fn):
            raise ScriptError("the path '%s' is not a directory" % fn)

    logger.info("syncing directory '%s' -> '%s'", src, dst)
    fns = os.listdir(src)
    fns.sort()
    for fn in fns:
        if os.path.exists(os.path.join(dst, fn)):
            sync_files(os.path.join(src, fn), os.path.join(dst, fn))


def sync_files(src, dst):
    for fn in (src, dst):
        if not os.path.isfile(fn):
            raise ScriptError("the path '%s' is not a file" % fn)

    logger.info("syncing file '%s' -> '%s'", src, dst)

    if opt.dry_run:
        return

    lines = []
    with open(src) as f:
        for l in f:
            if l.isspace() or opt.pattern.match(l):
                lines.append(l)
            else:
                break

    with open(dst) as f:
        f = iter(f)
        while 1:
            l = f.next()
            if not (l.isspace() or opt.pattern.match(l)):
                break

        lines.append(l)
        lines.extend(f)

    with open(dst, 'w') as f:
        f.write(''.join(lines))


def parse_cmdline():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('src', help="source file or directory")
    parser.add_argument('dst', nargs='+', help="target file or directory")
    parser.add_argument('--pattern', default=r'\s*#',
        help="pattern to recognise a comment [default: %(default)s]")
    parser.add_argument('-n', '--dry-run', action='store_true',
        help="just say what you would do [default: %(default)s]")

    opt = parser.parse_args()

    try:
        opt.pattern = re.compile(opt.pattern)
    except Exception as e:
        parser.error("bad pattern regexp: '%s': %s" % (opt.pattern, e))

    return opt


if __name__ == '__main__':
    sys.exit(main())
