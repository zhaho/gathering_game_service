import os, logging, smtplib, requests, time
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from sys import stdout

version = "2.3"
day_limit = 3  # Limit for when to start send email
load_dotenv()

# Constants
LOG_FORMAT = "%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s"

# Setup Logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Console Handler
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logging.Formatter(LOG_FORMAT))
logger.addHandler(consoleHandler)

# Log Messages
logger.info('Script is running')
logger.info(f'Using version: {version}')

def send_mail(to, subject, body):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = os.getenv('MAIL_FROM')
    msg['To'] = to
    msg.attach(MIMEText(body, 'html'))

    with smtplib.SMTP(os.getenv('SMTP_SERVER'), 587) as mail:
        mail.ehlo()
        mail.starttls()
        mail.login(os.getenv('SMTP_LOGIN'), os.getenv('SMTP_PASS'))
        mail.sendmail(os.getenv('MAIL_FROM'), to, msg.as_string())

def get_api_data(endpoint):
    api_url = os.getenv('API_URL') + endpoint
    req = requests.get(api_url,timeout=5)
    return req.json()

def process_event(event, day_limit):
    logger.info("processing event: "+ event['id'])
    mail_games, mail_users = {}, {}

    event_start = event['date_start'].split(" ")[0]
    variable_date = datetime.strptime(event_start, '%Y-%m-%d')
    current_date = datetime.now()
    difference = variable_date - current_date

    if difference < timedelta(days=day_limit) and difference > timedelta(days=1):
        logger.info(f"- < {day_limit} days")
        signups = get_api_data(os.getenv('API_ENDPOINT_LIST_GET_EVENT_SIGNUPS') + f"/{event['id']}")
        users = get_api_data(os.getenv('API_ENDPOINT_LIST_USERS'))

        for signed in signups:
            games = get_api_data(os.getenv('API_ENDPOINT_LIST_GET_TITLES_TO_BRING') + f"/{event['id']}/{signed['user_id']}")

            for user in users:
                if user['id'] == signed['user_id']:
                    mail_games[user['firstname']] = games
                    mail_users[user['email']] = user['firstname']

        if mail_users:
            logger.info(f"- title: '{event['title']}'")
            logger.info(f"- users: {len(mail_users)}")
            logger.info(f"- games: {str(mail_games)}")
        else:
            logger.info("- no users signed - skip")

    else:
        logger.info('- > '+str(day_limit) +' days')

    for mail, usr in mail_users.items():
        subject = "Gathering: Upcoming Event!"
        mail_games_body = ""

        for attender, games in mail_games.items():
            if games:
                mail_games_body += f"{attender}'s games:<br>"

                for game in games:
                    mail_games_body += f"- {game}<br>"

        if len(mail_games_body) == 0:
            mail_games_body = "-"
                
        body = f"""\
            <html>
            <head></head>
            <body>
                <p>Dear {usr},<br>
                You have an upcoming event within a week that you have signed up for.</p>
                <h3>{event['title']}</h3>
                <b>Event Details:</b><br>
                <p>- Start Date: {event['date_start']}<br>
                - Location: {event['location']}<br>
                - Player Limit: {event['player_limit']}</p>
                
                <h4>Games that are currently planned to be brought:</h4>
                    {mail_games_body}
                <br>
                If you wish to bring some games of your own or vote on some additional games to be brought, the time is now!
                <br><br>
                For more information, go to <a href="{os.getenv('GATHERING_URL')}">Gathering</a>.<br>
                <p>
                    <a href="{os.getenv('GATHERING_URL')}"><img src="{os.getenv('GATHERING_LOGO')}" width="100" height="100" /></a>
                </p>
                </p>
            </body>
            </html>
            """

        send_mail(to=mail, subject=subject, body=body)
        logger.info(f"- sent mail to: {mail}")

if __name__ == "__main__":
    while True:
        events = get_api_data(os.getenv('API_ENDPOINT_LIST_UPCOMING_EVENTS')) # Get upcoming events

        for event in events:
            process_event(event, day_limit)
        if not events:
            logger.info("no upcoming events")
            logger.info("script ended")
            
        time.sleep(24.0 * 60.0 * 60.0)