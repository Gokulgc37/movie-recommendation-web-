# Movie Recommendation System

This project is a web-based movie recommendation system that provides content-based recommendations. It utilizes FastAPI for the backend, HTML and CSS for the frontend, and is deployed on AWS EC2.

## Technologies Used

- **Backend:** FastAPI
- **Frontend:** HTML, CSS
- **Data Handling:** Pandas
- **Machine Learning:** Scikit-learn
- **Deployment:** AWS EC2

## Installation

Create a project directory:
   mkdir movie-recommendation-system
   cd movie-recommendation-system
   
Create the necessary directories and files:
mkdir templates static data
touch templates/home.html templates/result.html static/style.css data/movies.csv main.py requirements.txt README.md
Add your HTML content to home.html, result.html, and your CSS styles to style.css. Populate movies.csv with your movie data.

Open requirements.txt and add the following dependencies:
fastapi
uvicorn
pandas
numpy
scikit-learn
joblib
jinja2


Create a virtual environment and activate it:
python3 -m venv myenv
source myenv/bin/activate  # For Windows use `myenv\Scripts\activate`

Install the required packages:
pip install -r requirements.txt

Run the FastAPI application locally:(ensure it works properly)
uvicorn main:app --host 127.0.0.1 --port 8000
Open your browser and go to http://127.0.0.1:8000 to access the home page.

## Deployment on AWS
Create a free-tier AWS account and log in to the AWS Management Console.

Navigate to EC2 and create a new instance:

Choose Ubuntu as the AMI.
Select t2.micro for the instance type.
Create a new key pair or use an existing one.
Configure security group to allow SSH, HTTP, and HTTPS traffic.

navigate to security group and click the instance you created, edit the inbound rules and click add rule choose a type as custom TCP , type a port range as 8080 and select the source as Anywhere IPv4
Transfer your local files to the EC2 instance using SCP:
scp -i my-key.pem -r movie-recommendation-system ubuntu@your-public-ip:/home/ubuntu

SSH into the EC2 instance:
ssh -i your-key.pem ubuntu@your-public-ip

Update the package lists and install Python:
sudo apt update
sudo apt install python3 python3-venv

Create and activate a virtual environment:
python3 -m venv myenv
source myenv/bin/activate

Navigate to your project folder:
cd movie-recommendation-system

Install the dependencies:
pip install -r requirements.txt


Run the FastAPI application:
uvicorn main:app --host 0.0.0.0 --port 8080
Access the application from your browser using the public IP of the EC2 instance: http://your-public-ip:8080.

