import random
import string
import time
from datetime import datetime, timedelta
import oci

# Configuration
OCI_CONFIG_FILE = "~/.oci/config"  # Path to your OCI config file
OCI_PROFILE_NAME = "DEFAULT"      # Profile name in the config file

# Supported OCI Services
SUPPORTED_SERVICES = [
    "Compute Instance", "Object Storage Bucket",
    "Autonomous Database", "Functions Service",
    "Monitoring", "Virtual Cloud Network (VCN)",
    "Block Volume", "API Gateway"
]

# Initialize OCI Clients
config = oci.config.from_file(OCI_CONFIG_FILE, OCI_PROFILE_NAME)
identity_client = oci.identity.IdentityClient(config)

# Retrieve Tenancy OCID
tenancy_ocid = config["tenancy"]


def generate_password():
    """Generate a random password for IAM users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))


def create_iam_user(user_name):
    """Create an OCI IAM user and API key."""
    try:
        # Create IAM user
        user_details = oci.identity.models.CreateUserDetails(
            compartment_id=tenancy_ocid,
            name=user_name,
            description=f"User {user_name}"
        )
        user = identity_client.create_user(user_details).data
        print(f"Created IAM user: {user.name}")

        # Generate a random password
        password = generate_password()
        return {
            "UserName": user.name,
            "UserId": user.id,
            "Password": password
        }
    except Exception as e:
        print(f"Error creating IAM user {user_name}: {e}")
        return None


def assign_policy_to_user(user_id, policy_name="AllowUserToManageResources"):
    """Assign a policy to an IAM user."""
    try:
        policy_statement = f"Allow user {user_id} to manage all-resources in tenancy"
        policy_details = oci.identity.models.CreatePolicyDetails(
            compartment_id=tenancy_ocid,
            name=policy_name,
            description=f"Policy for user {user_id}",
            statements=[policy_statement]
        )
        policy = identity_client.create_policy(policy_details).data
        print(f"Assigned policy {policy.name} to user {user_id}.")
    except Exception as e:
        print(f"Error assigning policy to user {user_id}: {e}")


def deploy_service(service_name, user_name):
    """Simulate the deployment of OCI services."""
    print(f"Deploying {service_name} for user {user_name}...")
    if service_name == "Compute Instance":
        print(f"Simulated Compute Instance deployment for user {user_name}.")
    elif service_name == "Object Storage Bucket":
        bucket_name = f"user-{user_name}-bucket-{random.randint(1000, 9999)}"
        print(f"Simulated Object Storage Bucket creation: {bucket_name}.")
    else:
        print(f"{service_name} deployment simulation completed.")


def delete_iam_user(user):
    """Delete an IAM user."""
    try:
        identity_client.delete_user(user["UserId"])
        print(f"Deleted IAM user: {user['UserName']}")
    except Exception as e:
        print(f"Error deleting IAM user {user['UserName']}: {e}")


def display_iam_details(users):
    """Display IAM user credentials."""
    print("\nIAM User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['UserName']}")
        print(f"Password: {user['Password']}")
        print("=" * 50)


def main():
    print("Supported OCI Services:")
    for idx, service in enumerate(SUPPORTED_SERVICES, start=1):
        print(f"{idx}. {service}")
    print("\nEnter the numbers of the services to deploy (comma-separated, e.g., 1,2,5):")
    services_input = input("Services: ").strip()
    
    try:
        selected_indices = [int(i.strip()) - 1 for i in services_input.split(",")]
        selected_services = [SUPPORTED_SERVICES[i] for i in selected_indices if 0 <= i < len(SUPPORTED_SERVICES)]
    except ValueError:
        print("Invalid input. Please enter valid service numbers.")
        return
    
    if not selected_services:
        print("No services selected. Exiting.")
        return

    iam_user_count = int(input("Enter the number of IAM users to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    users = []
    for i in range(iam_user_count):
        user_name = f"user-{i+1}"
        credentials = create_iam_user(user_name)
        if credentials:
            assign_policy_to_user(credentials["UserId"])
            users.append(credentials)

    # Display IAM user details
    display_iam_details(users)

    # Deploy services for each IAM user
    for user in users:
        for service in selected_services:
            deploy_service(service, user["UserName"])

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up IAM users...")

    # Delete IAM users
    for user in users:
        delete_iam_user(user)

    print("\nCleanup completed.")


if __name__ == "__main__":
    main()
