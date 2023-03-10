# dt-sms-api-sdk-python

This library is meant as an unofficial SDK (Software Development Kit) for the [Deutsche Telekom Developer SMS API](https://developer.telekom.com/products/sms-api/summary) and to give Python developers a quick start to use it withing their code.

Please read the instructions on Deutsche Telekom Developer Portal and set up your account there to get the needed credentials for using this SDK.

## SMS - (Short Message Service)

SMS is a base functionality in GSM conform mobile communication. While it was designed to send a short text message of 160 characters from one cellular to another it got some upgrades and special features. The most important you need to know for proper usage of the API is, that nowadays you can send longer text messages and even use special characters like Emojis. But internally that will be split into multiple SMS messages with reduced text capacity - and as a consumer of the API you will have to pay for each of those split part messages, even if in-front of the receiver it is presented just as one message.

### Pricing

How do you know the price of a Message to be sent?

#### "num_segments"

So the important question for your balance is - how many part messages your account get billed for a message. If you want to understand the splitting you can (interactively) learn it on https://charactercounter.com/sms or use the following helper method:

```
from dt_sms_sdk.message import Message

Message.gsm_split_count("My message to be sent")  # will return 1 for this string
```

Alternatively you could also generate a full Message object
```
from dt_sms_sdk.message import Message

m = Message(_from="+491755555555", _to="+491755555556", _body="My message to be sent")
m.number_of_segments() # will return 1 for this string
```

#### "gross_price"

Now you know, the amount of SMS which will be sent, you need to know the price. Currently, the price is only available on the website https://developer.telekom.com/api/v1/prices

But the SDK will provide you two methods to get an (maybe outdated) offline price list or download the current only one as a list:
```
from dt_sms_sdk.pricing import Pricing
Pricing.default()
Pricing.download()
```

Both list are just the row data, but by instantiating a Pricing object with one of them, you get some controll over it:

```
from dt_sms_sdk.pricing import Pricing

p = Pricing()  # this is directly loading the offline
p = Pricing(Pricing.download())

p.gross_price_by_iso2("DE")  # gives you the price including vat for Germany
```

#### "iso2"

Before starting a deep dive into telephone number plans, just be aware, that some country calling codes are shared by multiple countries e.g. +1 is used by the USA and Canada (and many more). But in the DT pricing list both countries have different prices (e.g. ??? 0.0058 vs. ??? 0.0094 Price excl. VAT on December the 31st 2022).

So how do you know which country are you sending the SMS? Maybe you did not recognized the E164PhoneNumber class above while creating the Message object. The Message class will try to create such an object with the _from string parameter but have to for the _to parameter - otherwise a ValueError is raised.
An E164PhoneNumber object can evaluate the ISO2 code of the given number.

```
from dt_sms_sdk.phone_number import E164PhoneNumber

n = E164PhoneNumber("+491755555555")
n.iso2  # will return "DE" 
```

Using the Message object you can access this information from the _to parameter from the message recipient attribute:

```
from dt_sms_sdk.message import Message

m = Message("+491755555555", "+491755555556", "My message to be sent")
m.recipient.iso2  # will return "DE" 
```

#### "message_gross_price"

With the information about the gross price for a message and in how many parts that will be split you could calculate the price ... or get it done by Pricing:

```
from dt_sms_sdk.pricing import Pricing
from dt_sms_sdk.message import Message

m = Message("+491755555555", "+491755555556", "My message to be sent")

p = Pricing()  # this will use the offline price list within the SDK, to use the current online one, see above.
p.message_gross_price(m)  # will return the total gross price for the message (all of its splits to the designated country). 
```

If the message is not valid or no price data was loaded for the intended country, the returned price will be a Decimal("NaN").

#### "messages_gross_price"

And what if you want to get the price for multiple message, there is also a method for it:

```
p.messages_gross_price([m1, m2, m3]) # if any of m1, m2 or m3 would lead to a Decimal("NaN") price, it will be ignored for the sum
```

While one or more of those message might have a "NotANumber" price value (see above), by default those messages are ignored and only valid prices are summed up.

But you may change the behavior by providing an additional parameter, to change the behavior to: if at least one price is "NotANumber" the whole sum is "NotANumber":

```
p.messages_gross_price([m1, m2, m3], True)  # if any of m1, m2 or m3 would lead to a Decimal("NaN") price, the whole result will be Decimal("NaN")
```

### Invoking

Now that you know the price, you can risk to send the message. All API communication is encapsulated by the Client class in sms_api.py, which needs to be instanced with your API-Key.

```
from dt_sms_sdk.sms_api import Client

c = Client(api_key="YOUR_SECRET_API_KEY")
```

#### Send

The next step is to use this client object and give it the message to send:

```
response = c.send(message=m)
```

Be aware, that multiple exceptions can happen while trying to send an SMS. In general they are from the type SMSAPIError and specified with descended types. So please invoke that method with a try block!

#### Status

The response of the send method above will return an object of the class SMSAPIResponse, which includes a direct status of the invocation and the sid of the request, to query the status later on to see when/if the SMS got delivered. Just invoke the status method with the sid (or for easiness with the response itself - the method will take the sid itself ) and you will get a new SMSAPIResponse object for that Message.

```
updated_response = c.status(response)
print(updated_response.status)  # status is from the Enum class SMSAPIMessageStatus
```