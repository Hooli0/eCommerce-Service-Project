# eCommerce Service Project

A Quasar Framework app
This project is inspired by the E-commerce project provided by COMP3900.<br />
Typical E-commerce features are present such as buying/selling items. <br />

The website is split into two modules, an Admin module and User module.<br />
The Admin module is able to list/update items and view sales history.<br />
The User module is for general usage such as buying/browsing. <br />
This project's novel features include a daily coupon reward system and SM integration. <br />
(For the development build, the coupon refresh rate is set to 5 seconds rather than 24 hours. This makes testing and demonstration much easier.)<br />
<br />
The following install instructions are optimised for the CSE Linux environment. <br />


## Update Node.js
Quasar requires Node.js to be >= v12.22.1. 
It is reccomended to update node following the tutorial on https://linuxbuz.com/linuxhowto/update-node-version using NVM.
The development build was tested on node v14.15.4
The relevent commands are as follows: 
```bash
apt-get update -y
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
nvm install v14.15.4

```

### Install frontend dependencies
```bash
npm install
```

### Install backend dependencies 
```bash
pip3 install -r requirements.txt
```

### Start the backend server
If you are in the main capstone-project-3900-w18a-chatbot directory:
```bash
python3 "backend/server.py"
```
Or you can also go to the backend directory from the main directory and run:
```bash
python3 "server.py"
```

### Start the frontend
```bash
npm start
```
