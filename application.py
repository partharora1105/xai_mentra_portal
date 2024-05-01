import os
import csv
from datetime import datetime
# from werkzeug.utils import secure_filename

from flask import Flask, redirect, url_for, request, render_template, send_from_directory

import sqlite3
from flask import g
import json
import re



app = Flask(__name__, static_folder="static")
localDomain = "http://127.0.0.1:5000/"
publicDomain = "http://www.gtxr.club"
DOMAIN = localDomain

localPath = ""
publicPath = "/home/GTXR/mysite/"
PATH = localPath

extension = ""
root_key = "My Profile"


def is_positive_integer(value):
    try:
        int_value = int(value)
        return int_value > 0
    except (ValueError, TypeError):
        return False

app.jinja_env.filters['is_positive_integer'] = is_positive_integer


@app.route("/")
def openHome():
    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'r') as file:
        data = json.load(file)
    for k,v in data[root_key].items():
        data[root_key][k] = len(v)
    json_file = PATH + f"static/data/curr_tree.json"
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    return render_template("index.html", nodes = data, domain=DOMAIN)


def get_leaves_and_parents(tree, leaves, parent_map, path=[]):
    for key, value in tree.items():
        if type(value) == int or not value:  # Check if the node is a leaf
            leaves.append(key)
            parent_map[key] = path[:]
        else:
            path.append(key)
            get_leaves_and_parents(value, leaves, parent_map, path)
            path.pop()

@app.route("/expand/expand/<k>")
def doubleExpandTree(k):
    return redirect(url_for('expandTree', k=k))


@app.route("/expand/<k>")
def expandTree(k):
    json_file = PATH + f"static/data/curr_tree.json"
    with open(json_file, 'r') as file:
        curr_tree = json.load(file)
    leaves = []
    parent_map = {}
    get_leaves_and_parents(curr_tree, leaves, parent_map)
    try:
        path = parent_map[k]
    except KeyError:
        return redirect(url_for('openHome'))


    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'r') as file:
        nodes = json.load(file)

    curr = nodes[root_key]
    for key in path[1:]:
        curr = curr[key]
    curr = curr[k]
    for key,val in curr.items():
        curr[key] = len(val)
    tree_to_expand = curr
    
    print(tree_to_expand)
    current_node = curr_tree
    for key in path:
        current_node = current_node[key]
    current_node[k] = tree_to_expand

    json_file = PATH + f"static/data/curr_tree.json"
    with open(json_file, 'w') as file:
        json.dump(curr_tree, file, indent=4)
    data = curr_tree

    return render_template("index.html", nodes = data, domain=DOMAIN)


def find_key_path(input_key, current_dict, path=[]):
    for key, value in current_dict.items():
        # Append the current key to the path
        new_path = path + [key]
        if key == input_key:
            return new_path  # Return the path if the key is found
        elif isinstance(value, dict):
            # If the value is a dictionary, recursively search for the key in it
            found_path = find_key_path(input_key, value, new_path)
            if found_path:
                return found_path  # Return the path if the key is found within this branch
    return None  # Return None if the key is not found

@app.route("/expand/add/<k>")
def doubleAddTree(k):
    return redirect(url_for('addToTree', k=k))

@app.route("/add/<k>")
def addToTree(k):
    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'r') as file:
        nodes = json.load(file)
    path = find_key_path(k, nodes)
    print(path)
    node = nodes
    for key in path[:-1]:
        node = node[key]

    node[path[-1]]["just_added"] = {}
    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'w') as file:
        json.dump(nodes, file, indent=4)
    return redirect(url_for('openHome'))
    return path_to_key
    
    leaves = []
    parent_map = {}
    get_leaves_and_parents(curr_tree, leaves, parent_map)
    try:
        path = parent_map[k]
    except KeyError:
        return redirect(url_for('openHome'))




    return render_template("index.html", nodes = data, domain=DOMAIN)



    # Print the parent map
    print("Parent map:")
    for leaf, parents in parent_map.items():
        print(leaf, ":", " -> ".join(parents))


    return leaves
    json_file = PATH + f"static/data/nodes.json"
    with open(json_file, 'r') as file:
        data = json.load(file)
    for k,v in data[root_key].items():
        data[root_key][k] = len(v)
    data = dict(data)
    return render_template("index.html", text="Hello World", nodes = data, domain=DOMAIN)


if __name__ == "__main__":
    app.debug = True
    app.run()
