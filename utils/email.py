import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# ==================== EMAIL KONFIGURATSIYASI ====================
EMAIL_SENDER = 'tjasur224@gmail.com'
EMAIL_PASSWORD = 'tulq nero mjac xtih'
EMAIL_RECIPIENTS = ['tjasur224@gmail.com']
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587


# ==================== EMAIL YUBORISH FUNKTSIYASI ====================
def send_email_report(subject, body, attachment_path=None):
    """
    Email orqali test natijalarini yuboradi

    Args:
        subject: Email sarlavhasi
        body: Email asosiy mazmuni
        attachment_path: Qo'shimcha fayl yo'li (ixtiyoriy)
    """
    try:
        for recipient in EMAIL_RECIPIENTS:
            try:
                # Email xabarini tayyorlash
                msg = MIMEMultipart()
                msg['From'] = EMAIL_SENDER
                msg['To'] = recipient
                msg['Subject'] = subject

                # Body qo'shish
                msg.attach(MIMEText(body, 'plain', 'utf-8'))

                # Agar fayl biriktirilgan bo'lsa
                if attachment_path and os.path.exists(attachment_path):
                    with open(attachment_path, 'rb') as attachment:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(attachment.read())
                        encoders.encode_base64(part)
                        part.add_header(
                            'Content-Disposition',
                            f'attachment; filename= {os.path.basename(attachment_path)}'
                        )
                        msg.attach(part)

                # SMTP orqali email yuborish
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()
                    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
                    server.send_message(msg)

                print(f"✅ Email yuborildi: {recipient}")

            except smtplib.SMTPAuthenticationError:
                print(f"❌ Autentifikatsiya xatosi: {recipient}")
            except smtplib.SMTPException as e:
                print(f"❌ SMTP xatosi ({recipient}): {e}")
            except Exception as e:
                print(f"❌ Email yuborishda xatolik ({recipient}): {e}")

    except Exception as e:
        print(f"❌ Email jarayoni xatosi: {e}")


def format_test_results(passed, failed, skipped, errors, total_duration, test_details):
    """
    Test natijalarini formatlash

    Args:
        passed: O'tgan testlar soni
        failed: Muvaffaqiyatsiz testlar soni
        skipped: O'tkazib yuborilgan testlar soni
        errors: Xatolar soni
        total_duration: Umumiy davomiylik
        test_details: Test tafsilotlari

    Returns:
        Formatlangan xabar matni
    """
    total = passed + failed + skipped + errors
    success_rate = (passed / total * 100) if total > 0 else 0

    # Emoji yordamida status
    status_emoji = "✅" if failed == 0 and errors == 0 else "❌"

    body = f"""
{'=' * 70}
{status_emoji} TEST NATIJALARI
{'=' * 70}

📊 UMUMIY STATISTIKA:
{'─' * 70}
Jami testlar:              {total}
✅ Muvaffaqiyatli:         {passed}
❌ Muvaffaqiyatsiz:        {failed}
⏭️  O'tkazib yuborilgan:   {skipped}
⚠️  Xatolar:               {errors}
📈 Muvaffaqiyat darajasi:  {success_rate:.1f}%
⏱️  Umumiy davomiylik:     {total_duration:.2f} sekund

{'=' * 70}
📋 TEST TAFSILOTLARI:
{'=' * 70}
"""

    # Muvaffaqiyatsiz testlarni ko'rsatish
    if test_details['failed']:
        body += "\n❌ MUVAFFAQIYATSIZ TESTLAR:\n"
        body += "─" * 70 + "\n"
        for i, test in enumerate(test_details['failed'], 1):
            body += f"\n{i}. {test['name']}\n"
            body += f"   ⏱️ Davomiylik: {test['duration']:.2f}s\n"
            if test.get('error'):
                body += f"   ⚠️ Xato: {test['error'][:200]}...\n"

    # O'tgan testlarni ko'rsatish
    if test_details['passed']:
        body += "\n\n✅ MUVAFFAQIYATLI TESTLAR:\n"
        body += "─" * 70 + "\n"
        for i, test in enumerate(test_details['passed'], 1):
            body += f"{i}. {test['name']} (⏱️ {test['duration']:.2f}s)\n"

    # O'tkazib yuborilgan testlar
    if test_details['skipped']:
        body += "\n\n⏭️ O'TKAZIB YUBORILGAN TESTLAR:\n"
        body += "─" * 70 + "\n"
        for i, test in enumerate(test_details['skipped'], 1):
            body += f"{i}. {test['name']}\n"
            if test.get('reason'):
                body += f"   Sabab: {test['reason']}\n"

    body += "\n" + "=" * 70 + "\n"
    body += f"📅 Sana: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    body += "=" * 70 + "\n"

    return body