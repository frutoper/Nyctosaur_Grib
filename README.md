# MarineGRIB-InReach-Transmitter

Before setting out on our year-long Atlantic voyage, we needed a solution for accessing crucial weather data while being out on the open sea without internet connection. With this handy tool, we can now pull GRIB files on-demand using the Garmin inReach Satellite telephone, which turned out to be a cost-effective workaround to pricier options like IridiumGo. The system's entire process is illustrated in the following diagram:
![Workflow](images/workflow_diagram.jpg)

Props to Rhycus for the initial idea behind this workflow (https://github.com/rhycus/GRIB-via-inReach). I've since reworked and enhanced the approach to better align with our needs. A significant modification I made is the transmission of the full GRIB file, rather than just sending specific location data alongside compressed wind details. This approach provides access to a wider range of weather metrics, such as pressure. Moreover, by using a GRIB viewer app that can interpolate data across different time points and zoom levels, the need for high grid resolution is reduced. As a result, even with the expanded data scope, we've kept the message size in check, also due to enhanced compression techniques.

Feel free to use and modify the code to your needs. However, keep in mind that it depends on multiple APIs and libraries, which are subject to change. Always review the code thoroughly before using it, and proceed at your own risk!


## PREREQUISITES

- GARMIN INREACH: Make sure you have a Garmin inReach device with an active subscription. The unlimited message plan is recommended: https://www.garmin.com/en-US/p/837461/pn/010-06005-SU
- GMAIL SETUP: Create a dedicated Gmail account. Make sure the Gmail API is set up and you have the credentials.json files downloaded: https://developers.google.com/gmail/api/quickstart/python
- HOSTING: Use PythonAnywhere or another hosting service to run your script.
- DEVICE SETUP: Ensure you have a device like a tablet or computer with Jupyter Notebook to run the decoder and a GRIB file viewer app.


## REQUESTING GRIB

To request a GRIB-file, send a message to the dedicated Gmail adress via the Garmin inReach with specified weather model, location range, grid size, times and weather paramters. Here's an example of such a request:

```ecmwf:24n,34n,72w,60w|8,8|12,48|wind,press```

This translates to a request for data based on the ECMWF model, covering latitudes from 24N to 34N and longitudes from 72W to 60W, sampled at 8-degree intervals. The forecast times are 12 and 48 hours, and the requested weather parameters are wind and pressure.


## RECEIVING SERVICE

The PythonAnywhere-based receiving service regularly checks the Gmail inbox at one-minute intervals, hunting for new requests. This task is orchestrated by the main.py file, which operates continuously. Upon detecting a new message, it redirects the request to the Saildocs email API (http://www.saildocs.com/gribinfo). Saildocs promptly responds, sending back an email with the desired GRIB file attached to our Gmail. 

Following this, the GRIB file's binary content is extracted, compressed (zipped), and encoded using base64. The compression step effectively reduces the file size by about 35%. The processed data is segmented into smaller chunks, ready to be relayed back to the inReach device. The transmission occurs via a post-request, using the associated inReach link provided with the initial request message.


**NOTE:** Base 64 encoding uses a character set of {A–Z, a–z, 0–9, +, /}, making it suitable for message transmission. While a base 85 representation could further compress the data, reducing its size by an additional 10%, it involves many special characters. These require extra attention. For instance, Rhycus faced issues with certain character combinations like '>f' that were unsendable and demanded extra handling through character shift which may result in sending more messages than anticipated.

**NOTE:** As Rhycus pointed out, messages occasionally get truncated around the 130-140 character range. To circumvent this, we've capped each message to 120 characters.


## DECODING MESSAGE

The messages recived on the inReach device appear like this (based onrequest above):

**Message 1**
```
0 <--- Indicates beginning of first message
eJxzD/J0YmCIY2RgkGFKmvW/QTGTgUucQ5yBgZGBh4uBgUEUxGJQYPjPwMDCwMwQe6BR0qGBYY5Dw+4GeQd5BwcGMBBjYWA45Fx+jV3uZOtdi80Mdvu4FcyB
0 <--- Indicates end of second message
```

**Message 2**
```
1 <--- Indicates beginning of second message
wB236QYkmu62I4u94O5mA9bUhKCWPw0I0xPgpiuR5XYJDqDp0ZmvOAJaPKsjPDonyjAo7mEgYD4JroeYr1/FoZPsla2rF7Zisi3DUrD5AIClUBs=
1 <--- Indicates end of second message, = indicated the end of the transmission
```

To decode these messages efficiently, open them via the Garmin Earthmate App on an iPad. Then, copy and paste the messages into the Decoder Jupyter Notebook, for instance, using the Carnets App. Once decoded, you can view the resulting GRIB-file with a GRIB viewer app, such as LuckGrib.


## EXAMPLE ATLANTIC
Utilising this method, you can acquire wind and pressure data for the Atlantic crossing with two time points with just 6 messages.

**Request:**

```ecmwf:44n,10n,75w,10w|8,8|12,48|wind,press```


**Result (in GRIB viewer app):**
![Screenshot GRIB viewer](images/screenshot_grib_viewer.jpg)
