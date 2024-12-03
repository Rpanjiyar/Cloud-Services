import random
import string
import time
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.authorization import AuthorizationManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient

# Azure credentials
tenant_id = "your-tenant-id"
client_id = "your-client-id"
client_secret = "your-client-secret"
subscription_id = "your-subscription-id"

# Initialize clients
credentials = ClientSecretCredential(tenant_id, client_id, client_secret)
auth_client = AuthorizationManagementClient(credentials, subscription_id)
resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
storage_client = StorageManagementClient(credentials, subscription_id)

# List of Supported Azure Services
SUPPORTED_SERVICES = [
    "Azure Virtual Machines", "Azure Blob Storage", "Azure SQL Database", "Azure Active Directory",
    "Azure Kubernetes Service", "Azure App Service", "Azure Functions", "Azure Virtual Networks"
]

def generate_password():
    """Generate a random password for Azure users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def create_azure_user(user_name):
    """Create an Azure AD user and return credentials."""
    try:
        # Here we simulate creating an Azure AD user
        password = generate_password()
        
        # Normally we would use Azure Graph API to create users here, but for the sake of simulation,
        # we just return the generated password as an Azure AD user.
        login_url = f"https://portal.azure.com"
        
        # Simulate assigning a role (for example, Contributor)
        role_assignment = {
            "UserName": user_name,
            "Password": password,
            "Role": "Contributor",
            "LoginURL": login_url
        }

        return role_assignment
    except Exception as e:
        print(f"Error creating Azure user {user_name}: {e}")
        return None

def deploy_azure_service(service_name, user):
    """Simulate the deployment of Azure services for a given user."""
    print(f"Deploying {service_name} for user {user['UserName']}...")
    if service_name == "Azure Virtual Machines":
        print(f"Simulated Azure VM creation for user {user['UserName']}.")
    elif service_name == "Azure Blob Storage":
        storage_account = f"user{user['UserName']}-storage-{random.randint(1000, 9999)}"
        print(f"Simulated Blob Storage creation: {storage_account}.")
    else:
        print(f"{service_name} deployment simulation completed.")

def display_azure_details(users):
    """Display Azure user credentials in the Bash console."""
    print("\nAzure User Details:")
    print("=" * 50)
    for user in users:
        print(f"User Name: {user['UserName']}")
        print(f"Password: {user['Password']}")
        print(f"Role: {user['Role']}")
        print(f"Login URL: {user['LoginURL']}")
        print("=" * 50)

def main():
    print("Supported Azure Services:")
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

    azure_user_count = int(input("Enter the number of Azure users to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    users = []
    for i in range(azure_user_count):
        user_name = f"user-{i+1}"
        credentials = create_azure_user(user_name)
        if credentials:
            users.append(credentials)

    # Display Azure user details
    display_azure_details(users)

    # Deploy services for each Azure user
    for user in users:
        for service in selected_services:
            deploy_azure_service(service, user)

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up Azure users...")

    # Simulate cleanup (for actual deletion, we would interact with Azure AD)
    for user in users:
        print(f"Deleted Azure user: {user['UserName']}")

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()
