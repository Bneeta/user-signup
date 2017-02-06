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
import re
import cgi

USER_RE = re.compile(r"^[a-zA-z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)



# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>SignUp</title>
    <style type="text/css">
    .label{text-align:right}
    .error {color: red;}
    </style>
</head>
<body>
    <h1> SignUp </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # a form for adding new movies
        signup_form = """
        <form action="/signup" method="post">
          <table>
            <tr>
            <td class ="label">
                Username
            </td>
            <td>
              <input type="text" name="username" value="" required=""/>
            </td>
            <td class="error">
            </td>
            </tr> <br><br>

            <tr>
            <td class ="label">
                Password
            </td>
            <td>
              <input type="password" name="password" value="" required=""/>
            </td>
            <td class ="error">
            </td>
            </tr> <br><br>

            <tr>
            <td class ="label">
                 Verify Password
            </td>
            <td>
              <input type="password" name="verify" value="" required=""/>
            </td>
            <td class= "error">
            </td>
            </tr> <br><br>


            <tr>
            <td class ="label">
                Email(Optional)
            </td>
            <td>
              <input type="text" name="email" value="" />
            </td>
            <td class = "error">
            </td>
            </tr>
            </table> <br><br>
            <input type="submit" value="Submit Query"/>
        </form>
        """
        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""

        content= page_header+signup_form+error_element+page_footer
        self.response.write(content)


class Signup(webapp2.RequestHandler):
    def post(self):
        username=self.request.get("username")
        password=self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        if not valid_username(username):
            error= "That's not a valid username."
            error_escaped=cgi.escape(error,quote =True)
            self.redirect("/?error="+error_escaped)

        elif not valid_password(password):
            error= "That's not a valid password."
            error_escaped=cgi.escape(error,quote =True)
            self.redirect("/?error="+error_escaped)

        elif password!=verify:
            error= "Your passwords didn't match."
            error_escaped=cgi.escape(error,quote =True)
            self.redirect("/?error="+error_escaped)

        elif not valid_email(email):
            error= "That's not a valid email."
            error_escaped=cgi.escape(error,quote =True)
            self.redirect("/?error="+error_escaped)

        else :
            self.redirect("/welcome?username= "+username)


page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
<h1>SignUp</h1>
"""

class Welcome(webapp2.RequestHandler):
    def get(self):
        username=self.request.get("username")
        content=page_header+"""<h1>""" + """Welcome, """+username+"""</h1>"""+ page_footer
        self.response.write(content)






app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup',Signup),
    ('/welcome',Welcome)

], debug=True)
