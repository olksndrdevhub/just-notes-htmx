# Just Notes

## Simple Notes App

### Created using Django, HTMX, Alpine.js, TailwindCSS

#### Steps to run locally:
1. create virtual environment
2. install requirements:  
    ```pip install -r requirements.txt```
3. run migrations:  
    ```python manage.py migrate```
4. start server:  
    ```python manage.py runserver```

### Functionality:

    - [*] Register/Login
    - [*] Profile Page:
        - [*] Profile Details update
    - [*] Home (Notes) Page:
        - [*] List All Notes
        - [*] Create new Note
        - [*] Update Note
        - [*] Delete Note
        - [*] Bulk Actions on Notes:
            - [*] Bulk Delete seleted Notes
            - [*] Bulk Change 'Completed' Status on selected Notes