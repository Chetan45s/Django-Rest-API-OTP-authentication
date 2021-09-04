## REST Api's to authenticate user by Phone & OTP using Django Rest Framework 

  End Points are tested on postman and full details of each endpoint is given in the image stepwise
  
  Before using the api we need to install the project in your machine.
  
  If you are working in backend part and want to integrate this in your backend then :
  
  ### For Adding code files in backend
    
    - Install python and activate virtual environment
    - Create the django app 
      
      django-admin startproject "your project name"
      Copy the All_Users folder into your django project.
      Add urls and All_Users name in the url.py and setting.py of main folder of django
      
      Steps to migrate changes in the database :
      
      python manage.py makemigrations All_Users
      python manage.py migrate
      
      Now, you can use end points given in the images below

  ### For using end points only
    - Install python and activate virtual environment
    - git clone https://github.com/Chetan45s/Project1.git
    - cd Project1
    - pip install -r requirement.txt
    - python manage.py runserver
    - Now you can use end points given in the images below
    
    
### Images 

![/send_otp](https://raw.githubusercontent.com/Chetan45s/Project1/main/images/Screenshot%20(395).png)
![/verify_user](https://raw.githubusercontent.com/Chetan45s/Project1/main/images/Screenshot%20(396).png)
![/Register](https://raw.githubusercontent.com/Chetan45s/Project1/main/images/Screenshot%20(397).png)
![/login](https://raw.githubusercontent.com/Chetan45s/Project1/main/images/Screenshot%20(398).png)
  
  
