import os
import docker
import docker.errors
import time

def is_container_ready(container):
    container.reload()
    return container.status == "running"

def wait_for_stable_status(container, stable_duration=3, interval=1):
    start_time = time.time()
    stable_count = 0
    while time.time() - start_time < stable_duration:
        if is_container_ready(container):
            stable_count +=1
        else:
            stable_count = 0

        if stable_count >= stable_duration / interval:
            return True
        
        time.sleep(interval)
    return False

def start_db_container():
    client = docker.from_env()
    container_name = "test-db"
    scripts_dir = os.path.abspath("./scripts")
    
    try:
        existing_container = client.containers.get(container_name)
        print(f"Container {container_name} exists. Stopping and removing")
        existing_container.stop()
        existing_container.remove()
        print(f"Container {container_name} stopped and removed")
    except docker.errors.NotFound:
        print(f"Container {container_name} does not exist.")

    # Define container config
    container_config = {
        # "version": "3.9",
        "name": container_name,
        "image": "postgres:alpine",
        "detach": True,
        "ports": {"5432":"5431"},
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "password",
        },
        "volumes": [f"{scripts_dir}:/docker-entrypoint-initdb.d"],
        "network_mode": "recipe_api_dev-network",
    }

    container = client.containers.run(**container_config)

    while not is_container_ready(container):
        time.sleep(1)

    if not wait_for_stable_status(container):
        raise RuntimeError("Container didn't stabalize within the specified time")
    
    return container