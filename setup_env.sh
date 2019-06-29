pip install virtualenv
virtualenv image_detection_api
source venv/bin/activate
venv/bin/pip install --upgrade google
venv/bin/pip install --upgrade google-cloud-vision
venv/bin/pip install --upgrade google-cloud-storage
venv/bin/pip install --upgrade pytest
venv/bin/pip install --upgrade flask

# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud Platform public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update the package list and install the Cloud SDK
# sudo apt-get update && sudo apt-get install google-cloud-sdk
snap install google-cloud-sdk --classic

# Initialize the SDK
gcloud init
