# goodai-webpage
---
Single page [webapp](http://16.16.67.70/)  for GoodAI. Rendering of three 3D shapes whose size is changed randomly at a frequency set by the user.
The frontend is coded using the Svelte framework, and the backend is a websocket server using aiohttp and asyncio in Python.
The app is deployed on AWS using Gunicorn, Nginx and Supervisor.

### **Test System: Ubuntu 20.04, Node.js v20.9.0, Python 3.8.10**
Author: Miguel Garcia Naude

---

## Instructions for running locally
Before installing and running locally please ensure that you have node.js installed and npm configured. 
For svelte to run, it is required that at least node.js version 16 is installed. Installation instructions can be found [here](https://nodejs.org/en/download/package-manager).

### 1. Clone and Build
Clone this repository into a directory.
```bash
git clone https://github.com/migsdigs/goodai-webpage.git
cd goodai-webpage
```

### 2. Install dependencies
First install the dependencies for the aiohttp python asynchronous websocket server.
```bash
cd webapp
pip install -r requirements.txt
```

Second, install the npm dependencies for the svelte app.
```bash
cd ..
cd svelte-3d
npm install
```

### 3. Create .env file to hold URL address envirnonment variable
For security reasons, a `.env` file is normally not commited to repos, but should rather be created.
```bash
cd svelte-3d
nano .env
```

Inside of nano, add the following:
```
URL=ws://0.0.0.0:8080/ws # Save the file and exit
```

### 4. Running the local websocket server
Run the server script.
```bash
cd ..
cd webapp
python server.py  # or: python3 server.py
```

You should receive the following response:
```bash
======== Running on http://0.0.0.0:8080 ========
```

### 5. Running the app
In a separate terminal.
```bash
cd svelte-3d
npm run dev
```

Which should produce the following (or similar):
```bash
> svelte-app@1.0.0 dev
> rollup -c -w

rollup v3.29.4
bundles src/main.js → public/build/bundle.js...
LiveReload enabled
created public/build/bundle.js in 5.7s

[2023-11-22 00:49:55] waiting for changes...

> svelte-app@1.0.0 start
> sirv public --no-clear --dev


  Your application is ready~! 🚀

  ➡ Port 8080 is taken; using 42419 instead

  - Local:      http://localhost:42419
  - Network:    Add `--host` to expose
```

Your machine should realise that port 8080 is taken by your websocket server and should provide a different port.

### 6. Open in Browser
Open the link given `http://localhost:42419` in your browser.

You should see something similar to below. The shapes should be changing size at the frequency shown in the input, which you can change yourself.
<img src="https://github.com/migsdigs/goodai-webpage/blob/main/assets/webpage" alt="webpage" height="400"/>
