"""Cyber security and ethical hacking utilities for Sara."""

import re
import subprocess
import sys
from typing import List, Optional

import requests


class CyberSecurityTools:
    """Basic cyber security tools and knowledge base."""

    def __init__(self):
        self.knowledge_base = {
            "password_strength": "A strong password should be at least 12 characters, include uppercase, lowercase, numbers, and symbols.",
            "phishing": "Phishing is a cyber attack where attackers trick users into revealing sensitive information via fake emails or websites.",
            "encryption": "Encryption converts data into a coded format to prevent unauthorized access.",
            "firewall": "A firewall monitors and controls incoming and outgoing network traffic based on security rules.",
            "vpn": "A VPN creates a secure connection over a less secure network, like the internet.",
            "two_factor": "Two-factor authentication adds an extra layer of security by requiring two forms of verification.",
            "sql_injection": "SQL injection is a code injection technique that exploits vulnerabilities in an application's software.",
            "xss": "Cross-Site Scripting (XSS) allows attackers to inject malicious scripts into web pages viewed by other users.",
            "ddos": "Distributed Denial of Service (DDoS) overwhelms a server with traffic to make it unavailable.",
            "malware": "Malware is malicious software designed to harm or exploit devices and networks.",
        }

    def check_password_strength(self, password: str) -> str:
        """Check password strength and provide feedback."""
        score = 0
        feedback = []

        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long.")

        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Include at least one uppercase letter.")

        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Include at least one lowercase letter.")

        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Include at least one number.")

        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("Include at least one special character.")

        strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]
        strength = strength_levels[min(score, 4)]

        if feedback:
            return f"Password strength: {strength}\nSuggestions: {' '.join(feedback)}"
        return f"Password strength: {strength}"

    def scan_ports(self, target: str, ports: List[int] = None) -> str:
        """Basic port scanning using socket (ethical use only)."""
        if ports is None:
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995]

        import socket
        open_ports = []

        for port in ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass

        if open_ports:
            return f"Open ports on {target}: {', '.join(map(str, open_ports))}"
        return f"No common open ports found on {target}"

    def get_security_info(self, topic: str) -> str:
        """Get information about a security topic."""
        topic_lower = topic.lower().replace(" ", "_")
        if topic_lower in self.knowledge_base:
            return self.knowledge_base[topic_lower]
        return f"I don't have specific information on '{topic}'. For cyber security topics, I can help with password strength, common attacks, and basic tools."

    def run_nmap_scan(self, target: str) -> str:
        """Run a basic nmap scan if available (ethical use only)."""
        try:
            result = subprocess.run(
                ["nmap", "-sV", "--version-light", target],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                return result.stdout
            else:
                return f"Nmap scan failed: {result.stderr}"
        except FileNotFoundError:
            return "Nmap is not installed. Please install nmap for advanced scanning."
        except subprocess.TimeoutExpired:
            return "Scan timed out."
        except Exception as e:
            return f"Error running nmap: {str(e)}"

    def check_website_security(self, url: str) -> str:
        """Basic website security check."""
        try:
            response = requests.get(url, timeout=10, verify=True)
            security_info = []

            if response.url.startswith("https://"):
                security_info.append("✓ Uses HTTPS encryption")
            else:
                security_info.append("⚠ Uses HTTP (not encrypted)")

            headers = response.headers
            if "Strict-Transport-Security" in headers:
                security_info.append("✓ Has HSTS header")
            if "X-Frame-Options" in headers:
                security_info.append("✓ Has X-Frame-Options header")
            if "X-Content-Type-Options" in headers:
                security_info.append("✓ Has X-Content-Type-Options header")
            if "Content-Security-Policy" in headers:
                security_info.append("✓ Has Content Security Policy")

            return f"Security check for {url}:\n" + "\n".join(security_info)
        except requests.exceptions.SSLError:
            return f"⚠ SSL certificate error for {url}"
        except Exception as e:
            return f"Error checking website: {str(e)}"