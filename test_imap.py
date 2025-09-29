#!/usr/bin/env python3
import imaplib
import getpass
import logging

logging.basicConfig(level=logging.INFO)

def test_imap_connection():
    host = 'imap.126.com'
    port = 993
    
    print("Testing IMAP connection to 126.com")
    user = input("Email address: ")
    password = getpass.getpass("Password: ")
    
    try:
        logging.info(f'Connecting to {host}:{port}')
        imap = imaplib.IMAP4_SSL(host, port)
        
        logging.info('Logging in...')
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
        logging.error('1. Ensure IMAP is enabled in your 126.com account settings')
        logging.error('2. Try using an app-specific password instead of your regular password')
        logging.error('3. Check if your account has any security restrictions')
        logging.error('4. Visit https://mail.126.com and check account security settings')

if __name__ == '__main__':
    test_imap_connection()