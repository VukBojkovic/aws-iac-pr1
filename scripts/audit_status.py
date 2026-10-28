import boto3

ec2_client = boto3.client('ec2', region_name='eu-central-1')
asg_client = boto3.client('autoscaling', region_name='eu-central-1')
elbv2_client = boto3.client('elbv2', region_name='eu-central-1')

def check_infrastructure_status():
    print("--- AWS PROJECT: INFRASTRUCTURE STATUS AUDIT ---")

    
    try:
        lbs = elbv2_client.describe_load_balancers(Names=['aws-iac-pr1-alb'])
        for lb in lbs['LoadBalancers']:
            print(f"\n[ALB] Name: {lb['LoadBalancerName']}")
            print(f"      Status: {lb['State']['Code'].upper()}")
            print(f"      DNS Name: {lb['DNSName']}")
    except Exception as e:
        print(f"\n[ALB] Error fetching Load Balancer: {e}")

    
    try:
        asgs = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=['aws-iac-pr1-asg'])
        for asg in asgs['AutoScalingGroups']:
            print(f"\n[ASG] Name: {asg['AutoScalingGroupName']}")
            print(f"      Min/Desired/Max: {asg['MinSize']} / {asg['DesiredCapacity']} / {asg['MaxSize']}")
            print(f"      Active Instances Count: {len(asg['Instances'])}")
            
            print("      Instances in ASG:")
            for instance in asg['Instances']:
                print(f"        - ID: {instance['InstanceId']} | Zone: {instance['AvailabilityZone']} | Health: {instance['HealthStatus']} | State: {instance['LifecycleState']}")
    except Exception as e:
        print(f"\n[ASG] Error fetching Auto Scaling Group: {e}")

    print("\n---------------------------------------------------")

if __name__ == "__main__":
    check_infrastructure_status()