import bcrypt
from functools import wraps
from flask import Flask, redirect, render_template, request, session ,url_for
from flask import Flask

app = Flask (__name__)

@app.route('/')
def hello_world():
return 'hi'



