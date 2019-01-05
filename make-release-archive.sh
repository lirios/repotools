#!/bin/sh
#
# This file is part of Liri.
#
# Copyright (C) 2019 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:MIT$
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#
# $END_LICENSE$
#

test $# -eq 2 || { echo "Usage: $(basename $0) <name> <tag>" >&2; exit 1; }

workdir=$(dirname `readlink -f $0`)

name=$1
tag=$2
version=${tag#v}
prefix=${name}-${version}

rm -f ${prefix}.tar ${prefix}.tar.xz

{
    git archive --format=tar --prefix=$prefix/ $tag > ${prefix}.tar
    p=`pwd` && (git submodule foreach) | while read entering path; do
        temp="${path%\'}"
        temp="${temp#\'}"
        path=$temp
        [ "$path" = "" ] && continue
        (cd $path && git archive --format=tar --prefix=${prefix}/$path/ HEAD > /tmp/tmp.tar && tar --concatenate --file=${p}/${prefix}.tar /tmp/tmp.tar && rm /tmp/tmp.tar)
    done
    xz -9 ${prefix}.tar
} || {
    rm -f ${prefix}.tar ${prefix}.tar.xz
}
