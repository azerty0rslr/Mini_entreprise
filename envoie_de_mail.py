import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def envoie_mail(temp, sender_email, sender_password, receiver_email):
        # Infos de l'expéditeur
    sender_email = sender_email
    sender_password = sender_password  # Utilise un mot de passe d'application si tu es sur Gmail

    # Destinataire
    receiver_email = receiver_email

    # Sujet et message
    subject = "Hello depuis Python 👋"
    body = f"Durée estimée de conservation : {temp} jours"

    # Création du message
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    # Connexion au serveur SMTP de Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print("E-mail envoyé avec succès ! 🎉")
    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")
    return
