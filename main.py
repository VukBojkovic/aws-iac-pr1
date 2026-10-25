import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from scripts.audit_vpc import audit_aws_vpc
from scripts.audit_ec2 import audit_ec2_instances

def main():
    print("=" * 60)
    print(" AWS INFRASTRUCTURE AUTOMATED AUDIT TOOL")
    print("=" * 60)
    print("1. Run VPC & Network Security Audit")
    print("2. Run EC2 Instances Audit")
    print("3. Run All Audits")
    print("=" * 60)
    
    choice = input("Select an option (1-3): ").strip()
    
    if choice == '1':
        audit_aws_vpc()
    elif choice == '2':
        audit_ec2_instances()
    elif choice == '3':
        print("\n[+] Starting full infrastructure audit...\n")
        audit_aws_vpc()
        print("\n" + "-" * 60 + "\n")
        audit_ec2_instances()
    else:
        print("[-] Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()