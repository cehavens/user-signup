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
#

import os
import webapp2
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)


def valid_password(password):
    return PASSWORD_RE.match(password)


def valid_email(email):
    return EMAIL_RE.match(email)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render_content(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        self.render_content("signup.html")

    def post(self):
        username_provided = self.request.get("username")
        pw_provided = self.request.get("password")
        pw_verification_provided = self.request.get("verify_pw")
        email_provided = self.request.get("email")

        user_valid = ""
        pw_valid = ""
        pw_match = ""
        email_valid = ""
        all_valid = True

        feedback = dict(username_provided = username_provided, email_provided = email_provided)

        if valid_username(username_provided):
            user_valid = True
        else:
            user_valid = False
            all_valid = False
            feedback["invalid_username"] = "Please provide a valid password."

        if valid_password(pw_provided):
            pw_valid = True
        else:
            pw_valid = False
            all_valid = False
            feedback["invalid_password"] = "Please provide a valid password."

        if pw_provided == pw_verification_provided:
            pw_match = True
        else:
            pw_match = False
            all_valid = False
            feedback["pw_mismatch"] = "The passwords entered do not match."

        if email_provided and valid_email(email_provided):
            email_valid = True
        elif not email_provided:
            email_valid = True
        else:
            email_valid = False
            all_valid = False
            feedback["invalid_email"] = "The email entered is not valid."

        if all_valid:
            self.redirect("/welcome?username=" + username_provided)
        else:
            self.render_content("signup.html", **feedback)


class WelcomePage(Handler):
    def get(self):
        welcome = "Thank you for signing up, " + self.request.get("username") + "!"
        self.write(welcome)


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/welcome', WelcomePage)
], debug=True)
