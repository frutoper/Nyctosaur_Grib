import time
import sys

sys.path.append(".")
from grib_transmitter import email_functions as email_func
from grib_transmitter import saildoc_functions as saildoc_func
from grib_transmitter import inreach_functions as inreach_func

if __name__ == "__main__":
    # authenticate Gmail API
    auth_service = email_func.gmail_authenticate()

    # check for new InReach messages every minute
    while True:
        print('Checking...', flush=True)

        # check for new messages and retrieve GRIB path and Garmin reply URL
        result = email_func.process_new_inreach_message(auth_service)

        # if a new message is received
        if result is not None:
            grib_path, garmin_reply_url = result

            # encode GRIB to binary
            encoded_grib = saildoc_func.encode_saildocs_grib_file(grib_path)

            # send the encoded GRIB to InReach
            inreach_func.send_messages_to_inreach(garmin_reply_url, encoded_grib)

        # wait for the next check in 60 seconds
        time.sleep(60)