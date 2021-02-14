import ast

import docker
from app import app
from app.containers import (
    add_container,
    change_container,
    get_all_containers,
    get_cont_by_name,
    pre_checking,
    remove_container,
    start_containers,
    watch_file_update,
)
from app.forms import AddContainerForm, Buttons, ContainerForm
from flask import Flask, flash, redirect, render_template, request, url_for


@app.route("/", methods=["GET", "POST"])
def containers():
    check = pre_checking()
    form = Buttons()
    conts = get_all_containers()
    if check is not True:
        print(check)
        return render_template("errors.html", error=check)
    if form.validate_on_submit():
        return redirect(url_for("add"))
    return render_template("containers.html", conts=conts, form=form)


@app.route("/")
@app.route("/cont/<cont_name>", methods=["GET", "POST"])
def cont(cont_name):
    check = pre_checking()
    cont = get_cont_by_name(cont_name)
    form = Buttons()
    if check is not True:
        print(check)
        return render_template("errors.html", error=check)
    if form.edit.data:
        return redirect(url_for("change", cont_name=cont_name))
    elif form.remove.data:
        return redirect(url_for("remove", cont_name=cont_name))
    if not cont:
        flash(f"Container {cont_name} changed")
        return redirect("/")
    return render_template("cont.html", cont=cont, form=form)


@app.route("/")
@app.route("/remove/<cont_name>", methods=["GET", "POST"])
def remove(cont_name):
    cont_name = cont_name
    remove_container(cont_name)
    flash(f"Container {cont_name} stopped and removed")
    return redirect("/")


@app.route("/")
@app.route("/change/<cont_name>", methods=["GET", "POST"])
def change(cont_name):
    cont = get_cont_by_name(cont_name)
    form = ContainerForm(cont_name)
    try:
        if form.validate_on_submit():
            new_name = form.cont_name.data
            new_opts, new_image = (
                ast.literal_eval(form.options.data),
                form.img_name.data,
            )
            new_port, new_url = form.port.data, form.pub_url.data
            rerun_cont = change_container(
                cont_name, new_name, new_opts, new_image, new_port, new_url
            )
            flash(f"Changes requested for container {rerun_cont.name} applied!")
            return redirect(url_for("cont", cont_name=rerun_cont.name))
        elif request.method == "GET":
            form.cont_name.data = cont["name"]
            form.options.data = cont["options"]
            form.img_name.data = cont["image_name"]
            form.port.data = cont["port"]
            form.pub_url.data = cont["public_url"]
        return render_template("changes.html", title="Change container", form=form)
    except docker.errors.APIError as er:
        flash(f"An ERROR! {er}")
        return redirect(url_for("change", cont_name=cont_name))


@app.route("/")
@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddContainerForm()
    if form.validate_on_submit():
        new_name = form.cont_name.data
        new_opts = ast.literal_eval(form.options.data)
        new_image = form.img_name.data
        new_port, new_url = form.port.data, form.pub_url.data
        try:
            container = add_container(new_name, new_opts, new_image, new_port, new_url)
            flash(f"Add and run new container {container.name}!")
            return redirect(url_for("cont", cont_name=container.name))
        except docker.errors.APIError as er:
            flash(f"An ERROR! {er}")
            return redirect(url_for("add"))
    elif request.method == "GET":
        form.options.data = "{'detach': True}"
    return render_template("changes.html", title="Add new container", form=form)
