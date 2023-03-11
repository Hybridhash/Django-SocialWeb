
# Social Media Application

Social Media Application based on the django framework and django rest api.





## Run Locally

Clone the project

```bash
  git clone https://github.com/Hybridhash/Django-SocialWeb.git
```

Go to the project directory

```bash
  cd socialweb
```

Install dependencies

```bash
  poetry install
```

Start the server

```bash
  poetry run python manage.py runserver 
```

Alternative procedure to run using pip


## Instructions [Enabling Tailwind & Daisy UI]

Ensure that prebuild project has already install locally with the required dependencies in a virtual envoirnment.

### *Enabling Tailwind*

- Create a new directory within your Django project, in which you'll install tailwindCSS like in any vanilla JS project setup: 

```bash
    mkdir jstoolchains 
    cd jstoolchains
    npm init -y
    npm install -D tailwindcss
    npx tailwindcss init
```
- Configure your template paths in tailwind.config.js that have just been created by adding below in a file. *jstoolchains/tailwind.config.js*


```bash
   content: ["../**/templates/**/*.html"],
```

- In "upper/root folder", create an input.css and add below dependencies

```bash
    @tailwind base;
    @tailwind components;
    @tailwind utilities;
```
- In your package.json file, prepare npm scripts to ease execution of tasks (adapt the paths according to your Django static folder location): *jstoolchains\package.json* 

```bash
    "scripts": {
        "tailwind-watch": "tailwindcss -i ../input.css -o ../blogApp/static/css/output.css --watch",
        "tailwind-build": "tailwindcss -i ../input.css -o ../blogApp/static/css/output.css --minify"
    },

```

- In the <head> tag of your base.html add:

```bash
    <link rel="stylesheet" href="{% static "css/output.css" %}">
```

- Test it

```bash
    cd jstoolchains
    npm run tailwind-watch
```

### *Enabling daisyUI*

- Open a terminal, and run the following commands:

```bash
    cd jstoolchains
    npm install daisyui
```

- modify your jstoolchains\tailwind.config.js
```bash
   plugins: [require("daisyui")],
```

voilà!! :cupid:
## Tech Stack

**Client:** HTMX, TailwindCSS, DaisyUI

**Server:** Django, Djnago REST Framework


## Acknowledgements

 - [Guidline to install tailwind/daisy UI in Django project](https://blog.kenshuri.com/posts/001_setup_django_tailwind_daisyui.md)
