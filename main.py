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
import webapp2
import cgi
import re

head = "<head><title>User Signup</title></head>"
header = "<h2>User Signup</h2>"
layout_form_start = "<form name=\"signup\" method=\"post\">\
                    <table><tbody>"
layout_form_end = "</tbody></table><input type=\"submit\" value=\"Submit\"/></form>"


class MainHandler(webapp2.RequestHandler):
    def get(self, name_error="", pw_error="", email_error="", name="", email=""):

        pw_error_element = "<span class='error' style=\"color: red;\">" + pw_error + "</span>"
        name_error_element = "<span class='error' style=\"color: red;\">" + name_error + "</span>"
        email_error_element = "<span class='error' style=\"color: red;\">" + email_error + "</span>"
        
        un = ("<tr><td><label>Username</label></td><td><input name=\"username\" type=\"username\" required=\"\" value=\""
              + name + "\"/>" + name_error_element + "</td></tr>")
        pw = "<tr><td><label>Password</label></td><td><input name=\"password\" type=\"password\" required=\"\"/></td></tr>"
        vf = ("<tr><td><label>Verify Password</label></td><td><input name=\"verify\" type=\"password\" required=\"\"/>"
              + pw_error_element + "</td></tr>")
        email = ("<tr><td><label>Email (optional)</label></td><td><input name=\"email\" type\"email\" value=\""
                 + email + "\"/>" + email_error_element + "</td></tr>")

        page_top = head + header + layout_form_start
        content = page_top + un + pw + vf + email + layout_form_end
        self.response.write(content)

    def post(self):
        password = cgi.escape(self.request.get("password"))
        verify = cgi.escape(self.request.get("verify"))
        name = cgi.escape(self.request.get("username"))
        name_escaped = cgi.escape(name)
        email = cgi.escape(self.request.get("email"))

        name_test = re.search("[^A-Za-z]", name)
        email_test = re.match(r"[^@]+@[^@]+\.[^@]+", email)

        if name_test:
            name_error = "Username has invalid characters."
            self.get(name_error, "", "", name, email)

        elif not email_test and email != "":
            email_error = "Email address is invalid."
            self.get("", "", email_error, name, email)

        elif password != verify:
            pw_error = "Passwords do not match."
            self.get("", pw_error, "", name, email)

        else:
            self.response.write('Welcome, ' + name)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
