import re

import docker


def validate_config(new_cont, old_cont=None):
    client = docker.from_env()
    conts = client.containers
    imgs = client.images
    if "options" not in new_cont:
        new_cont["options"] = {}

    new_name = new_cont["name"]
    new_opts, new_image = (
        new_cont["options"],
        new_cont["image_name"],
    )
    new_port, new_url = (
        new_cont["port"],
        new_cont["public_url"],
    )

    def check_image():
        try:
            imgs.pull(new_image)
        except docker.errors.APIError as api:
            raise docker.errors.APIError("Invalid image. Change it.")

    check_image()

    if old_cont:
        # validate changes in container
        old_name = old_cont["name"]

        def check_free_port(port):
            for container in conts.list(all=True, filters={"publish": port}):
                if container.name != old_name:
                    raise docker.errors.APIError(
                        f"Port {port} is already allocated. Please, choose another port"
                    )

        def validate_name():
            if old_name != new_name:
                if conts.list(all=True, filters={"name": new_name}):
                    raise docker.errors.APIError(
                        f"The container name '{new_name}' is already in use. Change this name"
                    )

        def validate_url():
            port = int(re.search(r"http://localhost:(\d+)", new_url).group(1))
            pub_url = re.search(r"(http://localhost:\d+)", new_url)
            if not pub_url or new_url != pub_url.group(1):
                raise docker.errors.APIError(
                    "Public URL should be in form: 'http://localhost:<free host port>'"
                )
            check_free_port(port)

        def validate_options():
            if not isinstance(new_opts, dict):
                raise docker.errors.APIError(
                    "This field should be in form: {option_1: value_1, option_2: value_2, etc}"
                )
            if "ports" not in new_opts:
                return
            cont_port = list(new_opts["ports"])
            if new_port not in cont_port:
                print(f"New port {cont_port}")
                raise docker.errors.APIError(
                    f"Ports {cont_port} should contain port {new_port}"
                )
            host_ports = new_opts["ports"].values()
            for port in host_ports:
                if isinstance(port, list):
                    for p in port:
                        check_free_port(p)
                check_free_port(port)

        validate_name(), validate_url(), validate_options()
        return new_cont

    # validate new container

    def check_port(port):
        if conts.list(all=True, filters={"publish": port}):
            raise docker.errors.APIError(
                f"Port {port} is already allocated. Please, choose another port"
            )

    # validate container name
    if conts.list(all=True, filters={"name": new_name}):
        raise docker.errors.APIError(
            f"The container name '{new_name}' is already in use. Change this name"
        )
    # validate options
    if not isinstance(new_opts, dict):
        raise docker.errors.APIError(
            "This field should be in form: {option_1: value_1, option_2: value_2, etc}"
        )
    # validate ports in options
    if "ports" not in new_opts:
        return new_cont
    cont_port = list(new_opts["ports"])
    if new_port not in cont_port:
        print(cont_port)
        raise docker.errors.APIError(
            f"Ports {cont_port} should contain port {new_port}"
        )
    host_ports = new_opts["ports"].values()
    for port in host_ports:
        if isinstance(port, list):
            for p in port:
                check_port(p)
        check_port(port)
    # validate public URL
    port = int(re.search(r"http://localhost:(\d+)", new_url).group(1))
    pub_url = re.search(r"(http://localhost:\d+)", new_url)
    if not pub_url or new_url != pub_url.group(1):
        raise docker.errors.APIError(
            "Public URL should be in form: 'http://localhost:<free host port>'"
        )
    check_port(port)
    return new_cont
