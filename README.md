[![CircleCI](https://circleci.com/gh/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples.svg?style=shield)](https://circleci.com/gh/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples)
[![Coverage Status](https://coveralls.io/repos/github/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples/badge.svg?branch=master)](https://coveralls.io/github/Eurex-Clearing-Messaging-Interfaces/Python-Code-Examples?branch=master)

# pure_python

Examples in the pure_python folder are using the pure Python version of the Qpid Messaging API. This API supports only AMQP 0-10. To run the examples:
- Install the Qpid Messaging API either from the repositories of your OS or from http://qpid.apache.org/download.html (http://www.apache.org/dyn/closer.lua/qpid/0.32/qpid-python-0.32.tar.gz)
- Change the hostname / IP address, port number, paths to the certificates and account name / queue name
- Run the examples

## SSL

The public and private keys are passed to the client library in the form of file path. The client will open them and use them on its own.

## BroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It stops consuming once the queue is empty.

## RequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message or after time out.

## SSL (Linux)

The underlying C++ libraries are using the NSS tools to handle SSL. The NSS database has to be prepared before running the client and configured using environment variables.

### Preparing the NSS database

1. Create the database: `certutil -N -d sql:<path>`
2. Load the broker public key as a trusted peer `certutil -A -d sql:<path> -t "P,," -n broker -i certutil -A -d sql:./ -t "P,," -n ecag-fixml-simu1 -i ecag-fixml-simu1_deutsche-boerse_com.crt`
3. Load the member public key `certutil -A -d sql:<path> -t ",," -n ABCFR_ABCFRALMMACC1 -i ABCFR_ABCFRALMMACC1.crt`
4. Load the member private key `pk12util -i ABCFR_ABCFRALMMACC1.p12 -d sql:<path>`
5. Create the password file `echo "<password>" > <passwordFile>`

### Configuring the Qpid libraries

The Qpid Messaging C++ libraries are using environment varible to configure the SSL certificates. There are three relevant variables:
- `QPID_SSL_CERT_DB` contains the path to the NSS database
- `QPID_SSL_CERT_PASSWORD_FILE` contains the path to the password file for the database
- `QPID_SSL_CERT_NAME` contains the nick name of the certificate which should be used for the connection

for example:
```
export QPID_SSL_CERT_DB=sql:./tests/resources/
export QPID_SSL_CERT_PASSWORD_FILE=tests/resources/pwdfile
export QPID_SSL_CERT_NAME=ABCFR_ABCFRALMMACC1
```

## SSL (Windows)

The Qpid client application under the Windows can either use certificates for authentication against the broker from the system’s certificate store or the certificates may be provided to the application from files. To use certificates from the system’s store, one has to first properly import them.

### Broker public key

The public key for verifying the identity of Eurex’s AMQP broker has to be always stored directly in Windows certificate store. To import it, follow these steps:

1. Start the certmgr.msc for managing windows certificates
2. Expand the Trusted Root Certification Authorities store
3. Right-click on the Certificates folder and select "Import"
4. Import the broker public key

### Private key in Windows certificate store

To store the private key in the Windows certificate store and use it in your application, follow these steps:

1. Prepare the private key in PKCS12 file
2. Double click the PKCS12 file
3. A dialog window pops up which guides you through the import
4. Use environment variables to point your application to the private key
```
set QPID_SSL_CERT_STORE=<CertificateStore>
set QPID_SSL_CERT_NAME=<friendlyName>
```
For example:
```
set QPID_SSL_CERT_STORE=Personal
set QPID_SSL_CERT_NAME=CN=ABCFR_ABCFRALMMACC1
```

### Using private key directly from PKCS12 file

The private key can be also used directly from the PKCS12 file.

1. Prepare the private key in PKCS12 file
2. Create the password file (a text file containing the password to the PKCS12 file)
3. Use environment variables to point your application to the private key
```
set QPID_SSL_CERT_FILENAME=<certificateFile>
set QPID_SSL_CERT_PASSWORD_FILE=<passwordFile>
set QPID_SSL_CERT_NAME=<friendlyName>
```

For example:
```
set QPID_SSL_CERT_FILENAME=ABCFR_ABCFRALMMACC1.p12
set QPID_SSL_CERT_PASSWORD_FILE=ABCFR_ABCFRALMMACC1.pwd
set QPID_SSL_CERT_NAME=abcfr_abcfralmmacc1
```

## BroadcastReceiver.py

This example connects to the AMQP broker using AMQP 0-10, opens a consumer to the broadcast queue and starts consuming the broadcasts. It stops consuming once the queue is empty.

## RequestResponse.py

This example connects to the broker using AMQP 0-10, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message or after time out.

## Amqp10BroadcastReceiver.py

This example works in the same way as BroadcastReceiver.py, only using AMQP 1.0.

## Amqp10RequestResponse.py

This example works in the same way as RequestResponse.py, only using AMQP 1.0.

# proton_binding

Examples in the proton_binding folder are using the Python binding against the Apache Qpid Proton C library. This API supports only AMQP 1.0. To run the examples:
- Download and install the Qpid Proton library either from the repositories of your OS or from http://qpid.apache.org/download.html
- Download and install the Python binding for the Proton library either from the repositories of your OS or from http://qpid.apache.org/download.html
- Change the hostname / IP address, port number, paths to the certificates and account name / queue name
- Run the examples

## SSL

The public and private keys are passed to the client library in the form of file path. The client will open them and use them on its own.

## BroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It consumes them for a predefined time interval and exits afterwards. This example is using Proton Reactor - it is written in reactive style.

## RequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message. This example is using Proton Reactor - it is written in reactive style.

## BlockingBroadcastReceiver.py

This example connects to the AMQP broker, opens a consumer to the broadcast queue and starts consuming the broadcasts. It consumes them for a predefined time interval and exits afterwards. This example is using more traditional blocking API.

## BlockingRequestResponse.py

This example connects to the broker, sends a request message and waits for a response, which should be sent by the Eurex system. It stops after receiving the response message. This example is using more traditional blocking API.


# Integration tests

The project is using Travis-CI and Circle CI to run its own integration tests. The tests are executed against Docker images which contain the AMQP broker with configuration corresponding to Eurex Clearing FIXML Interface. The details of the Travis-CI and Circle CI integration can be found in the .travis.yml and circle.yml files.

# Documentation

More details about Python APIs and code examples can be found in the Volume B of Eurex Clearing Messaging Interfaces documentation on [Eurex Clearing website](http://www.eurexclearing.com/clearing-en/technology/eurex-release14/system-documentation/system-documentation/861464?frag=861450)
