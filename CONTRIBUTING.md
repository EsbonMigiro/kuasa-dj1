# Contributing to the KUASA Django Rest Framework Backend Project

Thank you for considering contributing to the KUASA Django Rest Framework Backend project. This guide will help you get started with the contribution process.

## Requirements

To contribute effectively to the KUASA Django Rest Framework Backend project, you should meet the following requirements:

- **Version Control**: You should be familiar with version control systems, particularly Git and GitHub.

- **Django and Django Rest Framework**: Proficiency in Django and Django Rest Framework is essential, as this project is built using these technologies.

- **Database Management**: PostgreSQL should be installed on your machine.

- **Python**: Knowledge of Python, including coding standards and best practices.

## Getting Started

1. **Fork the Repository**:
   - Click the "Fork" button at the top right of the [KUASA Django Rest Framework Backend GitHub repository](https://github.com/kuasakenya/kuasa-dj).

2. **Clone Your Fork**:
   - Clone the forked repository to your local machine using the following command:

     ```
     git clone https://github.com/your-username/kuasa-dj.git
     ```

3. **Create a Virtual Environment**:
   - Navigate to the project directory and create a virtual environment:

     ```
     cd kuasa-dj
     pipenv install
     ```

4. **Activate the Virtual Environment**:
   - Activate the virtual environment:

     ```
     pipenv shell
     ```

5. **Install Project Dependencies**:
   - Install project dependencies by running the following command:

     ```
     pip install -r requirements.txt
     ```

6. **Set Up Environment Variables**:
   - Create a `.env` file in the project root and add your environment variables. You can use the provided `.env` as a reference. Ensure that `DEBUG=True` in the `.env` file to enable debugging mode.
   - Copy and paste the following in your `.env` file.

    ```
    DEBUG=True
    ```

7. **Database Setup**:
   - PostgreSQL should be installed on your machine. You don't need to change anything in `settings.py` because `DEBUG=True` is activated in the `.env` file.

8. **Apply Migrations**:
   - Apply database migrations:

     ```
     python3 manage.py makemigrations
     python3 manage.py migrate
     ```

9. **Populate the Database with Dummy Data**:
   - To have the same dummy data as the project's development environment, you can run the following command:

     ```
     python3 manage.py loaddata datadump.json
     ```

   - **Note**: For all dummy data users in the `datadump.json` file, their password is set to "12345678", and superuser usernames are as follows:

     | Username  | Password    |
     |-----------|-------------|
     | K-1000    | 12345678    |
     | K-1001    | 12345678    |
     | K-2026    | 12345678    |

10. **Run the Development Server**:
    - Start the Django development server:

      ```
      python3 manage.py runserver
      ```

11. **Create a Branch**:
    - Create a new branch for your contribution:

      ```
      git checkout -b feature/your-feature-name
      ```

12. **Make Changes**:
    - Make your desired changes or additions to the codebase.

13. **Linting and Formatting**:
    - Before committing your changes, run linting with Flake8 to ensure code quality:

      ```
      flake8 .
      ```

    - To fix linting errors automatically, you can use autopep8. Run the following command for each file with linting errors (replace `<filename>` with the file name):

      ```
      autopep8 --in-place --aggressive --aggressive <filename>
      ```

    - Some errors may need manual correction if autopep8 does not handle them.

14. **Commit Your Changes**:
    - Commit your changes with a clear and descriptive commit message:

      ```
      git commit -m "Add feature: your feature description"
      ```

15. **Push to Your Fork**:
    - Push your changes to your GitHub fork:

      ```
      git push origin feature/your-feature-name
      ```

16. **Open a Pull Request**:
    - Go to the [KUASA Django Rest Framework Backend GitHub repository](https://github.com/kuasakenya/kuasa-dj) and click the "New Pull Request" button.
    - Select the base branch (usually "main" or "master") and your feature branch.
    - Write a detailed description of your changes in the pull request.

17. **Review and Collaborate**:
    - Participate in the discussion and address any feedback or questions related to your pull request.

18. **Merge**:
    - Once your pull request is approved, it will be merged into the main project.

If you have any questions, feedback, or need assistance, feel free to open an issue in the GitHub repository or reach out to the project maintainers through our official communication channels.

Thank you for considering contributing to the KUASA Django Rest Framework Backend project. Your contributions are greatly appreciated, and together, we can make our backend a robust and valuable part of our website.
