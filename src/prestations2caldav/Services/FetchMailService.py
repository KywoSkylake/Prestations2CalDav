import imaplib, email, os, logging

logger = logging.getLogger(__name__)

class FetchEmail():

    connection = None
    error = None

    def __init__(self, mail_server, username, password):
        self.connection = imaplib.IMAP4_SSL(mail_server)
        self.connection.login(username, password)

    def __del__(self):
        self.close_connection()

    def select_mailbox(self, mailbox="INBOX"):
        try:
            self.connection.select(mailbox=mailbox, readonly=False)  # so we can mark mails as read
            logger.debug("Folder '{}' has been selected".format(mailbox))
        except BaseException as e:
            logger.error("Cannot select Folder '{}': {}".format(mailbox, e))

    def close_connection(self):
        """
        Close the connection to the IMAP server
        """
        self.connection.close()

    def save_attachments(self, msg, path, overwrite=False):
        """
        Given a message, save its attachments to the specified
        download folder (default is /tmp)
        return: file path to attachment
        """
        att_path = "No attachment found."
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue

            filename = str(part.get_filename()).strip()
            att_path = os.path.join(os.path.realpath(path), filename)

            if not os.path.isfile(att_path) and not overwrite:
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()
            elif overwrite:
                fp = open(att_path, 'wb')
                fp.write(part.get_payload(decode=True))
                fp.close()

        return att_path

    def fetch_messages(self, searchTerm, mailbox='INBOX'):
        """
        Retrieve unread messages
        """
        self.select_mailbox(mailbox)
        emails = []
        (result, messages) = self.connection.search(None, str(searchTerm).encode('utf-8'))

        if result == "OK":
            for message in messages[0].decode().split(' '):
                try:
                    ret, data = self.connection.fetch(message, '(RFC822)')
                except:
                    logger.info("No emails to read, for search operation {}".format(searchTerm))
                    break

                msg = email.message_from_string(data[0][1].decode("ISO-8859-1"))
                if isinstance(msg, str) == False:
                    emails.append(msg)

            return emails

        self.error = "Failed to retreive emails."
        return emails

    def fetch_messages_content(self, searchTerm = "(UNSEEN)", mailbox='INBOX'):
        """
        Retrieve unread messages
        """
        self.select_mailbox(mailbox)
        (result, messages) = self.connection.search(None, searchTerm)
        body = None

        if result == "OK":
            mail_ids = messages[0]
            id_list = mail_ids.split()

            try:
                #ret, data = self.connection.fetch(id_list[-1], '(UID BODY[TEXT])')
                status, data = self.connection.fetch(id_list[-1], '(RFC822)')
                email_msg = email.message_from_bytes(data[0][1])  # email.message_from_string(data[0][1])

                # If message is multi part we only want the text version of the body, this walks the message and gets the body
                if email_msg.is_multipart():
                    for part in email_msg.walk():
                        if part.get_content_type() == "text/html":
                            body = part.get_payload(decode=True)
                            body = body.decode()

                        elif part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True)
                            body = body.decode()
            except:
                logger.info("No emails to read.")
                self.close_connection()
                return None

            return str(body)

    def parse_email_address(self, email_address):
        """
        Helper function to parse out the email address from the message
        return: tuple (name, address). Eg. ('John Doe', 'jdoe@example.com')
        """
        return email.utils.parseaddr(email_address)