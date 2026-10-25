import boto3
from botocore.exceptions import ClientError

def audit_ec2_instances():
    print("=" * 60)
    print(" AWS EC2 INSTANCES AUDIT")
    print("=" * 60)

    ec2_client = boto3.client('ec2', region_name='eu-central-1')

    try:
        response = ec2_client.describe_instances()
        instances_found = 0

        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                instances_found += 1
                instance_id = instance['InstanceId']
                instance_type = instance['InstanceType']
                state = instance['State']['Name']
                launch_time = instance['LaunchTime']

                name = "N/A"
                for tag in instance.get('Tags', []):
                    if tag['Key'] == 'Name':
                        name = tag['Value']
                        break

                print(f"\n[+] Instance ID: {instance_id}")
                print(f"    - Name: {name}")
                print(f"    - Type: {instance_type}")
                print(f"    - State: {state}")
                print(f"    - Launch Time: {launch_time}")

        if instances_found == 0:
            print("\n[+] No EC2 instances found in this region.")

        print("\n" + "=" * 60)
        print(" EC2 Audit completed successfully!")
        print("=" * 60)

    except ClientError as e:
        print(f"[-] Error communicating with AWS API: {e}")

if __name__ == "__main__":
    audit_ec2_instances()