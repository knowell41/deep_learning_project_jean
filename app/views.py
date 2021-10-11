from flask import render_template
from flask import Flask, request, render_template, session, redirect, flash, url_for, send_from_directory
import numpy as np
import pandas as pd
from app import app
import os


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/app')
def application():
    return render_template("app.html")

@app.route('/sourcecode')
def sourceCode():
    return render_template("source.html")

@app.route('/about')
def about():
    return render_template("about.html")
