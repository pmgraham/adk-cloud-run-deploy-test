## This is an example of how to configure an ADK AI Agent for deploying to Cloud Run.

1. Build the agent and store in the agent directory. In this example `greeter_agent` is the agent directory. Be sure to rename the `.env_example` file to `.env`.

2. Make sure all variables in the `.env` file and the `deploy.sh` file are updated with your Google Cloud information. Note: `us-central1` is the location in the script but you can update and use any supported Google Cloud region for this example.

3. Make sure you have the `gcloud` command line utility installed. If you do not have it, the CLI can be found here https://cloud.google.com/sdk/docs/install.

4. If `gcloud` utility is freshly installed, make sure to run `gcloud init` to setup your Google Cloud CLI and authemticate.

5. Next, make sure you run `gcloud auth application-default login.` This will ensure you don't have to generate a JSON key file or us an API key for authentication with your Google Cloud environment. Further information can be found here: https://cloud.google.com/sdk/gcloud/reference/auth/application-default/login

6. Make sure from your terminal or command line that you are in the root directory of the application (in this case the root directory should be `adk_example`.)

7. Run the `deploy.sh` script by either running `bash deploy.sh` or `./deploy`.

8. Assuming everything is setup correctly the ADK Agent will deploy to Cloud Run.

9. Run the `test_request.py` script to test your newly deployed service. Make sure to update the variables in the `test_request.py` script with your specific Google Cloud information. You should only need to set the `BASE_URL` and `APP_NAME` variables. Make sure the `APP_NAME` in the `test_request.py` script variable matches the `APP_NAME` in the `deploy.sh` script.
