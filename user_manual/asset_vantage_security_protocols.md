**Data Encryption **

- All user credentials in each client AV instance are encrypted using B
  Crypt.

- Data transmission between browser and server.

- Encrypted using Sectigo SSL certificate with RSA 2048 bit encryption
  key with SHA 256 algorithm, RSA encryption.

- Using latest TLS 1.3 version for all application server handshakes.

- Data at rest.

- Hosted on AWS S3, EBS.

- Encrypted with AWS AES 256.

- Backups & Disaster Recovery Snapshots.

- Encrypted and secured with AWS Key Management Service key.

- Accessible only within the same AWS account.

**Backups**

- An optional client requested secure daily backup service is available.

- Stored on SFTP server.

- Backup is encrypted using the client\'s product key and license key.

- Backups are rotated every 90 days.

**Server**

- Access to the database servers is permissioned through the respective
  EC2 and its subnets.

- Connections between application server(s) and database server(s) are
  made using the AWS side root SSL certificate.

**Network **

- All the database and application servers are deployed in a private
  subnet environment. 

- Access to the respective servers is permissible only through the
  secure PEM key with firewall inbound rules via bastion/jump server
  using an audited/logged VPN.

**User Access**

- AV supports Two-Factor-Authenticated login access to the application.
