# Certificate Setup

Inside your vagrant guest do the following commands.

## Create certificates
```
cd /vagrant/certs
sudo openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt
sudo openssl genrsa -out client.key 2048
sudo openssl req -out client.csr -key client.key -new
sudo openssl x509 -req -in client.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out client.crt -days 365
sudo openssl verify -verbose -CAfile ca.crt client.crt
```

## ePO Certificate Authority (CA) Import
Copy to certs/ folder.
```
1. Navigate to Server Settings and select the DXL Certificates setting on the left navigation bar.
2. Click the Edit button in the lower right corner (as shown in the image above)
3. Click the Import button in the Client Certificates section (as shown in the image above)
4. Select the Certificate (For example, ca.crt) for the Certificate Authority (CA) that was created previously.
5. Click the OK button in the lower right corner (as shown in the image above)
6. Click the Save button in the lower right corner (as shown in the image above)

The imported Certificate Authority (CA) information will propagate to the DXL brokers. This process can take several minutes to complete.
```

## ePO Broker Certificates Export
Copy Broker Certificates into brokercerts/ folder.
```
The certificate information for DXL Brokers must be available to DXL clients attempting to connect to the fabric. This certificate information allows clients to ensure the Brokers being connected to are valid (via mutual authentication).

The following steps walk through the process to export the DXL Broker certificate information:

1. Navigate to Server Settings and select the DXL Certificates setting on the left navigation bar.
2. Click the Edit button in the lower right corner (as shown in the image above)
3. Click the Export All button in the Broker Certificates section (as shown in the image above)
4. The exported file, brokercerts.crt, will be saved locally.
   
   This file is specified as the broker_ca_bundle parameter when constructing a dxlclient.client_config.DxlClientConfig instance.
   
   This file can also be specified via a configuration file used to instantiate a dxlclient.client_config.DxlClientConfig instance.

```

## ePO Broker List Export
Edit the Broker List in dxlclient.config with this information.
```
1. Navigate to Server Settings and select the DXL Certificates setting on the left navigation bar.
2. Click the Edit button in the lower right corner (as shown in the image above)
3. Click the Export All button in the Broker Certificates section (as shown in the image above)
4. The exported file, brokercerts.crt, will be saved locally.
   
   This file is specified as the broker_ca_bundle parameter when constructing a dxlclient.client_config.DxlClientConfig instance.
   
   This file can also be specified via a configuration file used to instantiate a dxlclient.client_config.DxlClientConfig instance.
```