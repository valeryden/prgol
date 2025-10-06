
# Code snippets for vulnerabilities in vulnerable_code.py

# Path Traversal vulnerability at line 46

def path_traversal_vulnerability(self, file_path):
    """SAST VULNERABILITY: Path Traversal"""
    # No validation of file path - allows directory traversal
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)


# SSRF vulnerability at line 81

def ssrf_vulnerability(self, url):
    """SAST VULNERABILITY: Server-Side Request Forgery"""
    # No validation of URL - allows SSRF attacks
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return str(e)


# LDAP Injection vulnerability at line 108

def ldap_injection_vulnerability(self, username):
    """SAST VULNERABILITY: LDAP Injection"""
    # Building LDAP query without proper escaping
    ldap_query = f"(&(objectClass=user)(sAMAccountName={username}))"
    return ldap_query


# XPath Injection vulnerability at line 113

def xpath_injection_vulnerability(self, username, password):
    """SAST VULNERABILITY: XPath Injection"""
    # Building XPath query without proper escaping
    xpath_query = f"//users/user[username/text()='{username}' and password/text()='{password}']"
    return xpath_query


# Buffer Overflow vulnerability at line 153

def buffer_overflow_simulation(self, data):
    """SAST VULNERABILITY: Buffer Overflow (Simulation)"""
    # Simulated buffer overflow - reading more data than allocated
    buffer_size = 256
    if len(data) > buffer_size:
        # In C/C++, this would cause a buffer overflow
        # In Python, it just processes the data but represents the vulnerability
        return data[:buffer_size] + " [BUFFER_OVERFLOW_DETECTED]"
    return data


# Timing Attack vulnerability at line 165

def timing_attack_vulnerability(self, submitted_token, valid_token):
    """SAST VULNERABILITY: Timing Attack"""
    # Byte-by-byte comparison allows timing attacks
    if len(submitted_token) != len(valid_token):
        return False
    
    for i in range(len(submitted_token)):
        if submitted_token[i] != valid_token[i]:
            return False
    return True


# Race Condition vulnerability at line 176

def race_condition_vulnerability(self):
    """SAST VULNERABILITY: Race Condition"""
    # Checking and using resource without proper locking
    if os.path.exists("temp_file.txt"):
        # Race condition here - file could be deleted between check and use
        with open("temp_file.txt", "r") as f:
            return f.read()
    return None


# Format String vulnerability

def format_string_vulnerability(user_input):
    """SAST VULNERABILITY: Format String"""
    # Using user input directly in format string
    return f"User provided: {user_input}" % locals()


# Integer Overflow vulnerability

def integer_overflow_simulation(number):
    """SAST VULNERABILITY: Integer Overflow (Simulation)"""
    # Simulating integer overflow conditions
    max_int = 2147483647  # 32-bit signed integer max
    if number > max_int:
        return "Integer overflow detected"
    return number * 2


# Null Pointer Dereference vulnerability

def null_pointer_dereference_simulation(obj):
    """SAST VULNERABILITY: Null Pointer Dereference (Simulation)"""
    # Accessing object without null check
    return obj.some_attribute  # Will cause AttributeError if obj is None


# Use After Free vulnerability

def use_after_free_simulation():
    """SAST VULNERABILITY: Use After Free (Simulation)"""
    # Simulating use-after-free vulnerability
    data = ["sensitive", "information"]
    del data  # "Free" the memory
    # Attempting to use freed memory (in Python this will cause NameError)
    return data[0]

