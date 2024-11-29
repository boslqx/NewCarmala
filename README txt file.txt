# Project name: 
Carmala car rental application

# Description:
Carmala is a car rental application that made with tkinter. Users will use this application as a platform to search for available rental cars. 

# Development tools:
language: python
database: sqlite
prototype design: Figma
frameworks: Tkinter and CustomTkinter
Version control: Git and Github

# User Features
- email verification
- password recovery
- car booking
- cancel bookings
- chat box
- rating and review

# Super admin and admin features:
1. Super admin
   - add, delete or edit car agencies
   - ban penalty user
2. admin
   - manage car inventories
   - review user feedback
   - generate PDF format statistic report

# Installations required
- asgiref==3.8.1
- babel==2.16.0
- chardet==5.2.0
- contourpy==1.3.0
- customtkinter==5.2.2
- cycler==0.12.1
- darkdetect==0.8.0
- Django==5.1.1
- fonttools==4.53.1
- kiwisolver==1.4.7
- matplotlib==3.9.2
- numpy==2.1.1
- packaging==24.1
- pillow==10.4.0
- pyparsing==3.1.4
- PyQt5==5.15.11
- PyQt5-Qt5==5.15.2
- PyQt5_sip==12.15.0
- python-dateutil==2.9.0.post0
- reportlab==4.2.5
- six==1.16.0
- sqlparse==0.5.1
- tkcalendar==1.6.1
- tzdata==2024.1
- xlwt==1.3.0

# Steps to run the system
1. clone the repository
2. install the required packages follows the installation list
4. compile and run
5. Carmala application start from Login.py first for both user and admin login
6. Admin does not have the ability to create account themselves, super admin is the one that creates account and pass to agencies

(For admin login, user might encounter error like "Modules cannot be found". If the problem cannot be solved by redownload the specific module, can just open Adminpage.py because the login already remembered last logged in admin)

