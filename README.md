# Packd

## About

An application to help better pack your bags (for travel, daily life, anyting).

## Usage

Updated to run via Docker/Docker Compose. To run this app locally, pull the repository and run: 

`docker-compose up -d --build`

docker-compose files also exist for staging and production, but they're set up to create an SSL certificate for the particular domain this app is hosted at (www.yosh.ski, a domain I already had for another project), so using those docker-compose files won't work withouth some modifications. 

## Screenshots

![Screenshot from 2024-09-04 09-47-15](https://github.com/user-attachments/assets/2da3b5b2-c101-4be0-b9aa-29db05ba8b0b)



## Todos (not prioritized)

* ~Style front end~
* Packr views tests
* NewUserForm tests
* User views tests
* Item images
* ~Set up persistant dev database (Digital Ocean?)~
* ~Add tests for Models and Forms~
* ~Edit Item / Edit Pack~
* ~Add 'bag total weight' and 'bag total volume' calculation and add warnings.~ 
* ~Create Pack~
* ~Share Pack~

## Ideas

* Standard packing lists for particular activities
* Adopt Item
* Bag costs
* Shipping vs carrying comparison tool
