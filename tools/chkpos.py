#!/usr/bin/env python
"""Check the translations consistency.
"""

import re
import sys
import glob
import polib
from operator import attrgetter

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

    classes = [ cls for cls in globals().itervalues()
        if type(cls) == type and issubclass(cls, Check)
        and cls is not Check]

    if opt.tests:
        checks = []
        for test in opt.tests:
            for cls in classes:
                if cls.__name__ == test:
                    checks.append(cls())
                    break
            else:
                raise ScriptError("test not known: %s" % test)

    else:
        checks = [ c() for c in classes ]

    for check in checks:
        logger.debug("performing check: %s", check.__class__.__name__)

    rv = 0
    for fn in [fn for pat in opt.files for fn in glob.glob(pat)]:
        po = polib.pofile(fn)
        for entry in po:
            for check in checks:
                try:
                    check.check(entry)
                except CheckFailed, e:
                    rv = 1
                    logger.error("%s failed in %s: %s\n%s",
                        check.__class__.__name__, fn, e, entry)

    return rv

def get_check_classes():
    classes = [ cls for cls in globals().itervalues()
        if type(cls) == type and issubclass(cls, Check)
        and cls is not Check ]
    classes.sort(key=attrgetter('__name__'))
    return classes

def parse_cmdline():
    from optparse import OptionParser
    parser = OptionParser(usage="%prog [options] file [...]",
        description="check message catalogs consistency")
    parser.add_option('--test', metavar="NAME", dest="tests", action='append',
        help="run the test NAME. Can be specified more than once."
            " If not specified, run all the tests."
            " Available tests are: %s"
            % ', '.join(map(attrgetter('__name__'), get_check_classes())))

    opt, args = parser.parse_args()
    opt.files = args

    return opt

class Check(object):
    def check(self, entry):
        raise NotImplementedError

    def messages(self, entry):
        """Return the pairs (msgid, msgstr) to check.

        Deal with plural entries. Skip fuzzy entries.
        """
        # skip obsolete, fuzzy and missing translations
        if entry.obsolete:
            return

        if 'fuzzy' in entry.flags:
            return

        if not entry.msgstr:
            return

        if not entry.msgid_plural:
            yield (entry.msgid, entry.msgstr)
        else:
            yield (entry.msgid, entry.msgstr_plural['0'])
            try:
                yield (entry.msgid_plural, entry.msgstr_plural['1'])
            except KeyError:
                pass


class CheckWhitespace(object):
    _chk_re = None

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            m1 = self._chk_re.search(s1)
            m2 = self._chk_re.search(s2)

            if m1 is None and m2 is None:
                return

            if m1 is None or m2 is None:
                raise CheckFailed("only one matches")

            if m1.group() != m2.group():
                raise CheckFailed("match failed")

class PrefixWhitespace(CheckWhitespace, Check):
    _chk_re = re.compile(r'^\s*')

class SuffixWhitespace(CheckWhitespace, Check):
    _chk_re = re.compile(r'\s*$')


class Placeholders(Check):
    _chk_re = re.compile(r"(?:%%)|(%(?:\d+\$)?(?:\.\d+)?[^%])")

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            p1 = [ s for s in self._chk_re.findall(s1) if s ]
            p2 = [ s for s in self._chk_re.findall(s2) if s ]

            if not p1 and not p2:
                return

            # reorder shuffled placeholders
            if '$' in ''.join(p2):
                p2.sort(key=lambda s: int(re.match(r'%((\d+)\$)', s).group(2)))
                p2 = [re.sub(r'\d+\$', '', s) for s in p2]

            if p1 != p2:
                raise CheckFailed("placeholders don't match")

class CheckOption(object):
    _chk_re = None

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            m1 = self._chk_re.search(s1)
            m1 = m1 and m1.group(1)
            m2 = self._chk_re.search(s2)
            m2 = m2 and m2.group(1)
            if m1 != m2:
                raise CheckFailed("option don't match")

class ShortOption(CheckOption, Check):
    _chk_re = re.compile(r'(?:\s|^)(-[a-zA-Z0-9])\b')

class LongOption(CheckOption, Check):
    _chk_re = re.compile(r'(?:\s|^)(--[^\s=A-Z]+)\b')

class PsqlCommand(CheckOption, Check):
    _chk_re = re.compile(r'(?:\s|^)(\\[^\s]+)\b')


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
