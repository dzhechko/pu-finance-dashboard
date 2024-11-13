# Product Requirements Document (PRD)

## Project Overview

**Project Name:** Personal Finance Dashboard  
**Platform:** Streamlit application deployed on [Railway.app](https://railway.app)  
**Language:** Menu options and user-facing texts in Russian  
**System Integrations:**  
- YandexGPT for certain system prompts (in Russian)  
- OpenAI-compatible models for other system prompts (in English)

**Description:**  
Develop a comprehensive and interactive Streamlit-based dashboard for personal finance management. The application will allow users to authenticate, upload financial data via Excel files, and visualize their financial health through various interactive charts. The dashboard aims to provide insightful analytics to help users manage their finances effectively.

## Objectives

- **User Authentication:** Secure registration and login system for personalized data access.
- **Data Visualization:** Interactive charts to display net worth, income vs. expenses, expense breakdown by category, and budget vs. actual spending.
- **Data Management:** Efficient loading and handling of financial data from Excel files.
- **User Experience:** Intuitive and user-friendly interface with Russian language support for menu options and system prompts to YandexGPT.
- **Scalability & Maintainability:** Adherence to software design principles to ensure the application is scalable, maintainable, and secure.

## Scope

### In-Scope

- User registration and authentication
- Data upload and parsing from Excel files
- Interactive financial charts:
  - Net Worth Over Time (Line Chart)
  - Income vs. Expenses (Bar Chart)
  - Expense Breakdown by Category (Pie/Donut Chart)
  - Budget vs. Actual Spending (Stacked Bar Chart)
- Interactive dialogues on chart interactions providing analytical insights
- Deployment on Railway.app

### Out-of-Scope

- Mobile application development
- Integration with external financial APIs
- Advanced financial forecasting algorithms

## Functional Requirements

### 0. Logging and Debugging
- please add extended logging and debugging capabilities whenever possible
- but it should be possible to turn on and turn off logging/debugging manually based on the value of variable named DEBUG = "true" or "false" 

### 1. Authentication
- **Description:** Implement a secure authentication system allowing users to register and log in to the application.
- **Purpose:** Ensures that personal financial data is protected and accessible only to authorized users.
- **Implementation Details:**
  - Utilize the `streamlit_authenticator` library for handling authentication processes.
  - Support user registration with email verification.
  - Provide password recovery options.
- It should be possible to turn on and turn off User Authentication based on the value of the variable named AUTH = "true" or "false"

- **Registration Page:**
  - Users can create an account by providing necessary details.
  - Validation for unique usernames/emails.
  - Password strength enforcement.
  
- **Login Page:**
  - Users can log in using their credentials.
  - Forgot password functionality.

### 2. Personal Finance Dashboard

#### a. Net Worth Over Time (Line Chart)

- **Description:** Displays the progression of the user's net worth over a selected period.
- **Interactivity:** Clicking on a data point shows detailed assets and liabilities for that date.
- **Purpose:** Visualize overall financial growth and trends.

#### b. Income vs. Expenses (Bar Chart)

- **Description:** Compares total income against total expenses monthly or yearly.
- **Interactivity:** Clicking on a bar provides a breakdown of income sources or expense categories for that period.
- **Purpose:** Determine financial surplus or deficit periods.

#### c. Expense Breakdown by Category (Pie/Donut Chart)

- **Description:** Shows the percentage distribution of expenses across different categories.
- **Interactivity:** Clicking on a category displays detailed transactions and trends for that category.
- **Purpose:** Identify spending patterns and potential areas for cost-cutting.

#### d. Budget vs. Actual Spending (Stacked Bar Chart)

- **Description:** Compares budgeted amounts to actual spending in each category.
- **Interactivity:** Clicking on a category highlights overspending or underspending details.
- **Purpose:** Monitor adherence to budgets and manage expenses effectively.

### 3. Data Management

- **Excel Data Upload:**
  - Users can upload an Excel file containing financial data.
  - Validation to ensure correct file format and data integrity.

- **Data Sheets:**
  - **Net Worth Table:**
    - Columns: Date, Assets, Liabilities
  - **Income Table:**
    - Columns: IncomeID, Date, Source, Amount
  - **Expenses Table:**
    - Columns: ExpenseID, Date, Category, Description, Amount
  - **Budget Table:**
    - Columns: Category, BudgetAmount

- **Data Processing:**
  - Parsing Excel sheets to extract and process data for visualization.
  - Handling data updates and ensuring synchronization with visual representations.

## Non-Functional Requirements

- **Performance:**  
  - Fast load times for data visualization.
  - Efficient handling of large datasets.

- **Security:**  
  - Secure storage of user credentials.
  - Protection against common vulnerabilities (e.g., SQL injection, XSS).

- **Usability:**  
  - Intuitive interface with Russian language support for all menu options.
  - Responsive design compatible with various screen sizes.

- **Scalability:**  
  - Modular architecture to support future feature expansions.

- **Maintainability:**  
  - Clear codebase structure adhering to software design principles.
  - Comprehensive documentation for ease of maintenance.


## User Interface Design

- **Language Support:**  
  - All menu options and user-facing texts in Russian.
  
- **Layout:**  
  - Authentication pages (Registration & Login) as separate views.
  - Dashboard landing page displaying overview charts.
  - Navigation menu for accessing different chart views and settings.

- **Interactivity:**  
  - Clickable elements on charts triggering dialogues with detailed insights.
  - Responsive filters to adjust time ranges and data views.

## System Architecture

- **Frontend:**  
  - Built with Streamlit leveraging its interactive components.
  
- **Backend:**  
  - Python-based backend handling data processing and authentication.
  
- **Deployment:**  
  - Hosted on Railway.app ensuring scalability and reliability.

- **Integrations:**  
  - YandexGPT for system prompts in Russian.
  - OpenAI-compatible models for system prompts in English.

## Project File Structure 
```
/
├── app.py
├── requirements.txt
├── authentication.py
├── data_loader.py
├── dashboards.py
├── utils.py
└── data/
    ├── net_worth.xlsx
    ├── income.xlsx
    ├── expenses.xlsx
    └── budget.xlsx
```

### File Descriptions

- **app.py:**  
  The main entry point of the Streamlit application. Handles routing and integrates all modules.

- **requirements.txt:**  
  Lists all Python dependencies required for the project.

- **authentication.py:**  
  Manages user registration, login, and authentication logic.

- **data_loader.py:**  
  Responsible for loading and parsing Excel files into usable data structures.

- **dashboards.py:**  
  Contains functions to generate and render all dashboard charts and interactive components.

- **utils.py:**  
  Utility functions and helpers used across the application.

- **data/**  
  Directory containing sample Excel data files for net worth, income, expenses, and budget.

## Documentation

### Data Schemas

#### 1. Net Worth Table

| Column   | Data Type | Description                       |
|----------|-----------|-----------------------------------|
| Date     | DATE      | The date when the net worth was calculated. |
| Assets   | DECIMAL   | Total monetary value of all owned assets. |
| Liabilities | DECIMAL | Total monetary value of all debts and obligations. |

#### 2. Income Table

| Column   | Data Type | Description                               |
|----------|-----------|-------------------------------------------|
| IncomeID | INTEGER   | Unique identifier for each income record. |
| Date     | DATE      | The date the income was received.         |
| Source   | TEXT      | Source of income (e.g., Salary, Rent).    |
| Amount   | DECIMAL   | Amount of money received from the source. |

#### 3. Expenses Table

| Column      | Data Type | Description                                     |
|-------------|-----------|-------------------------------------------------|
| ExpenseID   | INTEGER   | Unique identifier for each expense record.      |
| Date        | DATE      | The date the expense was incurred.              |
| Category    | TEXT      | Category of the expense (e.g., Food, Rent).     |
| Description | TEXT      | Detailed description of the expense.            |
| Amount      | DECIMAL   | Monetary value of the expense.                  |

#### 4. Budget Table

| Column        | Data Type | Description                                     |
|---------------|-----------|-------------------------------------------------|
| Category      | TEXT      | Expense category (e.g., Food, Transportation).  |
| BudgetAmount  | DECIMAL   | Budgeted amount for the respective category.     |

### Example Interactions

#### Net Worth Over Time Chart Interaction

- **User Action:** Clicks on a specific date point on the Net Worth line chart.
  
- **System Response:**  
  A dialogue appears showing:
  - **Assets:** Detailed list and values of each asset.
  - **Liabilities:** Detailed list and values of each liability.
  - **Net Worth Calculation:** Assets minus liabilities for that date.

#### Income vs. Expenses Chart Interaction

- **User Action:** Clicks on the income bar for March 2024.
  
- **System Response:**  
  A dialogue displays:
  - **Income Breakdown:** List of income sources and amounts for March 2024.
  - **Comparative Analysis:** Insights on highest income sources and any anomalies.

#### Expense Breakdown by Category Interaction

- **User Action:** Clicks on the "Food" segment of the pie chart.
  
- **System Response:**  
  A dialogue shows:
  - **Detailed Expenses:** List of all food-related expenses with descriptions and amounts.
  - **Spending Trends:** Analysis of food spending over the selected period.

#### Budget vs. Actual Spending Chart Interaction

- **User Action:** Clicks on the "Transportation" category in the stacked bar chart.
  
- **System Response:**  
  A dialogue presents:
  - **Budget vs. Actual:** Comparison of budgeted vs. actual transportation expenses.
  - **Over/Under Spending:** Highlights any overspending or savings in transportation.

### Example Data Loading
python:/data_loader.py
```
def load_net_worth_data(file_path):
"""
Loads the Net Worth data from the specified Excel file.
Parameters:
file_path (str): Path to the net_worth.xlsx file.
Returns:
pd.DataFrame: DataFrame containing Date, Assets, and Liabilities.
"""
# Implementation details
pass
```

### Example Utility Function
python:/utils.py
```
def calculate_net_worth(assets, liabilities):
"""
Calculates net worth based on assets and liabilities.
Parameters:
assets (float): Total assets.
liabilities (float): Total liabilities.
Returns:
float: Net worth.
"""
```
return assets - liabilities


### Example Dashboard Function

python:/dashboards.py
```
def render_net_worth_chart(data):
"""
Renders the Net Worth Over Time line chart.
Parameters:
data (pd.DataFrame): DataFrame containing Date and Net Worth.
Returns:
None
"""
# Implementation using Streamlit and a plotting library
pass
```


## Development Guidelines

- **Adherence to Software Design Principles:**
  - **KISS:** Keep the implementation straightforward without unnecessary complexity.
  - **YAGNI:** Focus only on current requirements; avoid adding features that may not be needed.
  - **DRY:** Reuse code effectively to minimize duplication.
  - **SOLID:** Ensure each module/class has a single responsibility and follows SOLID principles for maintainability and scalability.
  
- **Modularity and Low Coupling:**  
  Design each component to function independently, allowing for easy updates and maintenance without affecting other parts of the system.

- **Security Best Practices:**  
  Implement secure authentication mechanisms, protect user data, and follow best practices to prevent vulnerabilities.

- **Performance Optimization:**  
  Ensure efficient data processing and rendering of charts to provide a smooth user experience.

- **Comprehensive Documentation:**  
  Maintain clear and detailed documentation to assist developers in understanding and implementing the project effectively.

## Deployment

- **Platform:** Deploy the Streamlit application on Railway.app.
- **CI/CD:** Set up continuous integration and deployment pipelines to automate testing and deployment processes.
- **Environment Configuration:** Manage environment variables securely, especially for authentication and API integrations.

## Testing

- **Unit Testing:**  
  Write unit tests for individual functions and modules to ensure they work as intended.

- **Integration Testing:**  
  Test the interaction between different modules (e.g., authentication and data loading) to identify any issues.

- **User Acceptance Testing (UAT):**  
  Conduct testing sessions with potential users to gather feedback and ensure the application meets user needs.

## Maintenance

- **Monitoring:**  
  Implement monitoring tools to track application performance and identify issues promptly.

- **Regular Updates:**  
  Keep dependencies updated and apply security patches as needed.

- **User Support:**  
  Provide channels for users to report bugs or request features, ensuring timely responses and resolutions.

