import hashlib
import struct
import socket
from typing import Dict, Optional, Tuple

class RadiusService:
    """RADIUS Authentication Service"""
    
    def __init__(self, server: str, port: int = 1812, secret: str = "secret"):
        self.server = server
        self.port = port
        self.secret = secret.encode('utf-8')
        self.identifier = 1
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user via RADIUS"""
        try:
            # Create RADIUS Access-Request packet
            packet = self._create_access_request(username, password)
            
            # Send packet to RADIUS server
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(packet, (self.server, self.port))
            
            # Receive response
            response, addr = sock.recvfrom(1024)
            sock.close()
            
            # Parse response
            code = response[0]
            return code == 2  # Access-Accept
            
        except Exception as e:
            print(f"RADIUS authentication error: {e}")
            return False
    
    def _create_access_request(self, username: str, password: str) -> bytes:
        """Create RADIUS Access-Request packet"""
        # RADIUS packet structure
        code = 1  # Access-Request
        identifier = self.identifier
        self.identifier = (self.identifier + 1) % 256
        
        # Request Authenticator (16 random bytes)
        authenticator = b'\x00' * 16
        
        # Attributes
        attributes = b''
        
        # User-Name attribute (Type 1)
        username_bytes = username.encode('utf-8')
        attributes += struct.pack('BB', 1, len(username_bytes) + 2) + username_bytes
        
        # User-Password attribute (Type 2) - encrypted
        password_encrypted = self._encrypt_password(password, authenticator)
        attributes += struct.pack('BB', 2, len(password_encrypted) + 2) + password_encrypted
        
        # NAS-IP-Address attribute (Type 4)
        nas_ip = socket.inet_aton('127.0.0.1')
        attributes += struct.pack('BB', 4, 6) + nas_ip
        
        # Calculate length
        length = 20 + len(attributes)
        
        # Create packet
        packet = struct.pack('!BBH', code, identifier, length) + authenticator + attributes
        
        # Calculate and replace Request Authenticator
        authenticator = hashlib.md5(packet + self.secret).digest()
        packet = packet[:4] + authenticator + packet[20:]
        
        return packet
    
    def _encrypt_password(self, password: str, authenticator: bytes) -> bytes:
        """Encrypt password for RADIUS"""
        password_bytes = password.encode('utf-8')
        
        # Pad password to 16-byte boundary
        while len(password_bytes) % 16 != 0:
            password_bytes += b'\x00'
        
        encrypted = b''
        prev = authenticator
        
        for i in range(0, len(password_bytes), 16):
            chunk = password_bytes[i:i+16]
            hash_input = self.secret + prev
            hash_result = hashlib.md5(hash_input).digest()
            
            encrypted_chunk = bytes(a ^ b for a, b in zip(chunk, hash_result))
            encrypted += encrypted_chunk
            prev = encrypted_chunk
        
        return encrypted
    
    def accounting_start(self, username: str, session_id: str, nas_ip: str) -> bool:
        """Send accounting start packet"""
        try:
            packet = self._create_accounting_packet(username, session_id, nas_ip, "start")
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(packet, (self.server, 1813))  # Accounting port
            
            response, addr = sock.recvfrom(1024)
            sock.close()
            
            return response[0] == 5  # Accounting-Response
            
        except Exception as e:
            print(f"RADIUS accounting start error: {e}")
            return False
    
    def accounting_stop(self, username: str, session_id: str, nas_ip: str, 
                       session_time: int, bytes_in: int, bytes_out: int) -> bool:
        """Send accounting stop packet"""
        try:
            packet = self._create_accounting_packet(
                username, session_id, nas_ip, "stop", 
                session_time, bytes_in, bytes_out
            )
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
            sock.sendto(packet, (self.server, 1813))
            
            response, addr = sock.recvfrom(1024)
            sock.close()
            
            return response[0] == 5  # Accounting-Response
            
        except Exception as e:
            print(f"RADIUS accounting stop error: {e}")
            return False
    
    def _create_accounting_packet(self, username: str, session_id: str, nas_ip: str, 
                                status: str, session_time: int = 0, 
                                bytes_in: int = 0, bytes_out: int = 0) -> bytes:
        """Create RADIUS Accounting packet"""
        code = 4  # Accounting-Request
        identifier = self.identifier
        self.identifier = (self.identifier + 1) % 256
        
        authenticator = b'\x00' * 16
        attributes = b''
        
        # User-Name attribute
        username_bytes = username.encode('utf-8')
        attributes += struct.pack('BB', 1, len(username_bytes) + 2) + username_bytes
        
        # Acct-Status-Type attribute
        status_map = {"start": 1, "stop": 2, "update": 3}
        attributes += struct.pack('!BBL', 40, 6, status_map.get(status, 1))
        
        # Acct-Session-Id attribute
        session_bytes = session_id.encode('utf-8')
        attributes += struct.pack('BB', 44, len(session_bytes) + 2) + session_bytes
        
        # NAS-IP-Address attribute
        nas_ip_bytes = socket.inet_aton(nas_ip)
        attributes += struct.pack('BB', 4, 6) + nas_ip_bytes
        
        if status == "stop":
            # Acct-Session-Time attribute
            attributes += struct.pack('!BBL', 46, 6, session_time)
            
            # Acct-Input-Octets attribute
            attributes += struct.pack('!BBL', 42, 6, bytes_in)
            
            # Acct-Output-Octets attribute
            attributes += struct.pack('!BBL', 43, 6, bytes_out)
        
        length = 20 + len(attributes)
        packet = struct.pack('!BBH', code, identifier, length) + authenticator + attributes
        
        # Calculate Request Authenticator for accounting
        authenticator = hashlib.md5(packet + self.secret).digest()
        packet = packet[:4] + authenticator + packet[20:]
        
        return packet