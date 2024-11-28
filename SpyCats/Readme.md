1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/spy-cat-agency.git
cd spy-cat-agency
```
2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```
3. Install Dependencies
```bash
pip install -r requirements.txt
```
4. Set Up the Database
```bash
python manage.py makemigrations
python manage.py migrate
```
5. Run the Development Server
```bash
python manage.py runserver
```