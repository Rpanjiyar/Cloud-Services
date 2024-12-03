import random
import string
import time
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Load your GCP service account key file
SERVICE_ACCOUNT_FILE = 'path/to/your-service-account-key.json'

# Authenticate using the service account
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE
)
cloud_identity_client = build('cloudidentity', 'v1', credentials=credentials)
iam_client = build('iam', 'v1', credentials=credentials)
project_id = "your-gcp-project-id"

# List of Supported Services
SUPPORTED_SERVICES = [
    "Google Compute Engine", "Google Cloud Storage", "Google Cloud SQL", 
    "Google Kubernetes Engine", "Cloud Functions", "Cloud Monitoring", 
    "Cloud IAM", "Cloud Pub/Sub", "Cloud BigQuery", "Cloud Spanner"
]

def generate_password():
    """Generate a random password for IAM users."""
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choice(characters) for _ in range(12))

def create_service_account(sa_name, project_id):
    """Create a GCP service account."""
    try:
        sa_email = f"{sa_name}@{project_id}.iam.gserviceaccount.com"
        iam_client.projects().serviceAccounts().create(
            name=f"projects/{project_id}",
            body={
                "accountId": sa_name,
                "serviceAccount": {"displayName": sa_name}
            }
        ).execute()
        print(f"Service account {sa_email} created.")
        return sa_email
    except Exception as e:
        print(f"Error creating service account {sa_name}: {e}")
        return None

def assign_role_to_service_account(sa_email, role, project_id):
    """Assign a role to a GCP service account."""
    try:
        policy = iam_client.projects().getIamPolicy(resource=project_id).execute()
        bindings = policy.get('bindings', [])
        bindings.append({"role": role, "members": [f"serviceAccount:{sa_email}"]})
        policy['bindings'] = bindings

        iam_client.projects().setIamPolicy(
            resource=project_id,
            body={"policy": policy}
        ).execute()
        print(f"Assigned role {role} to {sa_email}.")
    except Exception as e:
        print(f"Error assigning role to {sa_email}: {e}")

def deploy_service(service_name, sa_email):
    """Simulate the deployment of GCP services for a service account."""
    print(f"Deploying {service_name} for service account {sa_email}...")
    if service_name == "Google Compute Engine":
        print(f"Simulated Compute Engine instance deployment for {sa_email}.")
    elif service_name == "Google Cloud Storage":
        bucket_name = f"{sa_email.split('@')[0]}-bucket-{random.randint(1000, 9999)}"
        print(f"Simulated Cloud Storage bucket creation: {bucket_name}.")
    else:
        print(f"{service_name} deployment simulation completed.")

def display_service_account_details(service_accounts):
    """Display service account details."""
    print("\nService Account Details:")
    print("=" * 50)
    for sa in service_accounts:
        print(f"Service Account: {sa['email']}")
        print(f"Password: {sa['password']}")
        print("=" * 50)

def main():
    print("Supported GCP Services:")
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

    sa_count = int(input("Enter the number of service accounts to create: "))
    duration_days = int(input("Enter the number of days to run services: "))
    duration_hours = int(input("Enter the number of hours to run services: "))

    service_accounts = []
    for i in range(sa_count):
        sa_name = f"sa-{i+1}"
        sa_email = create_service_account(sa_name, project_id)
        if sa_email:
            password = generate_password()
            assign_role_to_service_account(sa_email, "roles/editor", project_id)
            service_accounts.append({"email": sa_email, "password": password})

    # Display service account details
    display_service_account_details(service_accounts)

    # Deploy services for each service account
    for sa in service_accounts:
        for service in selected_services:
            deploy_service(service, sa["email"])

    # Simulate resource lifecycle
    end_time = datetime.now() + timedelta(days=duration_days, hours=duration_hours)
    print(f"\nResources will run until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    while datetime.now() < end_time:
        time.sleep(10)  # Simulating active resources

    print("\nTime's up! Cleaning up service accounts...")

    # Delete service accounts
    for sa in service_accounts:
        try:
            iam_client.projects().serviceAccounts().delete(
                name=f"projects/{project_id}/serviceAccounts/{sa['email']}"
            ).execute()
            print(f"Deleted service account: {sa['email']}")
        except Exception as e:
            print(f"Error deleting service account {sa['email']}: {e}")

    print("\nCleanup completed.")

if __name__ == "__main__":
    main()
