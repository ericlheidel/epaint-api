# Welcome to Paintkillerz

(Paintkillerz is currently deployed on my personal portfolio, located [here](https://paintkillerz.eheidel.com))

Paintkillerz is my Full-Stack Capstone from the 6 month Web and Software Development
Boot Camp I completed In May of 2024 at [Nashville Software School](https://nashvillesoftwareschool.com/).

## What is Paintkillerz

This app provides an eCommerce site where artists can purchase professional grade cans of spray paint.

## Table of Contents

- [Features](#features)
- [Deployment](#deployment)
- [Future](#future)

## Features
- Users can Register an account with Paintkillerz (currently disabled for viewing purposes)
- View available paint colors by paint type
  - Search paints by name or paint number
  - Sort paints by paint name or paint number
- Add/remove paints to/from Cart
  - Ability to choose a paint can size and amount
- Add payment method to user account
  - Edit or delete a pre-existing payment method
- Complete an order with a payment method
- User Art
  - Users can upload images of their art (disabled for viewing purposes)
  - Users can view a list of all other users' art

## Deployment
[Paintkillerz](https://paintkillerz.eheidel.com) is currently deployed on my personal portfolio site.
- Virtual machine via a DigitalOcean Droplet running `Ubuntu 24.04.01`
- Frontend Deployment:
  -  ReactJS deployed and built with `npm 9.2.0`
  - `Nginx 1.24.0` is being used as a reverse proxy, is serving the files, and is routing the API requests.
- Backend Deployment:
  - Virtual environment activated with `pipenv 2023.12.1`
  - Django server running with `python 3.12.3`
  Django serving with `gunicorn`
- Database:
  - The database for this project is a bit more simple than the database for my other capstone, [Omg, Shoes...](https://omgshoes.eheidel.com), wheras this database is a `SQPLite3` file.
- SSL/TLS Configuration:
  - `certbot` created my `.pem` files for certification
  - `letsencrypt` to secure my frontend and backend endpoints
  - `nginx` to configure my project to use `HTTPS`

## Future
Now that Paintkillerz is successfully deployed, my next steps will be using TailwindCSS to make the site mobile friendly as well as desktop friendly.

## Thanks for visiting!

<small style="font-size: 0.6em; color: gray;">**Disclaimer:**

This project, including all images, characters, and content, is intended solely
for educational and non-commercial purposes. The use of images and references to
any existing products or pop culture references is intended as a parody and does
not imply any endorsement or affiliation with the respective copyright holders.

All trademarks, images, and characters referenced within this project are the
property of their respective copyright holders. The use of such materials is
protected under the principles of fair use and free speech. No copyright
infringement is intended.

Users of this project should be aware that the project owner does not claim
ownership of any copyrighted materials referenced herein, and no profit is being
made from the distribution or use of this project. </small>
