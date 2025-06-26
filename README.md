## 🔧 How to Run Tests Locally

1. Clone the repo:
   ```bash
   git clone https://github.com/username/Smartup_testlar.git
   cd Smartup_testlar
   
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt

pytest all_test_runner.py::test_all -v --alluredir=allure-results
allure serve allure-results
