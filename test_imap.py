#!/usr/bin/env python3
import imaplib
import getpass
import logging
import os

logging.basicConfig(level=logging.INFO)

def test_imap_connection():
    # Get configuration from environment variables or prompt
    host = os.environ.get('IMAP_HOST', 'imap.126.com')
    port = int(os.environ.get('IMAP_PORT', '993'))
    user = os.environ.get('IMAP_USER')
    password = os.environ.get('IMAP_PASSWORD')
    
    if not user:
        user = input("Email address: ")
    if not password:
        password = getpass.getpass("Password: ")
    
    print(f"Testing IMAP connection to {host}:{port}")
    
    try:
        logging.info(f'Connecting to {host}:{port}')
        
        # Choose connection type based on port
        if port == 993 or port == 585:
            # SSL/TLS ports - use SSLv23 with TLS 1.2 for imap.139.com compatibility
            logging.info('Using SSL/TLS connection')
            try:
                import ssl
                
                # This server (imap.139.com) requires SSLv23 protocol with TLS 1.2
                logging.info('Creating SSL context with SSLv23 protocol...')
                context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                # Set compatible cipher suite
                try:
                    context.set_ciphers('AES256-GCM-SHA384:AES128-GCM-SHA256:HIGH:!aNULL:!eNULL')
                except:
                    pass  # Use default ciphers if specific ones fail
                
                imap = imaplib.IMAP4_SSL(host, port, ssl_context=context)
                logging.info('SSL connection successful!')
                
            except Exception as ssl_err:
                logging.error(f'SSL connection failed: {ssl_err}')
                raise
                    
        elif port == 143:
            # Plain text port - start TLS if available
            imap = imaplib.IMAP4(host, port)
            try:
                # Try to upgrade to TLS
                imap.starttls()
                logging.info('Connection upgraded to TLS')
            except:
                logging.info('Using plain text connection (no TLS)')
        else:
            # Default to plain connection for other ports
            imap = imaplib.IMAP4(host, port)
            logging.info('Using plain IMAP connection')
        
        # Set socket timeout for long operations
        import socket
        imap.socket().settimeout(30)
        
        logging.info(f'Logging in as {user}...')
        imap.login(user, password)
        logging.info('Login successful!')
        
        logging.info('Listing mailboxes...')
        status, mailboxes = imap.list()
        if status == 'OK':
            for mailbox in mailboxes:
                logging.info('  ' + mailbox.decode('utf-8'))
        
        logging.info('Selecting INBOX...')
        status, data = imap.select('INBOX')
        if status == 'OK':
            logging.info('INBOX selected successfully!')
            
            logging.info('Searching for messages...')
            status, msgnums = imap.search(None, 'ALL')
            if status == 'OK':
                logging.info(f'Found {len(msgnums[0].split())} messages')
        else:
            logging.error(f'Failed to select INBOX: {data}')
        
        imap.logout()
        logging.info('Connection test completed successfully!')
        
    except Exception as e:
        logging.error(f'Connection test failed: {e}')
        logging.error('\nTroubleshooting tips:')
        logging.error('1. Ensure IMAP is enabled in your email account settings')
        logging.error('2. Try using an app-specific password instead of your regular password')
        logging.error('3. Check if your account has any security restrictions')
        logging.error('4. Verify the server address and port are correct')
        logging.error('\nEnvironment variables:')
        logging.error('  IMAP_HOST - IMAP server address (default: imap.126.com)')
        logging.error('  IMAP_PORT - IMAP server port (default: 993)')
        logging.error('  IMAP_USER - Email address')
        logging.error('  IMAP_PASSWORD - Password or app-specific password')

if __name__ == '__main__':
    test_imap_connection()