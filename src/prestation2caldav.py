from prestations2caldav.Services import FetchMailService, CalDavService
import logging, sys, os, argparse, textwrap, time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


parser = argparse.ArgumentParser(prog="prestation2caldav", description=textwrap.dedent('''\
Prestation2CalDav
--------------------------------
Save events from an email received from Protail CGDIS into your caldav
'''))
parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument('--mail-server',     type=str, default=os.environ.get("MAIL_SERVER",     None),
                    help="IMAP Email Server where the email arrives")
parser.add_argument('--mail-username',   type=str, default=os.environ.get("MAIL_USERNAME",   None),
                    help="IMAP Username")
parser.add_argument('--mail-password',   type=str, default=os.environ.get("MAIL_PASSWORD",   None),
                    help="IMAP Password")
parser.add_argument('--caldav-url',      type=str, default=os.environ.get("CALDAV_URL",      None),
                    help="Caldav URL")
parser.add_argument('--caldav-username', type=str, default=os.environ.get("CALDAV_USERNAME", None),
                    help="Caldav Username")
parser.add_argument('--caldav-password', type=str, default=os.environ.get("CALDAV_PASSWORD", None),
                    help="Caldav Password")
parser.add_argument('--caldav-calendar', type=str, default=os.environ.get("CALDAV_CALENDAR", "personal"),
                    help="Calender ID to save the event")

def main(mail_server, mail_username, mail_password, caldav_url, caldav_username, caldav_password, caldav_calendar):
    mail_service = FetchMailService.FetchEmail(mail_server, mail_username, mail_password)
    dav_client = CalDavService.CalDav(caldav_url, caldav_username, caldav_password)
    calendar = dav_client.fetch_calendar(caldav_calendar.title(), caldav_calendar)

    mails = mail_service.fetch_messages("(UNSEEN) SUBJECT \"Prestations\"")
    if len(mails) == 0:
        logger.info(f"No Emails has been found on {mail_service}")
        return

    for msg in mails:
        logger.info(f"Email {msg} found")
        for attachment in msg.get_payload():
            if attachment.get_content_type() == "application/octet-stream":
                logger.info(f"Event {attachment} was found")
                try:
                    dav_client.add_event(attachment.get_payload(decode=True).decode(), calendar)
                    logger.info("Event was added")
                except BaseException as e:
                    logger.error(f"Event couldn't be saved: {e}", exc_info=True)


if __name__ == "__main__":
    args = parser.parse_args()
    if args.mail_server == None or args.mail_username == None or args.mail_password == None:
        parser.print_help()
        raise RuntimeError("No Email Server details were specified")

    if args.caldav_url == None or args.caldav_username == None or args.caldav_password == None:
        parser.print_help()
        raise RuntimeError("No Caldav details were specified")


    while True:
        main(args.mail_server, args.mail_username, args.mail_password,
            args.caldav_url, args.caldav_username, args.caldav_password, args.caldav_calendar)
        time.sleep(600)