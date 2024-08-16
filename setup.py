import os
import subprocess
import argparse

def generate_ssh_key(key_name):
    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)

    private_key_path = os.path.join(ssh_dir, key_name)
    public_key_path = f"{private_key_path}.pub"

    if os.path.exists(private_key_path) or os.path.exists(public_key_path):
        print(f"SSH key {key_name} already exists. Skipping key generation.")
    else:
        print(f"Generating new SSH key: {key_name}")
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", private_key_path, "-N", ""]
        )

    return private_key_path, public_key_path

def run_ansible_playbook(playbook_path, vars_file, inventory_file='localhost,'):
    print(f"Running Ansible playbook: {playbook_path}")
    try:
        subprocess.run(
            ["ansible-playbook", "-i", inventory_file, playbook_path, "-e", f"@{vars_file}"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the playbook: {e}")
        exit(1)

def main():
    parser = argparse.ArgumentParser(description="Generate SSH key and run Ansible playbook.")
    parser.add_argument("--key-name", required=True, help="The name of the SSH key to generate.")
    parser.add_argument("--playbook", required=True, help="The path to the Ansible playbook.")
    parser.add_argument("--vars-file", required=True, help="The path to the Ansible vars file.")

    args = parser.parse_args()

    private_key, public_key = generate_ssh_key(args.key_name)

    # Assuming the public key is required by the playbook and needs to be present in vars.yml
    # If you need to update the vars.yml file or do any other modifications, add that logic here

    run_ansible_playbook(args.playbook, args.vars_file)

if __name__ == "__main__":
    main()
