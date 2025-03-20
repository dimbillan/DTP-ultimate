from dtp import logger
from datetime import datetime

def send_reset_email(student, ip):
    return "Email sent"

def log(request_method, ip, route, username, user_id, message):
    logger.info(f"[{request_method}] - [{ip}] - [{route}] - [{username} - {user_id}] - {message}")