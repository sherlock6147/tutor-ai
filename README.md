# TutorAI 
## What is TutorAI
TutorAI is a conversational AI to help you gain a deeper understanding of any topic you're curious about.

## Setting up TutorAI(from the drive link)
the db.qlite3 file and .env files are already provided in this case, please follow the following commands to start running the project

1. Change into the tutor-ai directory

        cd tutor-ai/
2. Setup the virtual environment(linux)

        virtualenv env

    You can visit [here](https://www.geeksforgeeks.org/creating-python-virtual-environment-windows-linux/) to learn more about creating virtual environments for python on windows or linux

3. Activate the virtual environment

        source env/bin/activate (linux)
        env\Scripts\activate (windows)

4. Now install the requirements

        pip install -r requirements.txt

5. Now run the server

        python manage.py runserver

6. Now you can login using google at [http://127.0.0.1:8000/](http://127.0.0.1:8000/) and explore the project

Admin Password

username - admin

password - 1234

You can use these credentials to login on the admin page at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)