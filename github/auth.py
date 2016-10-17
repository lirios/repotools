#
# This file is part of Liri.
#
# Copyright (C) 2016 Pier Luigi Fiorini <pierluigi.fiorini@gmail.com>
#
# $BEGIN_LICENSE:BSD$
#
# You may use this file under the terms of the BSD license as follows:
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of the Liri project nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Pier Luigi Fiorini BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# $END_LICENSE$
#

import os
import github3

def two_factor_function():
    code = ""
    while not code:
        code = input("Enter 2FA code: ")
    return code

def authorize(credentials_file, scopes, note, note_url):
    if os.path.exists(credentials_file):
        token = id = ""
        with open(credentials_file, "r") as fd:
            token = fd.readline().strip()
            id = fd.readline().strip()
    else:
        from getpass import getpass
        username = input("Username: ")
        password = ""
        while not password:
            password = getpass("Password for {0}: ".format(username))
        auth = github3.authorize(username, password, scopes, note, note_url, two_factor_callback=two_factor_function)
        with open(credentials_file, "w") as fd:
            fd.write(auth.token + "\n" + str(auth.id))
        token = auth.token
        id = str(auth.id)
    gh = github3.login(token=token)
    return gh
