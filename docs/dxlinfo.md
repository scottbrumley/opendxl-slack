# DXL Information

* Copy broker certificates to brokercerts/ directory
* Copy client certificates to the certs/ directory
* Copy dxlclient.config to your / root directory

### Example dxlclient.config
```
[Certs]
BrokerCertChain=/vagrant/brokercerts/brokercerts.crt
CertFile=/vagrant/certs/client.crt
PrivateKey=/vagrant/certs/client.key

[Brokers]
unique_broker_id_1=broker_id_1;broker_port_1;broker_hostname_1;broker_ip_1
unique_broker_id_2=broker_id_2;broker_port_2;broker_hostname_2;broker_ip_2
```