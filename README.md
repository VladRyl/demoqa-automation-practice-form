# 🧪 DemoQA Practice Form - Automated Test Suite

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.59+-2EAD33?style=for-the-badge&logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![Pytest](https://img.shields.io/badge/Pytest-9.1+-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![Allure Report](https://img.shields.io/badge/Allure_Report-2.27+-FFA000?style=for-the-badge&logo=qameta&logoColor=white)](https://allurereport.org/)
[![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

A scalable, production-grade test automation framework designed for the [DemoQA Student Registration Practice Form](https://demoqa.com/automation-practice-form). Built with **Python**, **Playwright (Sync API)**, **Pytest**, **Page Object Model (POM)** design pattern, and **Allure Report** with CI/CD integration via **GitHub Actions**.

---

## 🌟 Key Features

- **🏛 Page Object Model (POM)**: Clean separation between page elements, interaction logic, and test assertions.
- **⚡️ Parallel Execution (`pytest-xdist`)**: Distributed multi-worker test execution reducing suite run time significantly.
- **📊 Interactive Allure Reporting**:
  - Full-page screenshot capture automatically attached upon test failure.
  - Step-by-step breakdown and categorized test outcomes.
  - Historical trends and execution statistics deployed to GitHub Pages.
- **📸 Local Screenshot Persistence**: Auto-saves failed test captures into `screenshots/` directory for immediate inspection.
- **🧪 Comprehensive Test Coverage**:
  - **Text & Input Validation**: Mandatory & optional fields, character limits, names, regex checks.
  - **Email & Phone Validation**: RFC compliant, invalid patterns, boundary lengths.
  - **Cascade Dropdowns**: Dependent State & City cascading select controls and reset behavior.
  - **Custom React DatePicker**: Leap years, boundary dates, month/year selects, direct input vs widget picker.
  - **Auto-Complete & Badges**: Multi-value subject additions and removals.
  - **Dynamic Controls**: Radio button switches (Gender), multiple checkbox toggles (Hobbies).
  - **File Uploads**: Valid image formats and invalid file extensions.
  - **Color & Style Validation**: Field border colors and validation states (`:valid` / `:invalid`).
- **🚀 CI/CD Pipeline (GitHub Actions)**: Automated test execution on Push/PR with Allure Report deployment to `gh-pages`.

---

## 📁 Project Structure

```text
demoqa-automation-practice-form/
├── .github/
│   └── workflows/
│       └── tests.yml              # CI/CD pipeline (Runs tests & deploys Allure to GitHub Pages)
├── assets/
│   └── manul.jpg                  # Test fixture image for upload scenarios
├── data/
│   ├── date_data.py               # Boundary & leap year test cases for DatePicker
│   ├── email_data.py              # Valid/invalid email dataset
│   ├── file_data.py               # Supported image formats & unauthorized extensions
│   ├── name_data.py               # Valid & boundary name test data
│   ├── phone_data.py              # Mobile phone format test data
│   └── state_city_data.py         # State-to-City cascading dependency map
├── pages/
│   ├── base_page.py               # Generic reusable page methods & Playwright helpers
│   ├── enums.py                   # Enums (Gender, Hobby, ValidationState)
│   └── practice_form_page.py      # Practice Form Page Object with locators and actions
├── tests/
│   └── test_practice_form.py      # Pytest test suite covering all form interactions
├── .gitignore                     # Git ignore rules
├── config.py                      # Base URLs and project configurations
├── conftest.py                    # Pytest fixtures, hooks & automatic Allure screenshot handlers
├── pyproject.toml                 # Pytest CLI options (parallel, Allure dir) & tools config
├── requirements.txt               # Project dependencies
└── README.md                      # Project documentation
```

---

## 🛠 Prerequisites

Ensure you have the following installed on your system:
- **Python 3.11+**
- **Homebrew** (macOS) or package manager for your OS
- **Java (JDK 11+)** *(Required only for Allure CLI report generation)*
- **Allure CLI**:
  ```bash
  brew install allure
  ```

---

## 🚀 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/VladRyl/demoqa-automation-practice-form.git
   cd demoqa-automation-practice-form
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate      # On macOS/Linux
   # or
   .venv\Scripts\activate         # On Windows
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers:**
   ```bash
   playwright install chromium
   ```

---

## 🧪 Running Tests

### 1. Run all tests in parallel (Default):
```bash
pytest
```
*(Uses configuration from `pyproject.toml`: `-n auto --dist=loadfile --alluredir=allure-results --clean-alluredir`)*

### 2. Run with custom worker count:
```bash
pytest -n 4
```

### 3. Run in headed mode (view browser UI):
```bash
pytest --headed
```

### 4. Run a specific test:
```bash
pytest tests/test_practice_form.py -k "test_all_forms_filled_correctly"
```

---

## 📊 Viewing Allure Reports

After running the tests, an interactive Allure report can be generated and served locally:

```bash
allure serve allure-results
```

### Generate static HTML report:
```bash
allure generate allure-results --clean -o allure-report
allure open allure-report
```

> **📌 Note on Screenshots:** When a test fails, a full-page screenshot is automatically captured, attached to the test case inside the Allure Report under the **Test body** / **Attachments** section, and saved locally to the `screenshots/` directory.

---

## 🔄 CI/CD & GitHub Pages Report

This repository includes a pre-configured **GitHub Actions Workflow** (`.github/workflows/tests.yml`):
- Automatically triggers on `push` and `pull_request` to `main` / `master`.
- Sets up Python, Java, dependencies, and Playwright browsers.
- Executes the test suite in headless mode.
- Preserves test run history across builds.
- Deploys the interactive Allure Report to **GitHub Pages**:
  `https://<username>.github.io/demoqa-automation-practice-form/`

---

## 🎨 Code Formatting

The codebase follows PEP 8 standards enforced by **Black**:
```bash
black .
```

---

## 👤 Author

- **Vladislav** - [@VladRyl](https://github.com/VladRyl)
