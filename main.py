import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from scripts.audit_vpc import audit_aws_vpc
from scripts.audit_ec2 import audit_ec2_instances
from scripts.audit_status import check_infrastructure_status

def main():
    print("=" * 60)
    print(" AWS INFRASTRUCTURE AUTOMATED AUDIT TOOL")
    print("=" * 60)
    print("1. Run VPC & Network Security Audit")
    print("2. Run EC2 Instances Audit")
    print("3. Run Compute & Load Balancer Status Audit")
    print("4. Run All Audits")
    print("=" * 60)
    
    choice = input("Select an option (1-4): ").strip()
    
    if choice == '1':
        audit_aws_vpc()
    elif choice == '2':
        audit_ec2_instances()
    elif choice == '3':
        check_infrastructure_status()
    elif choice == '4':
        print("\n[+] Starting full infrastructure audit...\n")
        audit_aws_vpc()
        print("\n" + "-" * 60 + "\n")
        audit_ec2_instances()
        print("\n" + "-" * 60 + "\n")
        check_infrastructure_status()
    else:
        print("[-] Invalid choice! Please select 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()