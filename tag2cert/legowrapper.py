import os
import boto3
import metadata
import logging


"""Wrapper that governs interactions with the lego client."""

class Certificate(object):
    """Actions pertaining to type of interaction with lego."""
    def __init__(self, testing=False):
        """Initialize the function."""
        self.logger = logging.getLogger(__name__)
        self.__get_metadata()
        self.domain = self.__get_domain()
        self.email = self.__get_email()
        self.lego_path = '/usr/local/bin/lego'
        self.test_mode = testing

        self.logger.info(
            "Executing in {mode} mode".format(
                    mode=self.__get_mode()
                )
        )

    def __get_mode(self):
        if self.test_mode:
            return "Testing"
        else:
            return "Production"

    def __get_metadata(self):
        """Populate metadata from the magic URL."""
        m = metadata.EC2Metadata()
        self.instance_id = m.get('instance-id')
        self.availability_zone = m.get('availability-zone')
        self.region = self.availability_zone[:-1]
        self.logger.info(
            "Metadata retreived for {instance}.".format(
                    instance=self.instance_id
                )
        )

    def __get_domain(self):
        """
        Locate the instance and describe tags.

        Set domain based on presence of valid LE tag attr.
        """
        client = boto3.client(
                    'ec2',
                    region_name=self.region
        )
        response = client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        self.instance_id,
                    ]
                },
            ]
        )
        self.logger.info(
            "Tags retreived for {instance}.".format(
                    instance=self.instance_id
                )
        )
        for tag in response['Tags']:
            if tag['Key'] == 'Domain':
                return tag['Value']
            elif tag['Key'] == 'LE_Domain':
                return tag['Value']
            else:
                pass
        return None

    def __get_email(self):
        """Locate the instance and describe tags.
        Set domain based on presence of valid LE tag attr."""
        client = boto3.client(
                    'ec2',
                    region_name=self.region
        )
        response = client.describe_tags(
            Filters=[
                {
                    'Name': 'resource-id',
                    'Values': [
                        self.instance_id,
                    ]
                },
            ]
        )
        self.logger.info(
            "Tags retreived for {instance}.".format(
                    instance=self.instance_id
                )
        )
        for tag in response['Tags']:
            if tag['Key'] == 'LE_Email':
                return tag['Value']
            else:
                pass
        return None

    def lego_present(self):
        """Check to see if lego exists in the place we expect it to be."""
        return os.path.exists(self.lego_path)

    def renew(self):
        """Renew a cert if the certificate already exists."""
        self.logger.info(
            "Attempting renewal for {domain}.".format(
                    domain=self.domain
                )
        )
        if self.test_mode:
            res = os.popen(
                (
                    "{lego} \
                    --email=\"{email}\" \
                    --server=\"{server}\" \
                    --domains=\"{domain}\" \
                    --dns=\"route53\" \
                    --path=/etc/pki/tls/lego\
                    --accept-tos renew"
                ).format(
                    lego=self.lego_path,
                    email=self.email,
                    domain=self.domain,
                    server='https://acme-staging.api.letsencrypt.org/directory'
                )
            )
        else:
            res = os.popen(
                (
                    "{lego} \
                    --email=\"{email}\" \
                    --domains=\"{domain}\" \
                    --dns=\"route53\" \
                    --path=/etc/pki/tls/lego\
                    --accept-tos renew"
                ).format(
                    lego=self.lego_path,
                    email=self.email,
                    domain=self.domain
                )
            )
        self.logger.info(res)
        if 'Server responded with a certificate.' in res:
            return True
        else:
            return False

    def register(self):
        """Register a new client with Let's Encrypt for your domain(s)."""
        self.logger.info(
            "Attempting lets encrypt registration for {domain}.".format(
                    domain=self.domain
                )
        )
        if self.test_mode:
            res = os.popen(
                (
                    "{lego} \
                    --email=\"{email}\" \
                    --server=\"{server}\" \
                    --domains=\"{domain}\" \
                    --dns=\"route53\" \
                    --path=/etc/pki/tls/lego\
                    --accept-tos run"
                ).format(
                    lego=self.lego_path,
                    email=self.email,
                    domain=self.domain,
                    server='https://acme-staging.api.letsencrypt.org/directory'
                )
            )
        else:
            res = os.popen(
                (
                    "{lego} \
                    --email=\"{email}\" \
                    --domains=\"{domain}\" \
                    --dns=\"route53\" \
                    --path=/etc/pki/tls/lego\
                    --accept-tos run"
                ).format(
                    lego=self.lego_path,
                    email=self.email,
                    domain=self.domain
                )
            )
        self.logger.info(res)
        if 'Server responded with a certificate.' in res:
            return True
        else:
            return False
