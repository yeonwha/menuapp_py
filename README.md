# Display Menu App

Displaying menu app is a single page web application to manage the menu of restaurant using Next.js. 
The backend and database are implemented in Python utilizing Django and SQlite.
The frontend is implemented with React and Tailwind.
With this app, the user can create, retrieve, update and delete the food item with a HTTP request.

The base project is a console program in C++.
<a href="https://github.com/yeonwha/Menu.git">C++</a>

The backend is also implemented in JavaScript, Express and MongoDB
<a href="https://github.com/yeonwha/menuapp_js">JavaScript</a>

## Build Environment

    - Complier: Visual Studio Code
    - Framework: Node.js, React, Next.js @latest
    - Middleware and Server: Python Virtual Environment, Django REST Framework
    - Database: Sqlite

## How to run

First, run the frontend on the root directory(menuapp_py/):

```bash
npm run dev
```

Second, 
run the backend server on the menuapp-api(menuapp_py/menuapp-api/) directory:

```bash
source .venv/bin/activate  
python manage.py runserver 0.0.0.0:3005     
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the page.


