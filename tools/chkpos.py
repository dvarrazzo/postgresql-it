#!/usr/bin/env python
"""Check the translations consistency.
"""

import re
import sys
import glob
import polib
import codecs
from operator import attrgetter
from itertools import count

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
        checks = [ c() for c in classes if c.default ]

    for check in checks:
        logger.debug("performing check: %s", check.__class__.__name__)

    if opt.fix:
        return _check_and_fix(opt, checks)
    else:
        return _check_only(opt, checks)

def _check_only(opt, checks):
    rv = 0
    for fn in [fn for pat in opt.files for fn in glob.glob(pat)]:
        po = polib.pofile(fn)
        for entry in po:
            for check in checks:
                try:
                    check.check(entry)
                except CheckFailed, e:
                    logger.error("%s failed in %s: %s\n%s",
                        check.__class__.__name__, fn, e, entry)
                    rv = 1
    return rv

def _check_and_fix(opt, checks):
    for fn in [fn for pat in opt.files for fn in glob.glob(pat)]:
        po = polib.pofile(fn)
        errs = []
        for entry in po:
            for check in checks:
                try:
                    check.check(entry)
                except CheckFailed, e:
                    errs.append(entry)
                    logger.error("%s failed in %s: %s\n%s",
                        check.__class__.__name__, fn, e, entry)
                    check.fix(entry)

        # save the file if there has been an update
        if errs:
            update_file(po, errs)

    return 0

def update_file(po, entries):
    """Update a few entries and save the file inplace.

    Leave the file unchanged for all the rest. Just using polib's file leaves
    a mess of spurious changes.
    """
    with codecs.open(po.fpath, 'r', po.encoding) as f:
        lines = f.readlines()

    i = 0
    # assume the entries are in order and all are to be found
    for entry in entries:
        # look for the entry by occurrency instead of by key. The key could be
        # wrapped so it's harder to parse
        if not entry.occurrences:
            logger.warn("can't fix entry: no occurrency:\n%s", entry)
            continue

        if entry.msgid_plural:
            logger.warn("can't fix plural entries:\n%s", entry)
            continue

        occ = u':'.join(entry.occurrences[-1])
        for i in count(i):
            line = lines[i]
            if not line.startswith(u'#:'):
                continue
            if occ in line and occ in line.split():
                break

        # look for the msgfmt
        for i in count(i+1):
            line = lines[i]
            if line.startswith(u'msgstr'):
                start = i
                break

        # look for the end of the msgfmt
        for i in count(i+1):
            line = lines[i]
            if not line.startswith(u'"'):
                end = i
                break
        assert line.isspace()

        # replace with the new string
        s = entry._str_field('msgstr', '', '', entry.msgstr, wrapwidth=0)
        lines[start:end] = [ line + u'\n' for line in s ]
        i -= (end - start) + 1

    # replace the file
    with codecs.open(po.fpath, 'w', po.encoding) as f:
        for line in lines:
            f.write(line)

def get_check_classes():
    classes = [ cls for cls in globals().itervalues()
        if type(cls) == type and issubclass(cls, Check)
        and cls is not Check ]
    classes.sort(key=attrgetter('__name__'))
    return classes

def parse_cmdline():
    import optparse

    class DontTouchTheEpilog(optparse.IndentedHelpFormatter):
        def format_epilog(self, epilog):
            if epilog:
                return "\n" + epilog + "\n"
            else:
                return ""

    parser = optparse.OptionParser(usage="%prog [options] file [...]",
        description="check message catalogs consistency",
        formatter=DontTouchTheEpilog(),
        epilog="Available tests are:\n" + '\n'.join(
            "  - %s%s: %s" % (
                    cls.__name__,
                    not cls.default and '(*)' or '',
                    cls.__doc__)
                for cls in get_check_classes()))
    parser.add_option('--test', metavar="NAME", dest="tests", action='append',
        help="run the test NAME. Can be specified more than once."
            " If not specified, run all the tests"
            " (except the ones marked with *).")
    parser.add_option('--fix', action='store_true',
        help="fix the broken entries if possible and save the .po inplace")

    opt, args = parser.parse_args()
    opt.files = args

    return opt


