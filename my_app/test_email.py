import smtplib # for testing smtp server :)
try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('fsnforce@gmail.com', 'uqplubkqeposnfdr')  # Use your App Password
    print("Authentication successful!")
    server.quit()
except Exception as e:
    print("Failed to authenticate:", e)

