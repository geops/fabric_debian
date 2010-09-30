from fabric.api import *
from fabric.utils import abort
import re


def list_debs():
    """
    """
    package_list = run("dpkg -l").split("\n")

    re_debs = re.compile("^(?P<status>[a-zA-Z]{2})\s+(?P<package>[a-zA-Z\.\-_0-9]+)\s+(?P<version>[^\s]+)\s+(?P<description>.*)$")

    packages={}
    for line in package_list:
        m = re_debs.match(line)
        if m:
            mdict = m.groupdict()
            packages[mdict["package"]] = mdict

    return packages


def is_installed(debs):
    """
    no version check so far
    """
    if type(debs) in (str, unicode):
        debs = list(debs)

    packages = list_debs()
    missing = []
    for deb in debs:
        if not packages.has_key(deb):
            missing.append(deb)
        else:
            if packages[deb]["status"] == "rc":
                missing.append(deb)

    if len(missing) != 0:
        abort("The following debs are missing: %s" % ", ".join(missing))
