import subprocess

class manage_firewallclass:
    def __init__(self):
        pass

    def add_firewall_rule(self, rule_name, app_path):
        command = [
            "netsh", "advfirewall", "firewall", "add", "rule",
            f"name={rule_name}",
            "dir=out",
            "action=block",
            f"program={app_path}",
            "enable=yes"
        ]
        
        try:
            subprocess.run(command, check=True)
            return f"Successfully added rule '{rule_name}'."
            
        except subprocess.CalledProcessError as e:
            return f"Error: {e}"



    def remove_firewall_rule(self, rule_name):
            command = [
                "netsh", "advfirewall", "firewall", "delete", "rule",
                f"name={rule_name}"
            ]
            try:
                subprocess.run(command, check=True)
                return f"Successfully removed rule '{rule_name}'."
            except subprocess.CalledProcessError as e:
                return f"Error: {e}"