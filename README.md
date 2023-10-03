# OC_Projet_13 Toolshare

The program is a web application where you can search for borrowable tools and equipment for your construction projects (with a contract system).

## First of all

These instructions will guide you on how to get a copy of my project and test it using your machine's command console.

### Prerequisites

Since the program is written in Python, it needs to be installed on your computer. You can download it from this link : [Télecharger Python](https://www.python.org/downloads/)

You will also need a valid API Key for using [Google Maps](https://developers.google.com/maps/get-started?hl=fr#create-project).

### Installation

First, retrieve my project with this command : 

```git clone https://github.com/R4mTex/P13_POUTOT_Simon.git```

then navigate to this folder :

```cd ToolShare-web-app```

To avoid interfering with other projects, it is recommended to run this one in a virtual environment. Here are the main commands for :

1. Creating a virtual environment 

windows/mac/linux : 

```python -m venv env```

2. Activating the virtual environment

windows : 

```env\Scripts\activate.bat```

mac/linux : 

```source env/bin/activate```

To learn more about virtual environments, you can refer to the documentation here : [Documentation Python](https://docs.python.org/fr/3.6/tutorial/venv.html/)

For the program to function correctly, it is essential to install the provided libraries. These are listed in the requirements.txt document.

Once the console is located in the program's root folder, you can install them using the following command :

```pip install -r requirements.txt --use-pep517```

### Initialization

Execute these commands in sequence :

1. ```python manage.py migrate```
2. ```python manage.py createsuperuser``` (follow the instructions displayed in the command console)

Make sure to replace "GOOGLE_MAPS_API_KEY" in the file "geocoderApi.py" located here : 

```ToolShare-web-app\toolshare\blog\scripts\geocoderApi.py```

Now, if the commands mentioned above have been executed successfully, you can run the following command :

```python manage.py runserver```

Finally, you will be provided with a URL : ```Starting development server at http://127.0.0.1:8000/``` follow the link, and you will be redirected to my site.
Log in with the credentials of the user created just before.

You can stop the server at any time by pressing ```ctrl + c```.

Good luck !

## Built with

[VisualStudioCode](https://code.visualstudio.com/) - Text Editor

## Author

POUTOT Simon. 

### Thanks

Thanks to **GONNAGE Ranga** for their support.
