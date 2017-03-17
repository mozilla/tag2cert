# tag2cert
Lightweight pip installable wrapper for creating and renewing Let's Encrypt certificates using Route53 and AWS Tags

## Description
During CloudInit new machines deployed need to be able to automatically generate let's encrypt certificates.
Ideally as a user the you can set the Domain name and contact e-mail as AWS Tags.  

The command line utility requires two tags set on the instance to autocert with let's encrypt using another cool
project the lego certificate client.  

__Required AWS Tags:__

* LE_Domain ( your domain name foo.bar.com )
* LE_Email ( admin@foo.bar.com )

## Usage

```
usage: tag2cert [-h] [--verbose] [--testing] [--setup] [--renew]

AutoCert wrapper for calling during CloudInit. Requires lego on the system and
Route53 delegation.

optional arguments:
  -h, --help  show this help message and exit

  --verbose   log debug messages
  --testing   Use the let's encrypt staging instance
  --setup     Generate a let's encrypt certificate with lego for the first
              time and setup a cron job to renew. Requires AWS tag of
              LE_DOMAIN set.
  --renew     Will renew the let's encrypt certificate using the lego ACME
              client for the AWS tag value of LE_DOMAIN.
```

## TLDR on Route53 Zones

You must have the following IAM Policy on the Route53 zone for Let's Encrypt to
validate against.  Attach this inline or as a policy to your instance profile.

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "route53:GetChange",
                "route53:ListHostedZonesByName"
            ],
            "Resource": [
                "*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "route53:ChangeResourceRecordSets"
            ],
            "Resource": [
                "arn:aws:route53:::hostedzone/<INSERT_YOUR_HOSTED_ZONE_ID_HERE>"
            ]
        }
    ]
}
```
