import os
import subprocess
import argparse
import random
import sys
import datetime
import yaml

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def load_word_list(filename):
    """Load words from a text file, one word per line"""
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, filename)
        with open(file_path, 'r') as f:
            words = [line.strip() for line in f if line.strip()]
        return words
    except FileNotFoundError:
        print(f"Warning: {filename} not found. Using fallback word lists.")
        if 'verbs' in filename:
            return ["running", "flying", "blazing", "soaring", "charging", "prowling"]
        else:
            return ["wolf", "eagle", "tiger", "falcon", "bear", "lion"]

def generate_random_deployment_name():
    """Generate a random deployment name using verb + animal (no hyphen)"""
    verbs = load_word_list('verbs.txt')
    animals = load_word_list('animals.txt')
    
    verb = random.choice(verbs)
    animal = random.choice(animals)
    return f"{verb}{animal}"

def interactive_setup():
    """Interactive setup when no arguments are provided"""
    print("🚀 FourEyes Interactive Setup")
    print("=" * 40)
    
    # Get deployment name
    default_name = generate_random_deployment_name()
    key_name = input(f"Enter deployment name (or press Enter for '{default_name}'): ").strip()
    if not key_name:
        key_name = default_name
    
    # Get playbook path
    available_playbooks = []
    
    # Check for deployment files in deployments/ directory (prioritize basic-chat)
    deployments_dir = 'deployments'
    if os.path.exists(deployments_dir):
        deployment_files = []
        for file in os.listdir(deployments_dir):
            if file.endswith('.yaml') or file.endswith('.yml'):
                deployment_files.append(file)
        
        # Sort to put basic-chat first
        deployment_files.sort(key=lambda x: (x != 'basic-chat.yaml', x))
        
        for file in deployment_files:
            # Display without the deployments/ prefix for readability
            available_playbooks.append((os.path.join(deployments_dir, file), file))
    
    # Check for playbooks in root directory
    for file in os.listdir('.'):
        if file.endswith('.yaml') or file.endswith('.yml'):
            if 'server' in file.lower() or 'playbook' in file.lower():
                available_playbooks.append((file, file))
    
    if available_playbooks:
        print(f"\nAvailable playbooks:")
        for i, (full_path, display_name) in enumerate(available_playbooks, 1):
            default_marker = " (default)" if i == 1 else ""
            print(f"  {i}. {display_name}{default_marker}")
        
        while True:
            try:
                choice = input(f"\nSelect playbook (1-{len(available_playbooks)}, Enter for default): ").strip()
                if not choice:  # Default to first option
                    playbook = available_playbooks[0][0]
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(available_playbooks):
                    playbook = available_playbooks[int(choice) - 1][0]
                    break
                elif os.path.exists(choice):
                    playbook = choice
                    break
                else:
                    print("Invalid choice or file doesn't exist. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    else:
        playbook = input("Enter playbook path: ").strip()
        while not os.path.exists(playbook):
            print(f"File '{playbook}' not found.")
            playbook = input("Enter playbook path: ").strip()
    
    # Get vars file
    available_vars = []
    for file in os.listdir('.'):
        if file.startswith('vars') and (file.endswith('.yaml') or file.endswith('.yml')):
            available_vars.append(file)
    
    # Sort to put vars.yaml first if it exists
    if 'vars.yaml' in available_vars:
        available_vars.remove('vars.yaml')
        available_vars.insert(0, 'vars.yaml')
    
    if available_vars:
        print(f"\nAvailable vars files:")
        for i, vars_file in enumerate(available_vars, 1):
            default_marker = " (default)" if i == 1 else ""
            print(f"  {i}. {vars_file}{default_marker}")
        
        while True:
            try:
                choice = input(f"\nSelect vars file (1-{len(available_vars)}, Enter for default) or enter custom path: ").strip()
                if not choice:  # Default to first option (vars.yaml if available)
                    vars_file = available_vars[0]
                    break
                elif choice.isdigit() and 1 <= int(choice) <= len(available_vars):
                    vars_file = available_vars[int(choice) - 1]
                    break
                elif os.path.exists(choice):
                    vars_file = choice
                    break
                else:
                    print("Invalid choice or file doesn't exist. Please try again.")
            except (ValueError, IndexError):
                print("Invalid input. Please try again.")
    else:
        vars_file = input("Enter vars file path: ").strip()
        while not os.path.exists(vars_file):
            print(f"File '{vars_file}' not found.")
            vars_file = input("Enter vars file path: ").strip()
    
    # Confirmation
    print(f"\n📋 Configuration Summary:")
    print(f"  Deployment name: {key_name}")
    print(f"  Playbook: {playbook}")
    print(f"  Vars file: {vars_file}")
    
    confirm = input(f"\nProceed with deployment? (Y/n): ").strip().lower()
    if confirm in ['n', 'no']:
        print("Deployment cancelled.")
        sys.exit(0)
    
    return key_name, playbook, vars_file

def generate_ssh_key(key_name):
    ssh_dir = os.path.expanduser("~/.ssh")
    if not os.path.exists(ssh_dir):
        os.makedirs(ssh_dir)

    private_key_path = os.path.join(ssh_dir, key_name)
    public_key_path = f"{private_key_path}.pub"

    if os.path.exists(private_key_path) or os.path.exists(public_key_path):
        print(f"🔑 SSH key {key_name} already exists. Skipping key generation.")
    else:
        print(f"🔑 Generating new SSH key: {key_name}")
        subprocess.run(
            ["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", private_key_path, "-N", ""]
        )
        print(f"✅ SSH key generated: {private_key_path}")

    return private_key_path, public_key_path

def run_ansible_playbook(playbook_path, vars_file, deployment_name, inventory_file='localhost,'):
    print(f"🚀 Running Ansible playbook: {playbook_path}")
    print(f"📋 Using vars file: {vars_file}")
    print(f"🏷️  Deployment name: {deployment_name}")
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"{log_dir}/deployment_{deployment_name}_{timestamp}.log"
    
    print(f"📝 Logging to: {log_file}")
    print("=" * 80)
    
    try:
        # Run ansible with verbose output and real-time logging
        with open(log_file, 'w') as log:
            # Start the ansible process with moderate verbosity
            process = subprocess.Popen(
                ["ansible-playbook", "-v", "-i", inventory_file, playbook_path, "-e", f"@{vars_file}", "-e", f"deployment_name={deployment_name}"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,  # Line buffered
                universal_newlines=True
            )
            
            # Read output line by line and display/log simultaneously
            output_lines = []
            final_status_found = False
            capture_final_output = False
            final_output_lines = []
            
            for line in process.stdout:
                # Write to log file
                log.write(line)
                log.flush()  # Ensure immediate write
                output_lines.append(line)
                
                # Look for the final status information
                if "DEPLOYMENT COMPLETED SUCCESSFULLY" in line:
                    final_status_found = True
                    capture_final_output = True
                
                # Capture lines that contain deployment info
                if any(keyword in line for keyword in ["Tailscale IP:", "Login Credentials:", "Username:", "Password:", "Matrix Chat:", "Dashboard:", "CA certificate:"]):
                    final_output_lines.append(line)
                
                # Display selected output on console (not all the verbose SSH stuff)
                if any(keyword in line for keyword in [
                    "PLAY [", "TASK [", "RECAP", "changed:", "failed:", "ok:", 
                    "Tailscale IP:", "Matrix Chat:", "Dashboard:", "Username:", "Password:",
                    "DEPLOYMENT COMPLETED", "SERVER IS READY", "█"
                ]) or "ERROR" in line or "FAILED" in line:
                    print(line, end='')
                elif not line.startswith('debug') and 'SSH:' not in line and 'OpenSSH_' not in line:
                    # Show non-debug output
                    print(line, end='')
            
            # Wait for process to complete
            process.wait()
            
            # Check return code
            if process.returncode != 0:
                raise subprocess.CalledProcessError(process.returncode, "ansible-playbook")
        
        print("=" * 80)
        print("🎉 Deployment completed successfully!")
        print(f"📝 Full log saved to: {log_file}")
        print("=" * 80)
        
        # Extract and display key deployment information
        if final_output_lines:
            print("\n" + "🌟" * 25 + " DEPLOYMENT SUMMARY " + "🌟" * 25)
            for line in final_output_lines:
                if line.strip():
                    print(line.rstrip())
            print("🌟" * 71)
        
        # Display the completion information prominently
        print("\n" + "�" * 25 + " QUICK ACCESS INFO " + "�" * 25)
        print(f"🏷️  Deployment Name: {deployment_name}")
        print(f"📋 Log File: {log_file}")
        print("🔍 Key information extracted above from deployment output")
        print("📁 Helper scripts deployed to: /root/matrix-helpers/")
        print("💡 If Matrix UI hangs, SSH to server and run: sudo fix_matrix_config.sh")
        print("�" * 71 + "\n")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ An error occurred while running the playbook: {e}")
        print(f"📝 Check the log file for details: {log_file}")
        exit(1)

def diagnose_deployment(vars_file):
        """Diagnose common deployment issues"""
        print(f"\n{Colors.HEADER}═══ FourEyes Deployment Diagnostics ═══{Colors.ENDC}")
        
        if not os.path.exists(vars_file):
            print(f"{Colors.FAIL}No configuration file found at {vars_file}{Colors.ENDC}")
            return
            
        with open(vars_file, 'r') as f:
            config = yaml.safe_load(f)
            
        server_name = config.get('matrix_server_name')
        if not server_name:
            print(f"{Colors.FAIL}No matrix_server_name found in configuration{Colors.ENDC}")
            return
            
        print(f"{Colors.OKBLUE}Checking deployment for: {server_name}{Colors.ENDC}")
        
        # Check dashboard at port 8443
        print(f"\n{Colors.OKCYAN}Testing Dashboard (Port 8443):{Colors.ENDC}")
        dashboard_cmd = f"curl -k -I https://{server_name}:8443 2>/dev/null | head -1"
        print(f"Running: {dashboard_cmd}")
        
        # Check Matrix server
        print(f"\n{Colors.OKCYAN}Testing Matrix Server:{Colors.ENDC}")
        matrix_cmd = f"curl -k https://{server_name}/_matrix/static/ 2>/dev/null | head -5"
        print(f"Running: {matrix_cmd}")
        
        # Provide fix suggestions
        print(f"\n{Colors.HEADER}Suggested Fixes:{Colors.ENDC}")
        print(f"1. Check nginx configuration: sudo nginx -t")
        print(f"2. Restart nginx: sudo systemctl restart nginx")
        print(f"3. Check if sites are enabled: ls -la /etc/nginx/sites-enabled/")
        print(f"4. Check nginx logs: sudo tail -f /var/log/nginx/error.log")
        print(f"5. Verify SSL certificates: sudo openssl x509 -in /etc/ssl/certs/nginx-selfsigned.crt -text -noout")
        
def fix_dashboard_issue(vars_file, base_dir):
        """Fix common dashboard configuration issues"""
        print(f"\n{Colors.HEADER}═══ FourEyes Dashboard Fix ═══{Colors.ENDC}")
        
        if not os.path.exists(vars_file):
            print(f"{Colors.FAIL}No configuration file found. Run setup first.{Colors.ENDC}")
            return
            
        print(f"{Colors.OKBLUE}Generating dashboard fix playbook...{Colors.ENDC}")
        
        # Create a small fix playbook
        fix_playbook_content = """---
- name: Fix FourEyes Dashboard Issues
  hosts: "{{ target_host | default('localhost') }}"
  become: yes
  vars_files:
    - vars.yaml
  
  tasks:
    - name: Check nginx configuration
      command: nginx -t
      register: nginx_test
      failed_when: false
      
    - name: Display nginx test results
      debug:
        var: nginx_test
        
    - name: Ensure foureyes-vpn site is enabled
      file:
        src: /etc/nginx/sites-available/foureyes-vpn
        dest: /etc/nginx/sites-enabled/foureyes-vpn
        state: link
      notify: restart nginx
      
    - name: Remove conflicting default site
      file:
        path: /etc/nginx/sites-enabled/default
        state: absent
      notify: restart nginx
      
    - name: Check if SSL certificates exist
      stat:
        path: "{{ item }}"
      register: ssl_files
      with_items:
        - /etc/ssl/certs/nginx-selfsigned.crt
        - /etc/ssl/private/nginx-selfsigned.key
        
    - name: Display SSL certificate status
      debug:
        msg: "SSL file {{ item.item }} exists: {{ item.stat.exists }}"
      with_items: "{{ ssl_files.results }}"
      
    - name: Regenerate self-signed certificates if missing
      block:
        - name: Generate new SSL certificate
          command: >
            openssl req -x509 -nodes -days 365 -newkey rsa:2048
            -keyout /etc/ssl/private/nginx-selfsigned.key
            -out /etc/ssl/certs/nginx-selfsigned.crt
            -subj "/C=US/ST=State/L=City/O=FourEyes/CN={{ matrix_server_name }}"
          notify: restart nginx
      when: not ssl_files.results[0].stat.exists or not ssl_files.results[1].stat.exists
      
    - name: Test dashboard accessibility
      uri:
        url: "https://{{ matrix_server_name }}:8443"
        method: GET
        validate_certs: no
        status_code: [200, 302]
      register: dashboard_test
      failed_when: false
      
    - name: Display dashboard test results
      debug:
        msg: "Dashboard status: {{ dashboard_test.status | default('Failed to connect') }}"
        
    - name: Check nginx processes
      command: ps aux | grep nginx
      register: nginx_processes
      
    - name: Display nginx processes
      debug:
        var: nginx_processes.stdout_lines
        
  handlers:
    - name: restart nginx
      service:
        name: nginx
        state: restarted
"""
        
        fix_playbook_path = os.path.join(base_dir, "fix-dashboard.yaml")
        with open(fix_playbook_path, 'w') as f:
            f.write(fix_playbook_content)
            
        print(f"{Colors.OKGREEN}Fix playbook created: {fix_playbook_path}{Colors.ENDC}")
        
        if input("Run the dashboard fix now? (y/N): ").strip().lower() in ['y', 'yes']:
            run_ansible_playbook(fix_playbook_path, vars_file, os.path.basename(fix_playbook_path).replace('.yaml', ''))

def main():
    # Check if any arguments were provided
    if len(sys.argv) == 1:
        # No arguments provided, run interactive setup
        key_name, playbook_path, vars_file = interactive_setup()
    else:
        # Arguments provided, use argparse
        parser = argparse.ArgumentParser(description="Generate SSH key and run Ansible playbook.")
        parser.add_argument("--key-name", help="The name of the SSH key to generate. If not provided, a random name will be generated.")
        parser.add_argument("--playbook", required=True, help="The path to the Ansible playbook.")
        parser.add_argument("--vars-file", required=True, help="The path to the Ansible vars file.")

        args = parser.parse_args()
        
        # Generate random key name if not provided
        key_name = args.key_name if args.key_name else generate_random_deployment_name()
        playbook_path = args.playbook
        vars_file = args.vars_file
        
        print(f"🎯 Using deployment name: {key_name}")

    private_key, public_key = generate_ssh_key(key_name)

    # Assuming the public key is required by the playbook and needs to be present in vars.yml
    # If you need to update the vars.yml file or do any other modifications, add that logic here

    run_ansible_playbook(playbook_path, vars_file, key_name)

    # Diagnostic and fix capabilities
    diagnose_deployment(vars_file)
    fix_dashboard_issue(vars_file, os.path.dirname(playbook_path))

if __name__ == "__main__":
    main()
