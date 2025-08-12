# Set your Google Cloud Project ID
export GOOGLE_CLOUD_PROJECT="my-gcp-project"

# Set your desired Google Cloud Location
export GOOGLE_CLOUD_LOCATION="us-central1" # Example location

# Set the path to your agent code directory
export AGENT_PATH="./travel_planner" # Assuming travel_planner is in the current directory

# Set a name for your Cloud Run service
export SERVICE_NAME="travel-planner"

# Set an application name (optional)
export APP_NAME="travel-planner-app" # name of the service once deployed to cloud run

adk deploy cloud_run \
--project=$GOOGLE_CLOUD_PROJECT \
--region=$GOOGLE_CLOUD_LOCATION \
--service_name=$SERVICE_NAME \
--app_name=$APP_NAME \
--with_ui \
$AGENT_PATH
