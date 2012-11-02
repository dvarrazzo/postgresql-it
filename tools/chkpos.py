#!/usr/bin/env python
"""Check the translations consistency.
"""

import re
import sys
import polib
import glob

import logging
logger = logging.getLogger()
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s %(message)s')


class CheckFailed(Exception):
    """Some translation check failed"""

def main():
    checks = [ cls() for cls in globals().itervalues()
        if type(cls) == type and issubclass(cls, Check)
        and cls is not Check]
    for check in checks:
        logger.debug("performing check: %s", check.__class__.__name__)

    rv = 0
    for fn in [fn for arg in sys.argv[1:] for fn in glob.glob(arg)]:
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

class Check(object):
    def check(self, entry):
        raise NotImplementedError

    def messages(self, entry):
        """Return the pairs (msgid, msgstr) to check.

        Deal with plural entries. Skip fuzzy entries.
        """
        if 'fuzzy' in entry.flags:
            return

        if not entry.msgid_plural:
            yield (entry.msgid, entry.msgstr)
        else:
            yield (entry.msgid, entry.msgstr_plural['0'])
            yield (entry.msgid_plural, entry.msgstr_plural['1'])


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

class CheckPreixWhitespace(CheckWhitespace, Check):
    _chk_re = re.compile(r'^\s*')

class CheckSufixWhitespace(CheckWhitespace, Check):
    _chk_re = re.compile(r'\s*$')

class CheckPlaceholders(Check):
    _chk_re = re.compile("(%%)|((%(\.\d+)?[^%]))")

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            p1 = self._chk_re.findall(s1)
            p2 = self._chk_re.findall(s2)
            if p1 != p2:
                raise CheckFailed("placeholders don't match")

if __name__ == '__main__':
    sys.exit(main())

