import os
import re
import time

import docker
import yaml
from app.validation import validate_config

config_path = os.path.join(os.path.dirname(__file__), "config-file.yaml")
copy_path = os.path.join(os.path.dirname(__file__), "copy-config-file.yaml")


def pre_checking():
    try:
        start_containers()
        return True
    except docker.errors.APIError as err:
        return docker.errors.APIError(f"ERROR! {err}")


def get_all_containers(path=config_path):
    with open(path) as conf:
        return yaml.safe_load(conf)


def get_cont_by_name(name):
    for cont in get_all_containers():
        if cont["name"] == name:
            return cont


def update_timestamp(new_stamp):
    with open(os.path.join(os.path.dirname(__file__), "timestamp.txt"), "w") as stamp:
        stamp.write(str(new_stamp))


def update_config(new_data, path=copy_path):
    with open(path, "w") as conf:
        yaml.dump(new_data, conf)


def start_containers():
    client = docker.from_env()
    conts = client.containers
    containers = get_all_containers()
    watch_file_update()
    for container in containers:
        cont_name = container["name"]
        options, img_name = container["options"], container["image_name"]
        port, pub_url = container["port"], container["public_url"]
        if not conts.list(all=True, filters={"name": cont_name}):
            run_container(cont_name, options, img_name, port, pub_url)
            update_config(containers, config_path)
            update_config(containers, copy_path)
        elif conts.get(cont_name).status != "running":
            conts.get(cont_name).start()
            print(f"Container {cont_name} started!")
        else:
            print(f"Container {cont_name} is running!")


def change_container(old_name, new_name, new_opts, new_image, new_port, new_url):
    containers = get_all_containers()
    client = docker.from_env()
    for cont in containers:
        if cont["name"] == old_name:
            container = client.containers.get(old_name)
            container.stop()
            container.remove()
            run_cont = run_container(new_name, new_opts, new_image, new_port, new_url)
            cont["name"] = new_name
            cont["options"], cont["image_name"] = new_opts, new_image
            cont["port"], cont["public_url"] = new_port, new_url
            update_config(containers, config_path)
            update_config(containers)
            update_timestamp(os.stat(config_path).st_mtime)
            return run_cont


def check_ports(options, port, host_port):
    if "ports" not in options:
        options["ports"] = {port: host_port}
        return options
    if (
        isinstance(options["ports"][port], list)
        and host_port not in options["ports"][port]
    ):
        options["ports"][port].append(host_port)
        return options
    if (
        not isinstance(options["ports"][port], list)
        and host_port != options["ports"][port]
    ):
        options["ports"][port] = [options["ports"][port]]
        options["ports"][port].append(host_port)
        return options
    return options


def run_container(cont_name, options, img_name, port, pub_url):
    client = docker.from_env()
    conts = client.containers
    host_port = int(re.search(r"http://localhost:(\d*)", pub_url).group(1))
    options["detach"] = True
    options["name"] = cont_name
    options = check_ports(options, port, host_port)
    # create container
    try:
        container = conts.run(image=img_name, **options)
        print(f"Container {container.name} run!")
        return container
    except TypeError:
        raise docker.errors.APIError("Fail in run container. Change parameters")


def add_container(cont_name, options, img_name, port, pub_url):
    cont_config = {
        "name": cont_name,
        "options": options,
        "image_name": img_name,
        "port": port,
        "public_url": pub_url,
    }
    run_cont = run_container(cont_name, options, img_name, port, pub_url)
    containers = get_all_containers()
    containers.append(cont_config)
    update_config(containers, config_path)
    update_config(containers)
    update_timestamp(os.stat(config_path).st_mtime)
    return run_cont


def remove_container(name):
    client = docker.from_env()
    container = client.containers.get(name)
    container.stop()
    container.remove()
    containers = get_all_containers()
    containers.remove(get_cont_by_name(name))
    update_config(containers, config_path)
    print(f"Container {name} stopped and removed")
    update_config(containers)
    update_timestamp(os.stat(config_path).st_mtime)


def watch_file_update():
    time_path = os.path.join(os.path.dirname(__file__), "timestamp.txt")
    if not os.path.exists(copy_path):
        with open(copy_path, "x") as copy_conf:
            yaml.dump(get_all_containers(), copy_conf)
    while True:
        time.sleep(1)
        if os.path.exists(time_path):
            with open(time_path) as stamp:
                timestamp = float(stamp.read().strip())
                file_stamp = os.stat(config_path).st_mtime
                if timestamp != file_stamp:
                    print("They are different")
                    find_changed_cont_and_update()
                    return True
                print("No changes!")
                return False
        else:
            with open(time_path, "w") as stamp:
                stamp.write(str(os.stat(config_path).st_mtime))


def find_changed_cont_and_update():
    new_conts = get_all_containers()
    old_conts = get_all_containers(copy_path)
    len_new, len_old = len(new_conts), len(old_conts)
    client = docker.from_env()
    conts = client.containers
    if len_old > len_new:
        for cont in old_conts[len_new:]:
            container = conts.get(cont["name"])
            container.stop()
            container.remove()
            print(f"Container {cont['name']} stopped and removed")
    for ind, container in enumerate(new_conts):
        if container not in old_conts:
            container = (
                validate_config(container, old_conts[ind])
                if ind < len_old
                else validate_config(container)
            )
            if ind < len_old:
                old_cont = conts.get(old_conts[ind]["name"])
                old_cont.stop()
                old_cont.remove()
            new_name = container["name"]
            new_opts, new_image = (
                container["options"],
                container["image_name"],
            )
            new_port, new_url = (
                container["port"],
                container["public_url"],
            )
            run_container(new_name, new_opts, new_image, new_port, new_url)
    update_config(new_conts, config_path)
    config_timestamp = os.stat(config_path).st_mtime
    update_config(new_conts, copy_path)
    update_timestamp(config_timestamp)
