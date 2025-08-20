# SPDX-FileCopyrightText: Copyright (c) 2013-2014 micropython-lib contributors
#
# SPDX-License-Identifier: MIT


def warn(msg, cat=None, stacklevel=1):
    print("%s: %s" % ("Warning" if cat is None else cat.__name__, msg))
