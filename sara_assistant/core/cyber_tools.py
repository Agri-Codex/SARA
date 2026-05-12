class CyberToolRegistry:
    """Defensive cybersecurity tool registry.

    This registry displays common security tools for learning, lab use, and authorized testing.
    It does not run intrusive commands or automate attacks.
    """

    TOOLS = [
        {"name": "Nmap", "category": "Network Mapping", "status": "Display Only", "safe_use": "Authorized network inventory and exposure review"},
        {"name": "Burp Suite", "category": "Web Security", "status": "Display Only", "safe_use": "Authorized web app testing and proxy inspection"},
        {"name": "Hydra", "category": "Credential Audit", "status": "Display Only", "safe_use": "Only in owned lab systems for password policy education"},
        {"name": "Wireshark", "category": "Packet Analysis", "status": "Display Only", "safe_use": "Traffic analysis on owned networks"},
        {"name": "Nikto", "category": "Web Scanner", "status": "Display Only", "safe_use": "Authorized web server configuration review"},
        {"name": "Metasploit", "category": "Security Framework", "status": "Display Only", "safe_use": "Controlled lab validation and education"},
        {"name": "Gobuster", "category": "Content Discovery", "status": "Display Only", "safe_use": "Authorized directory discovery in labs"},
        {"name": "SQLMap", "category": "Database Testing", "status": "Display Only", "safe_use": "Training labs and explicitly authorized tests only"},
    ]

    @classmethod
    def list_tools_text(cls) -> str:
        lines = ["Defensive Cybersecurity Toolkit:"]
        for tool in cls.TOOLS:
            lines.append(f"• {tool['name']} — {tool['category']} — {tool['status']}")
        return "\n".join(lines)

    @classmethod
    def safety_notice(cls) -> str:
        return "Cyber tools are shown for ethical, defensive, and authorized lab use only."
