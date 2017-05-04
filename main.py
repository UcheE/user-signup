#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import webapp2
import re
import cgi

page_header = """
<!DOCTYPE html>
<html>
<head>
    <title><h1>Signup<h1></title>
</head>
<body>
</body>
</html>
"""

form = """
<form method="post"><strong><h1>
    Signup
    </h1></strong>
    <br>
    <label>Username
        <input type="text" name="name" value="%(user_name)s">
    </label>
    <div style="color: red">%(erroruname)s</div>

    <label>Password
        <input type="password" name="password" value="">
    </label>
    <div style="color: red">%(errorPassword)s</div>

    <label>Verify password
        <input type="password" name="passwordverify" value="">
    </label>
    <div style="color: red">%(errorPasswordverify)s</div>

    <label>Email (option)
        <input type="text" name="email" value="%(user_email)s">
    </label>
        <div style="color: red">%(errorEmail)s</div>
    <input type="submit">
</form>
"""

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(user_name):
    return user_name and USER_RE.match(user_name)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(user_password):
    return user_password and PASS_RE.match(user_password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(user_email):
    return not user_email or EMAIL_RE.match(user_email)


class Signup(webapp2.RequestHandler):
    # creates form
    def write_form(self, erroruname="", errorPassword="", errorPasswordverify="", errorEmail="", user_name="", user_email=""):
        self.response.write(form % {"erroruname": erroruname,
                                    "errorPassword": errorPassword,
                                    "errorPasswordverify": errorPasswordverify,
                                    "errorEmail": errorEmail,
                                    "user_name": cgi.escape(user_name),
                                    "user_email": cgi.escape(user_email)})

    def get(self):
        self.write_form()

    def post(self):

        user_name = self.request.get('name')
        user_password = self.request.get('password')
        user_passwordverify = self.request.get('passwordverify')
        user_email = self.request.get('email')

        has_error = False
        errors = {"user_name": user_name, "user_email": user_email}

        if not valid_username(user_name):
            has_error = True
            errors["erroruname"] = "Not a valid name."

        if not valid_password(user_password):
            has_error = True
            errors["errorPassword"] = "Not a valid password."

        if user_password != user_passwordverify:
            has_error = True
            errors["errorPasswordverify"] = "These passwords don't match."

        if not valid_email(user_email):
            has_error = True
            errors["errorEmail"] = "Not a valid email."

        if has_error:
            self.write_form(**errors)
        else:
            self.redirect('/welcome?username='+user_name)


class Welcome(webapp2.RequestHandler):
    def get(self):
        #self.response.write("<h1>Welcome, %s!</h1>" % user_name)
        self.response.write("<h1>Welcome,</h1> "+self.request.get("username") )

app = webapp2.WSGIApplication([
    ('/', Signup),
    ('/welcome', Welcome),
], debug=True)