class Check(object):
    default = True

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

    def set_msgstr(self, entry, msgstr, idx=0):
        if not entry.msgid_plural:
            if idx:
                raise ValueError(
                    "setting idx=%r of a non-plural entry" % idx)
            entry.msgstr = msgstr
        else:
            entry.msgstr_plural[str(idx)] = msgstr

    def fix(self, entry):
        pass


class CheckWhitespace(object):
    _chk_re = None

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            m1 = self._chk_re.search(s1)
            m2 = self._chk_re.search(s2)

            assert m1 is not None and m2 is not None, "regex match failed"

            if m1.group() != m2.group():
                raise CheckFailed("match failed")

    def fix(self, entry):
        for i, (s1, s2) in enumerate(self.messages(entry)):
            m1 = self._chk_re.search(s1)
            m2 = self._chk_re.search(s2)

            assert m1 is not None and m2 is not None, "regex match failed"

            if m1.group() != m2.group():
                s2 = self._chk_re.sub(m1.group(), s2)
                self.set_msgstr(entry, s2, i)


class PrefixWhitespace(CheckWhitespace, Check):
    """check that the leading whitespaces are equal"""
    _chk_re = re.compile(r'^\s*')

class SuffixWhitespacePedantic(CheckWhitespace, Check):
    """check that the trailing whitespaces are equal"""
    _chk_re = re.compile(r'\s*$')
    default = False

class SuffixWhitespace(SuffixWhitespacePedantic):
    """check that the trailing nonempty whitespaces are equal"""
    default = True
    def check(self, entry):
        for s1, s2 in self.messages(entry):
            m1 = self._chk_re.search(s1)
            assert m1 is not None, "regex match failed"
            if not m1.group():
                return

            m2 = self._chk_re.search(s2)
            assert m2 is not None, "regex match failed"

            if m1.group() != m2.group():
                raise CheckFailed("match failed")

class ClearBrokenEntries(object):
    """Mixin class to remove broken translations."""
    def fix(self, entry):
        for i, (s1, s2) in enumerate(self.messages(entry)):
            self.set_msgstr(entry, '', i)


class Placeholders(ClearBrokenEntries, Check):
    """check that the placeholders are consistent"""
    _chk_re = re.compile(r"(?:%%)|(%(?:\d+\$)?(?:\.\d+)?[^%])")

    def check(self, entry):
        for s1, s2 in self.messages(entry):
            p1 = [ s for s in self._chk_re.findall(s1) if s ]
            p2 = [ s for s in self._chk_re.findall(s2) if s ]

            if not p1 and not p2:
                return

            # Reorder shuffled placeholders.
            # Allow partially reordered placeholders, e.g.
            #   p1 = [u'%u', u'%s', u'%m']
            #   p2 = [u'%2$s', u'%1$u', u'%m']
            # are probably fine.
            if '$' in ''.join(p2):
                p2o = p2[:]
                for i, s in enumerate(p2):
                    m = re.match(r'%((\d+)\$)', s)
                    if m:
                        p2o[int(m.group(2)) - 1] = re.sub(r'\d+\$', '', s)

                p2 = p2o

            if p1 != p2:
                raise CheckFailed("placeholders don't match")

class CheckOption(ClearBrokenEntries):
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
    """check that the short options (e.g. -x) are consistent"""
    _chk_re = re.compile(r'(?:\W|^)(-[a-zA-Z0-9])\b')

class LongOption(CheckOption, Check):
    """check that the long options (e.g. --foo) are consistent"""
    _chk_re = re.compile(r'(?:\W|^)(--[a-z0-9-]+)\b')

class PsqlCommand(CheckOption, Check):
    """check that the psql commands (e.g. \\dX[+]) are consistent"""
    _chk_re = re.compile(r'(?:\W|^)(\\[^\s]+)\b')


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
