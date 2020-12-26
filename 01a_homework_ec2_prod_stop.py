import json
import boto3
import os


ec2 = boto3.client('ec2')
sns = boto3.client("sns")
def lambda_handler(event, context):
    # TODO implement
    ec2_dict=ec2.describe_instances()
    
    reservations_list=ec2_dict['Reservations']
    
    snsArn = os.environ['SNS_TOPIC_ARN']
    emailSubject="Prod instance stop"
    message="instance in env prod has been stop"
    
    print("-----------------------------------------")
    for instances in reservations_list:
        # print("instances",instances,type(instances))
        instance_id=instances['Instances'][0]['InstanceId']
        instance_state=instances['Instances'][0]['State']['Name']
        print("instance_id is",instance_id)
        print("instance_state is",instance_state)
        InstanceIdsList= []
        
        tag_lists=instances['Instances'][0]['Tags']
        print("Tags list are",tag_lists)
        for tags in tag_lists:
                if tags['Key']=='env' and tags['Value']=='prod':
                   if instance_state == 'stopped':
                        sns_response =sns.publish(TopicArn=snsArn,Message=message,Subject=emailSubject)                          
            

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
