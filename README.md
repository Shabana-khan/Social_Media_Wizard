# Social_Media_Wizard - MongoDB based Python Project

## Requirements
- Python 3.12
- `pymongo`
- `python-dotenv`

## Setup Instructions

1. Clone the repository:
   ```sh
   git clone https://github.com/Shabana_khan/Social_Media_Wizard.git
   cd <project-directory>
   
2. Run the following commands:
   ### Create Virtual Environment
   python -m venv venv

   ### To cativate the above vitual env
   Windows: venv\Scripts\activate
   Mac/Linux: source venv/bin/activate

   ### Install dependencies
   pip install -r requirements.txt

3. Install MongoDB
   mongod --dbpath "C:\data\db"  # Windows
   sudo systemctl start mongod   # Linux/macOS

4. Add a .env File to the project directory
   MONGO_URI=mongodb://localhost:27017/mydatabase

5. Run the project
   python controller.py
