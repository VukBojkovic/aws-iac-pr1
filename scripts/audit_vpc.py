import boto3
from botocore.exceptions import ClientError

def audit_aws_vpc():
    print("=" * 60)
    print(" AWS VPC & NETWORK INFRASTRUCTURE AUDIT")
    print("=" * 60)

    ec2_client = boto3.client('ec2', region_name='eu-central-1')

    try:
        vpcs = ec2_client.describe_vpcs()
        print(f"\n[+] VPCs found: {len(vpcs['Vpcs'])}")
        for vpc in vpcs['Vpcs']:
            print(f"    - VPC ID: {vpc['VpcId']} | CIDR: {vpc['CidrBlock']} | State: {vpc['State']}")


        subnets = ec2_client.describe_subnets()
        print(f"\n[+] Subnets found: {len(subnets['Subnets'])}")
        for subnet in subnets['Subnets']:
            print(f"    - Subnet ID: {subnet['SubnetId']} | CIDR: {subnet['CidrBlock']} | AZ: {subnet['AvailabilityZone']}")


        igws = ec2_client.describe_internet_gateways()
        print(f"\n[+] Internet Gateways found: {len(igws['InternetGateways'])}")
        for igw in igws['InternetGateways']:
            attachments = [att['VpcId'] for att in igw.get('Attachments', [])]
            print(f"    - IGW ID: {igw['InternetGatewayId']} | Attached VPCs: {attachments}")


        route_tables = ec2_client.describe_route_tables()
        print(f"\n[+] Route Tables found: {len(route_tables['RouteTables'])}")
        for rt in route_tables['RouteTables']:
            print(f"    - Route Table ID: {rt['RouteTableId']} | VPC: {rt['VpcId']}")
            for route in rt.get('Routes', []):
                destination = route.get('DestinationCidrBlock', route.get('DestinationIPv6CidrBlock', 'N/A'))
                gateway = route.get('GatewayId', route.get('NatGatewayId', 'local/other'))
                print(f"        * Route -> Destination: {destination} | Target: {gateway}")


        security_groups = ec2_client.describe_security_groups()
        print(f"\n[+] Security Groups found: {len(security_groups['SecurityGroups'])}")
        for sg in security_groups['SecurityGroups']:
            print(f"    - SG ID: {sg['GroupId']} | Name: {sg['GroupName']} | VPC: {sg['VpcId']}")
            print("        * Inbound Rules:")
            if not sg['IpPermissions']:
                print("            (No inbound rules defined)")
            for perm in sg['IpPermissions']:
                protocol = perm.get('IpProtocol', 'all')
                from_port = perm.get('FromPort', 'All')
                to_port = perm.get('ToPort', 'All')
                ip_ranges = [ip['CidrIp'] for ip in perm.get('IpRanges', [])]
                

                is_public = '0.0.0.0/0' in ip_ranges
                warning = " [!] WARNING: OPEN TO THE WORLD!" if is_public and (from_port in [22, 3389, 'All'] or from_port == 'All') else ""
                
                print(f"            - Protocol: {protocol} | Ports: {from_port}-{to_port} | Allowed CIDRs: {ip_ranges}{warning}")


        nat_gws = ec2_client.describe_nat_gateways()
        print(f"\n[+] NAT Gateways found: {len(nat_gws['NatGateways'])}")
        for nat in nat_gws['NatGateways']:
            print(f"    - NAT ID: {nat['NatGatewayId']} | Status: {nat['State']}")

        print("\n" + "=" * 60)
        print(" Audit completed successfully!")
        print("=" * 60)

    except ClientError as e:
        print(f"[-] Error communicating with AWS API: {e}")

if __name__ == "__main__":
    audit_aws_vpc()