#!/usr/bin/env python3
"""
Additional vulnerable code examples for SAST testing
This file contains various types of security vulnerabilities
that should be detected by Wiz SAST scanning.
"""

import os
import pickle
import subprocess
import hashlib
import random
import sqlite3
from xml.etree import ElementTree as ET
import yaml
import requests

# HARDCODED SECRETS (for secret scanning)
API_KEY = "sk_test_123456xxxxxqrstuvwxyz"
DATABASE_PASSWORD = "admin123"
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEA4f5wg5l2hKsTeNem..."

class VulnerableApp:
    def __init__(self):
        self.db_connection = None
        
    def sql_injection_vulnerability(self, user_input):
        """SAST VULNERABILITY: SQL Injection"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        
        # Direct string concatenation - vulnerable to SQL injection
        query = f"SELECT * FROM users WHERE name = '{user_input}'"
        cursor.execute(query)
        
        return cursor.fetchall()
    
    def command_injection_vulnerability(self, filename):
        """SAST VULNERABILITY: Command Injection"""
        # Unsanitized user input in system command
        command = f"cat {filename}"
        result = os.system(command)
        return result
    
  
    
    def xml_external_entity_vulnerability(self, xml_data):
        """SAST VULNERABILITY: XML External Entity (XXE)"""
        # Parsing XML without disabling external entities
        root = ET.fromstring(xml_data)
        return ET.tostring(root, encoding='unicode')
    
    def deserialization_vulnerability(self, serialized_data):
        """SAST VULNERABILITY: Insecure Deserialization"""
        # Using pickle to deserialize untrusted data
        return pickle.loads(serialized_data)
    
    def weak_cryptography_md5(self, password):
        """SAST VULNERABILITY: Weak Cryptographic Hash (MD5)"""
        # MD5 is cryptographically broken
        return hashlib.md5(password.encode()).hexdigest()
    
    def weak_cryptography_sha1(self, data):
        """SAST VULNERABILITY: Weak Cryptographic Hash (SHA1)"""
        # SHA1 is also considered weak
        return hashlib.sha1(data.encode()).hexdigest()
    
    def weak_random_generation(self):
        """SAST VULNERABILITY: Weak Random Number Generation"""
        # Using predictable random number generator for security purposes
        return random.random()
    
  
    
    def yaml_deserialization_vulnerability(self, yaml_content):
        """SAST VULNERABILITY: YAML Deserialization"""
        # Using unsafe YAML loading
        return yaml.load(yaml_content, Loader=yaml.Loader)
    
    def hardcoded_password_check(self, password):
        """SAST VULNERABILITY: Hardcoded Password"""
        # Hardcoded password in source code
        if password == "admin123":
            return "Access granted"
        return "Access denied"
    
    def shell_injection_vulnerability(self, user_command):
        """SAST VULNERABILITY: Shell Injection"""
        # Using shell=True with user input
        result = subprocess.run(user_command, shell=True, capture_output=True, text=True)
        return result.stdout
    
  
    
    def xpath_injection_vulnerability(self, username, password):
        """SAST VULNERABILITY: XPath Injection"""
        # Building XPath query without proper escaping
        xpath_query = f"//users/user[username/text()='{username}' and password/text()='{password}']"
        return xpath_query
    
    def eval_vulnerability(self, user_expression):
        """SAST VULNERABILITY: Code Injection via eval()"""
        # Using eval() with user input
        return eval(user_expression)
    
    def exec_vulnerability(self, user_code):
        """SAST VULNERABILITY: Code Injection via exec()"""
        # Using exec() with user input
        exec(user_code)
    
    def open_redirect_vulnerability(self, redirect_url):
        """SAST VULNERABILITY: Open Redirect"""
        # No validation of redirect URL
        return f"<script>window.location.href='{redirect_url}'</script>"
    
    def information_disclosure(self):
        """SAST VULNERABILITY: Information Disclosure"""
        # Exposing sensitive system information
        return {
            "environment_variables": dict(os.environ),
            "current_directory": os.getcwd(),
            "python_path": os.sys.path,
            "database_password": DATABASE_PASSWORD,
            "api_key": API_KEY
        }
    
    def insecure_file_permissions(self, filename, content):
        """SAST VULNERABILITY: Insecure File Permissions"""
        # Creating files with overly permissive permissions
        with open(filename, 'w') as f:
            f.write(content)
        os.chmod(filename, 0o777)  # World readable/writable
    
  
    
    def timing_attack_vulnerability(self, submitted_token, valid_token):
        """SAST VULNERABILITY: Timing Attack"""
        # Byte-by-byte comparison allows timing attacks
        if len(submitted_token) != len(valid_token):
            return False
        
        for i in range(len(submitted_token)):
            if submitted_token[i] != valid_token[i]:
                return False
        return True
    
    def race_condition_vulnerability(self):
        """SAST VULNERABILITY: Race Condition"""
        # Checking and using resource without proper locking
        if os.path.exists("temp_file.txt"):
            # Race condition here - file could be deleted between check and use
            with open("temp_file.txt", "r") as f:
                return f.read()
        return None


# More hardcoded secrets for comprehensive testing
class SecretManager:
    AWS_ACCESS_KEY = "xxxxx"
    AWS_SECRET_KEY = "xx"
    GITHUB_TOKEN = "ghp_1234567890xxxxxopqrstuvwxyz"
    JWT_SECRET = "susssss"
    ENCRYPTION_KEY = "abcdsssss"
    DATABASE_URI = "postgresql://admin:password123@localhost:5432/production"
    REDIS_PASSWORD = "redis_password_123"
    MONGODB_CONNECTION = "mongodb://admin:xxxxxlocalhost:27017/app"
    STRIPE_SECRET = "sk_live_12345xxxxxxxjklmnopqrasdasdguvwxyz"

if __name__ == "__main__":
    # Example usage that would trigger vulnerabilities
    app = VulnerableApp()
    
    # This would be vulnerable to SQL injection
    result = app.sql_injection_vulnerability("'; DROP TABLE users; --")
    
    # This would be vulnerable to command injection
    app.command_injection_vulnerability("../../../etc/passwd")
    
    # This would be vulnerable to path traversal
    app.path_traversal_vulnerability("../../../etc/passwd")
    
    print("Vulnerable application initialized with security flaws for testing")
