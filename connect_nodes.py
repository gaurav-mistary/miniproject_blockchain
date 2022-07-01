import json
import os
import requests
import argparse
import subprocess
import socket, os


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", action="store_true", default=False, required=False)
    return parser.parse_args()

def main():
    args = get_args()

    with open("network.json", "r") as f:
            networks = json.load(f)
            print(f"Networks: {networks}")

    if args.ip:
        print(f"Received Fucking IPPP")
        with open("network.json", "w") as f:
            hostname = socket.gethostname()   
            IPAddr = socket.gethostbyname(hostname)   
            print("Your Computer Name is:" + hostname)   
            print("Your Computer IP Address is:" + IPAddr)  
            networks.append(f"{IPAddr}:{os.getenv('FLASK_PORT')}")
            f.write(json.dumps(networks))
    else:
        app_ports = {"App1":"5001", "App2":"5002", "app3":"5003"}
        network_mapping = {n.split(":")[-1] : f"http://{n}" for n in set(networks)}

        for app, port in app_ports.items():
            subsequent_nodes = [v for n, v in network_mapping.items() if n != port]
            print("Subsequent Nodes: ", subsequent_nodes)
            data = {"nodes": subsequent_nodes}

            response = requests.post(f"{network_mapping.get(port)}/connect_node", json=data)
            print(f"{app}::{network_mapping.get(port)} connected to {response.json()}")
            # print(f"APP: {app}: {response.status_code}")
            print("====================================")


if __name__ == "__main__":
    main()
