A college campus-centric market place that will allow students to buy and sell goods over the web. 

This application is built with the django framework for a College Course Final Project

Setup Instruction:

1. Open a terminal window and run git clone https://github.com/danieldelgado3/ninerExchange_ITSC3155
2. Once cloned open a terminal for the repo and create a virtual environment named venv: python3 -m venv venv
3. Activate the virtual environment using : source venv/bin/activate
4. After activating the virtual environment download all dependencies in the requirements.txt using the terminal 
5. Create a .env file in the directory that contains:
  CLOUDINARY_CLOUD_NAME="dm1hmegmg"
  CLOUDINARY_API_KEY="894683478223129"
  CLOUDINARY_API_SECRET="XY15925mPL4LqJe9tG-pVSNqCCo"
6. Open a terminal on the ninerMarket folder and run python manage.py runserver
7. The app should now be running and the terminal will tell you the server number in order to access the app


