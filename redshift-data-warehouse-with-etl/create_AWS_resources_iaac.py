import pandas as pd
import boto3
import json
import configparser
import os
import logging
import time

##############################################################################
logging.basicConfig(format="%(asctime)s %(name)s %(levelname)-10s %(message)s")
LOG = logging.getLogger("create_AWS_resources_iaac.py")
LOG.setLevel(os.environ.get("LOG_LEVEL", logging.DEBUG))
config = configparser.ConfigParser()
config.read_file(open('dwh.cfg'))

##############################################################################

KEY                    = config.get('AWS','KEY')
SECRET                 = config.get('AWS','SECRET')

DWH_CLUSTER_TYPE       = config.get("DWH","DWH_CLUSTER_TYPE")
DWH_NUM_NODES          = config.get("DWH","DWH_NUM_NODES")
DWH_NODE_TYPE          = config.get("DWH","DWH_NODE_TYPE")

DWH_CLUSTER_IDENTIFIER = config.get("DWH","DWH_CLUSTER_IDENTIFIER")
DWH_DB                 = config.get("DWH","DWH_DB")
DWH_DB_USER            = config.get("DWH","DWH_DB_USER")
DWH_DB_PASSWORD        = config.get("DWH","DWH_DB_PASSWORD")
DWH_PORT               = config.get("DWH","DWH_PORT")

DWH_IAM_ROLE_NAME      = config.get("DWH", "DWH_IAM_ROLE_NAME")

df = pd.DataFrame({"Param":
                  ["DWH_CLUSTER_TYPE", "DWH_NUM_NODES", "DWH_NODE_TYPE",
                   "DWH_CLUSTER_IDENTIFIER", "DWH_DB", "DWH_DB_USER",
                   "DWH_DB_PASSWORD", "DWH_PORT", "DWH_IAM_ROLE_NAME"],
              "Value":
                  [DWH_CLUSTER_TYPE, DWH_NUM_NODES, DWH_NODE_TYPE,
                   DWH_CLUSTER_IDENTIFIER, DWH_DB, DWH_DB_USER,
                   DWH_DB_PASSWORD, DWH_PORT, DWH_IAM_ROLE_NAME]
             })
##############################################################################

ec2 = boto3.resource("ec2", region_name="us-west-1",
                     aws_access_key_id=KEY,
                     aws_secret_access_key=SECRET)

s3 = boto3.resource("s3", region_name="us-west-1",
                    aws_access_key_id=KEY,
                    aws_secret_access_key=SECRET)

iam = boto3.client("iam", region_name="us-west-1",
                   aws_access_key_id=KEY,
                   aws_secret_access_key=SECRET)

redshift = boto3.client("redshift", region_name="us-west-1",
                        aws_access_key_id=KEY,
                        aws_secret_access_key=SECRET)

##############################################################################

def create_iam_role():
    try:
        LOG.info('Creating a new IAM Role')
        dwhRole = iam.create_role(
            Path='/',
            RoleName=DWH_IAM_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(
                {'Statement': [{'Action': 'sts:AssumeRole',
                                'Effect': 'Allow',
                                'Principal': {'Service': 'redshift.amazonaws.com'}}],
                 'Version': '2012-10-17'}
            ),
            Description='Allows Redshift clusters to call AWS services on your behalf.'
        )
    except Exception as e:
        LOG.info(e)
    return dwhRole


# - For complete arguments to `create_cluster`, see [docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/redshift.html#Redshift.Client.create_cluster)
def create_redshift_cluster():
    try:
        response = redshift.create_cluster(        
            #HW
            ClusterType=DWH_CLUSTER_TYPE,
            NodeType=DWH_NODE_TYPE,
            NumberOfNodes=int(DWH_NUM_NODES),
    
            #Identifiers & Credentials
            DBName=DWH_DB,
            ClusterIdentifier=DWH_CLUSTER_IDENTIFIER,
            MasterUsername=DWH_DB_USER,
            MasterUserPassword=DWH_DB_PASSWORD,
            
            #Roles (for s3 access)
            IamRoles=[roleArn]  
        )
    except Exception as e:
        print(e)
    return response


def prettyRedshiftProps(props):
    pd.set_option('display.max_colwidth', -1)
    keysToShow = ["ClusterIdentifier", "NodeType", "ClusterStatus", "MasterUsername", "DBName", "Endpoint", "NumberOfNodes", 'VpcId']
    x = [(k, v) for k,v in props.items() if k in keysToShow]
    return pd.DataFrame(data=x, columns=["Key", "Value"])

def open_incoming_tcp_port_for_cluster_endpoint(myClusterProps):
    try:
        vpc = ec2.Vpc(id=myClusterProps['VpcId'])
        defaultSg = list(vpc.security_groups.all())[0]
        LOG.info("The default security group is: %s" % defaultSg)
        
        defaultSg.authorize_ingress(
            GroupName=defaultSg.group_name,
            CidrIp='0.0.0.0/0',
            IpProtocol='TCP',
            FromPort=int(DWH_PORT),
            ToPort=int(DWH_PORT)
        )
    except Exception as e:
        LOG.info(e)

if __name__ == "__main__":
##############################################################################

    # Create IAM Role
    iam_role = create_iam_role()
    
    # Attach Policy
    LOG.info('Attaching Policy')
    iam.attach_role_policy(RoleName=DWH_IAM_ROLE_NAME,
                           PolicyArn="arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
                          )['ResponseMetadata']['HTTPStatusCode']
    roleArn = iam.get_role(RoleName=DWH_IAM_ROLE_NAME)['Role']['Arn']
    
    LOG.info(roleArn)
    ##############################################################################
    # - Create a RedShift Cluster
    dwh_cluster = create_redshift_cluster()
    
    ##############################################################################
    # check the cluster status becomes `Available`
    
    myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
    details = prettyRedshiftProps(myClusterProps)
    LOG.info("The details of the cluster created are: %s" % details)
    #############################################################################
    check_status = myClusterProps['ClusterStatus']
    while check_status == 'creating':
        LOG.info("The dwh cluster is still creating, we will sleep for 3mins and try again. \
                 Please check your screen again")
        time.sleep(200)
        myClusterProps = redshift.describe_clusters(ClusterIdentifier=DWH_CLUSTER_IDENTIFIER)['Clusters'][0]
        check_status = myClusterProps['ClusterStatus']
        if check_status == 'available':
            continue
    ##############################################################################
    DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
    LOG.info("The cluster endpoint is %s" % DWH_ENDPOINT)
    
    # STEP 3: Open an incoming  TCP port to access the cluster ednpoint
    
    DWH_ENDPOINT = myClusterProps['Endpoint']['Address']
    DWH_ROLE_ARN = myClusterProps['IamRoles'][0]['IamRoleArn']
    print("DWH_ENDPOINT :: ", DWH_ENDPOINT)
    print("DWH_ROLE_ARN :: ", DWH_ROLE_ARN)
    
    #############################################################################
    conn_string="postgresql://{}:{}@{}:{}/{}".format(DWH_DB_USER, DWH_DB_PASSWORD, DWH_ENDPOINT, DWH_PORT,DWH_DB)
    LOG.info("testing the connection as: %s" % conn_string)
    
    #############################################################################
    # Writing back to config file
    
    config.set("DWH","HOST", DWH_ENDPOINT)
    
    config.set("DWH","DWH_ROLE_ARN", DWH_ROLE_ARN)
    
    
    with open('dwh.cfg', 'w') as conf:
        config.write(conf)


