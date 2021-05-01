#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 06:12:13 2021

@author: john
"""
import boto3
import pandas as pd
import configparser
import logging
import os
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("create_AWS_resources_iaac.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
"""
Clean up your resources
"""

KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')
DWH_ENDPOINT       = config.get("DWH","HOST")
DWH_ROLE_ARN          = config.get("DWH","DWH_ROLE_ARN")

DWH_DB                 = config.get("DWH","DWH_DB")
DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
DWH_PORT               = config.get("DWH","DWH_PORT")

DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")
#############################################################################
iam = boto3.client("iam", region_name="us-west-1",
                   aws_access_key_id=KEY,
                   aws_secret_access_key=SECRET)

redshift = boto3.client("redshift", region_name="us-west-1",
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET)


conn_string="postgresql://{}:{}@{}:{}/{}".format(DWH_DB_USER, DWH_DB_PASSWORD,
                                                 DWH_ENDPOINT, DWH_PORT,DWH_DB)


###############################################################################
def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus",
                  "MasterUsername", "DBName", "Endpoint",
                  "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

###############################################################################
if __name__ == "__main__":
# deleting the created resources
    redshift.delete_cluster( ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
                            SkipFinalClusterSnapshot=True)
    
    iam.detach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess")
    iam.delete_role(RoleName=DWH_IAM_ROLE_NAME)
    
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    LOG.info("The status now is: %s " % myClusterProps["ClusterStatus"])

###############################################################################


