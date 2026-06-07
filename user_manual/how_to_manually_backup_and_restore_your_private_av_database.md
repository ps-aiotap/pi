**Explaining AV data backups and disaster recovery**

There are three ways the AV platform manages data backups:

1.  **System image backup:\**
    AV performs automatic nightly backups of the entire system as part
    of an overall system off-site disaster recovery setup. This provides
    complete recovery in case of a main server failure.

*Note: This is not designed to back up individual client data files. *

2.  **Secure transfer to the client server:\**
    You can request AV to set up an automatic backup to a server
    designated by you, or to a secure area within a separate Amazon Web
    Services (AWS) data store created with secure FTP access.

*Note: This is a service provided only upon request; additional service
fees apply. *

3.  **Client/User-controlled backup (manual backup):\**
    Completely controlled by you, this functionality initiates a backup
    of your database to a location designated by you. You\'re encouraged
    to understand this feature before using it.

*Note: The first two options are administered by AV and AWS. The third
is described in detail in this article. *

**Where is your data located?**

All client databases only reside in Amazon Web Services (AWS) S3 Bucket
Storage instances in either the United States or India (optional), and
the Disaster Recovery location is in Ohio, California, or Oregon.

**How to use the client/user-controlled backup (manual backup)**

You can back up your AV database regularly based on your usage and
internal policies, e.g., at the end of every AV session, every day,
every week, every month, or any other appropriate interval. For example,
if you are manually backing up your database once the books for a year
are closed, you may also want to make several year-end backup copies and
store them securely, preferably off-site.

*Tip: We highly recommend you follow these procedures for reliable
backup data to restore when needed. This ensures you will always have
recent copies of your critical accounting records in case an issue
occurs beyond normal processing. *

There are two methods to back up data:

- **FTP:** Save all years of database data to a backup file stored on an
  FTP server, which will copy your data to a local network server.

- **Save to local:** Save all years of database data to a backup file
  stored in your choice of location, including to a different folder on
  a local computer or a network's hard disk, CDs, or other backup
  mediums.

**How to take manual backups**

**Step 1**

Go to 'System' from 'Settings' in the 'Menu'. You'll see the below
screen.

![](media/image1.png){width="6.268055555555556in"
height="3.4770833333333333in"}

**Step 2**

Select your preferred restore option.

- **FTP:** Enter your 'Host' name/IP address, 'Username', 'Password',
  and 'Port' number and then select FTP Files to select the backup file
  to restore.

- **Save to local:** To restore from your local system, select 'Choose
  File'. This will bring up the following window:

![](media/image2.png){width="6.268055555555556in"
height="3.4770833333333333in"}

**Step 3**

Select 'OK'

**Step 4**

Choose the destination folder for your backup file and click 'Save'.
You'll get a message saying your backup was successful as soon as the
file has been downloaded and saved to the location of your choice.

**Step 5**

Selecting 'OK' takes you back to the 'System' page, which you can
refresh to see a Backup Audit Trail history. This gives descriptions of
the date and time stamps of all backups being made, and by whom the
backups were initiated.

![](media/image3.png){width="6.268055555555556in"
height="3.4770833333333333in"}

*Note: If you overwrite an existing backup file, all data in that
original file will be lost. If necessary, make sure you have a copy of
the data before overwriting.*

**How to manually restore AV backups**

Kindly get in touch with the AV Support team for backup restoration
assistance.

**We hope you are now able to create data backups on the AV system.
Still have questions? Feel free to reach out to AV\'s Customer Success
Team.**
