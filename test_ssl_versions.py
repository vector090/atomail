#!/usr/bin/env python3
import ssl
import socket

def test_ssl_versions():
    host = "imap.139.com"
    port = 993
    
    print(f"Testing different SSL/TLS configurations for {host}:{port}")
    print("=" * 60)
    
    # Test different SSL/TLS versions
    protocols = [
        ('SSLv23', ssl.PROTOCOL_SSLv23),
        ('TLS', ssl.PROTOCOL_TLS),
        ('TLSv1', ssl.PROTOCOL_TLSv1),
        ('TLSv1.1', ssl.PROTOCOL_TLSv1_1),
        ('TLSv1.2', ssl.PROTOCOL_TLSv1_2),
    ]
    
    for proto_name, proto in protocols:
        print(f"\nTesting {proto_name}...")
        try:
            context = ssl.SSLContext(proto)
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Try with different cipher settings
            try:
                context.set_ciphers('DEFAULT')
                print(f"  {proto_name}: Default ciphers")
            except:
                print(f"  {proto_name}: Could not set default ciphers")
            
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    print(f"  {proto_name}: SUCCESS - SSL established")
                    print(f"    Version: {ssock.version()}")
                    print(f"    Cipher: {ssock.cipher()[0]}")
                    
                    # Try to send IMAP command
                    try:
                        ssock.send(b"* ID NIL\r\n")
                        response = ssock.recv(1024)
                        print(f"    IMAP Response: {response.decode('utf-8', errors='ignore')}")
                    except Exception as e:
                        print(f"    IMAP test failed: {e}")
                        
        except Exception as e:
            print(f"  {proto_name}: FAILED - {e}")

if __name__ == '__main__':
    test_ssl_versions()