import socket
import hashlib
import binascii
from typing import Dict, List, Optional, Any

class MikroTikAPI:
    """MikroTik RouterOS API client"""
    
    def __init__(self, host: str, port: int = 8728, timeout: int = 10):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.socket = None
        self.current_tag = 0
        
    def connect(self, username: str, password: str) -> bool:
        """Connect to MikroTik device"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(self.timeout)
            self.socket.connect((self.host, self.port))
            
            # Login process
            login_result = self._login(username, password)
            return login_result
            
        except Exception as e:
            print(f"Connection error: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MikroTik device"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
    
    def _login(self, username: str, password: str) -> bool:
        """Perform login authentication"""
        try:
            # Get challenge
            self.socket.send(self._encode_sentence(["/login"]))
            response = self._read_sentence()
            
            if len(response) < 2 or response[0] != "!done":
                return False
                
            challenge = None
            for item in response[1:]:
                if item.startswith("=ret="):
                    challenge = binascii.unhexlify(item[5:])
                    break
            
            if not challenge:
                return False
            
            # Send credentials
            md5 = hashlib.md5()
            md5.update(b"\x00")
            md5.update(password.encode('utf-8'))
            md5.update(challenge)
            
            self.socket.send(self._encode_sentence([
                "/login",
                f"=name={username}",
                f"=response=00{md5.hexdigest()}"
            ]))
            
            response = self._read_sentence()
            return response[0] == "!done"
            
        except Exception as e:
            print(f"Login error: {e}")
            return False
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get system statistics"""
        try:
            self.socket.send(self._encode_sentence(["/system/resource/print"]))
            response = self._read_sentence()
            
            stats = {}
            for item in response:
                if item.startswith("="):
                    key, value = item[1:].split("=", 1)
                    stats[key] = value
            
            return {
                "cpu_load": float(stats.get("cpu-load", "0")),
                "memory_usage": float(stats.get("free-memory", "0")),
                "uptime": stats.get("uptime", "0"),
                "version": stats.get("version", "unknown"),
                "board_name": stats.get("board-name", "unknown"),
                "architecture": stats.get("architecture-name", "unknown")
            }
        except:
            return {}
    
    def get_interfaces(self) -> List[Dict[str, Any]]:
        """Get interface statistics"""
        try:
            self.socket.send(self._encode_sentence(["/interface/print", "=stats"]))
            response = self._read_sentence()
            
            interfaces = []
            current_interface = {}
            
            for item in response:
                if item.startswith("="):
                    key, value = item[1:].split("=", 1)
                    current_interface[key] = value
                elif item == "!re":
                    if current_interface:
                        interfaces.append({
                            "name": current_interface.get("name", ""),
                            "rx_bytes": int(current_interface.get("rx-byte", "0")),
                            "tx_bytes": int(current_interface.get("tx-byte", "0")),
                            "rx_packets": int(current_interface.get("rx-packet", "0")),
                            "tx_packets": int(current_interface.get("tx-packet", "0")),
                            "status": current_interface.get("running", "false") == "true" and "running" or "stopped"
                        })
                    current_interface = {}
            
            return interfaces
        except:
            return []
    
    def get_pppoe_sessions(self) -> List[Dict[str, Any]]:
        """Get active PPPoE sessions"""
        try:
            self.socket.send(self._encode_sentence(["/ppp/active/print"]))
            response = self._read_sentence()
            
            sessions = []
            current_session = {}
            
            for item in response:
                if item.startswith("="):
                    key, value = item[1:].split("=", 1)
                    current_session[key] = value
                elif item == "!re":
                    if current_session:
                        sessions.append({
                            "name": current_session.get("name", ""),
                            "caller_id": current_session.get("caller-id", ""),
                            "address": current_session.get("address", ""),
                            "uptime": current_session.get("uptime", ""),
                            "bytes_in": int(current_session.get("bytes-in", "0")),
                            "bytes_out": int(current_session.get("bytes-out", "0")),
                            "service": current_session.get("service", "")
                        })
                    current_session = {}
            
            return sessions
        except:
            return []
    
    def _encode_sentence(self, words: List[str]) -> bytes:
        """Encode API sentence"""
        sentence = b""
        for word in words:
            sentence += self._encode_word(word.encode('utf-8'))
        sentence += b"\x00"
        return sentence
    
    def _encode_word(self, word: bytes) -> bytes:
        """Encode API word"""
        length = len(word)
        if length < 0x80:
            return bytes([length]) + word
        elif length < 0x4000:
            return bytes([0x80 | (length >> 8), length & 0xFF]) + word
        elif length < 0x200000:
            return bytes([0xC0 | (length >> 16), (length >> 8) & 0xFF, length & 0xFF]) + word
        elif length < 0x10000000:
            return bytes([0xE0 | (length >> 24), (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF]) + word
        else:
            return bytes([0xF0, (length >> 24) & 0xFF, (length >> 16) & 0xFF, (length >> 8) & 0xFF, length & 0xFF]) + word
    
    def _read_sentence(self) -> List[str]:
        """Read API sentence"""
        sentence = []
        while True:
            word = self._read_word()
            if not word:
                break
            sentence.append(word.decode('utf-8'))
        return sentence
    
    def _read_word(self) -> bytes:
        """Read API word"""
        length_bytes = self.socket.recv(1)
        if not length_bytes:
            return b""
        
        length = length_bytes[0]
        if length == 0:
            return b""
        
        if length < 0x80:
            word_length = length
        elif length < 0xC0:
            length_bytes += self.socket.recv(1)
            word_length = ((length & 0x7F) << 8) + length_bytes[1]
        elif length < 0xE0:
            length_bytes += self.socket.recv(2)
            word_length = ((length & 0x1F) << 16) + (length_bytes[1] << 8) + length_bytes[2]
        elif length < 0xF0:
            length_bytes += self.socket.recv(3)
            word_length = ((length & 0x0F) << 24) + (length_bytes[1] << 16) + (length_bytes[2] << 8) + length_bytes[3]
        else:
            length_bytes += self.socket.recv(4)
            word_length = (length_bytes[1] << 24) + (length_bytes[2] << 16) + (length_bytes[3] << 8) + length_bytes[4]
        
        return self.socket.recv(word_length)