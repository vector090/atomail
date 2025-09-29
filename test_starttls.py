#!/usr/bin/env python3
import imaplib
import ssl
import os

def test_starttls():
    host = "imap.139.com"
    port = 143
    
    print(f"Testing STARTTLS on {host}:{port}")
    print("=" * 40)
    
    try:
        # Connect with plain IMAP first
        print("1. Connecting with plain IMAP...")
        imap = imaplib.IMAP4(host, port)
        print("   Plain IMAP connection successful")
        
        # Check if STARTTLS is supported
        print("2. Checking STARTTLS capability...")
        try:
            status, capabilities = imap.capability()
            if status == 'OK':
                cap_str = b' '.join(capabilities).decode('utf-8')
                print(f"   Server capabilities: {cap_str}")
                if 'STARTTLS' in cap_str.upper():
                    print("   STARTTLS is supported!")
                else:
                    print("   STARTTLS not found in capabilities")
        except Exception as cap_err:
            print(f"   Capability check failed: {cap_err}")
        
        # Try STARTTLS
        print("3. Attempting STARTTLS upgrade...")
        try:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            imap.starttls(ssl_context=context)
            print("   STARTTLS upgrade successful!")
            print("   Connection is now encrypted")
            
            # Test login after STARTTLS
            print("4. Testing authentication...")
            user = os.environ.get('IMAP_USER', '18359734792@139.com')
            password = os.environ.get('IMAP_PASSWORD')
            if password:
                try:
                    imap.login(user, password)
                    print("   Login successful with STARTTLS!")
                except Exception as login_err:
                    print(f"   Login failed: {login_err}")
            else:
                print("   No password provided, skipping login test")
                
        except Exception as tls_err:
            print(f"   STARTTLS failed: {tls_err}")
            print("   Server may not support STARTTLS")
        
        imap.logout()
        
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == '__main__':
    test_starttls()