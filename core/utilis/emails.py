import resend
from django.conf import settings

resend.api_key = settings.RESEND_API_KEY


def send_resend_email(subject, message, recipient):

    try:
        resend.Emails.send({
            "from": "BB CARE <onboarding@resend.dev>",
            "to": [recipient],
            "subject": subject,
            "text": message,
        })

        print("EMAIL SENT:", recipient)
        return True

    except Exception as e:
        print("RESEND ERROR:", e)
        return False