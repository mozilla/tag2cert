#!/usr/bin/env python
import sys
import argparse
import logging

import tag2cert
import legowrapper

"""Basic arg parser for tag2cert cli"""
class cli():
    def __init__(self):
        self.config = None
        self.prog = sys.argv[0].split('/')[-1]

    """Parent parser for top level flags"""
    def parse_args(self, args):

        parser = argparse.ArgumentParser(
            description="""
                AutoCert wrapper for calling during CloudInit. Requires lego on
                the system and Route53 delegation.
            """
        )

        optional_args = parser.add_argument_group()

        optional_args.add_argument(
            '--verbose',
            action='store_true',
            help='log debug messages')

        optional_args.add_argument(
            '--testing',
            action='store_true',
            help='Use the let\'s encrypt staging instance')

        optional_args.add_argument(
            '--setup',
            action='store_true',
            help="""
                Generate a let's encrypt certificate with lego for
                the first time and setup a cron job to renew. Requires
                AWS tag of LE_DOMAIN set.
            """
        )

        optional_args.add_argument(
            '--renew',
            action='store_true',
            help="""
                Will renew the let's encrypt certificate using the lego
                ACME client for the AWS tag value of LE_DOMAIN.
            """
        )

        return parser.parse_args(args)

    """Logic to decide on host or key compromise"""
    def run(self):
        self.config = self.parse_args(sys.argv[1:])

        if self.config.verbose:
            log_level = logging.DEBUG
        else:
            log_level = logging.INFO

        tag2cert.set_stream_logger(level=log_level)
        logger = logging.getLogger(__name__)

        logger.info(
            "Initialization successful proceeding to certificate stuff."
        )

        logger.info(
            "Searching for lego on the system."
        )
        try:
            lc = legowrapper.Certificate(testing=self.config.testing)
            if lc.lego_present:
                logger.info(
                    "Lego Found proceeding with your action."
                )
            else:
                raise "Lego could not be found."

            if lc.renew:
                lc.renew()
            elif lc.setup:
                lc.setup()
            else:
                raise "No command specified."

        except Exception as e:
            logger.info("An error has occurred {e}".format(e=e))
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    c = cli()
    if c.prog is not None:
        c.run()
