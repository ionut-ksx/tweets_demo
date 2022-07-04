from flask import Flask, Blueprint, jsonify, render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename

import os
import ipdb


home_blueprint = Blueprint("home", __name__)


@home_blueprint.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")
