# plexLocationBlock
 Block Plex streams via location. Can block by city, state or add users to allow the user to override a block.
 The script will automatically kill any stream that tries too start in a blocked location.

Requirements:
* Python 3
* Tautulli v2.5.2 or newer to run Python 3 or configure older versions to run Python 3)

# How to Setup - Windows
* Download the script [Plex Location Block](https://github.com/primetime43/plexLocationBlock/blob/master/plexLocationBlock.pyw) and place it anywhere locally on your machine
* In [Tautulli](https://github.com/Tautulli/Tautulli) go to Settings and then Notification Agents
![image](https://user-images.githubusercontent.com/12754111/174919786-16e09543-3d98-4d72-8762-2c0d1a430242.png)
* Once in the above location, select add Add a new notification agent and scroll down to script in the list
![image](https://user-images.githubusercontent.com/12754111/174920096-be992718-a58a-475c-b558-e1b749312e82.png)
* There you select where the script you downloaded in step 1 is located on your machine and set up like so
![image](https://user-images.githubusercontent.com/12754111/174920199-f9c011d1-e949-4945-89de-331a3f54d3fd.png)
* Then the only other setting you need to set is on the Triggers tab. Check the Playback Start trigger and click save
![image](https://user-images.githubusercontent.com/12754111/174920310-04d11896-e4ca-4dfe-b3b2-d70980a0c8be.png)

# How to Use the Script
* Once you have the above completed and set-up, you can modify the script to your needs (use notepad++ or whatever you prefer)
* The only changes to the script that are needed are at the top on lines 8-10 (nothing else needs modified)
The locationsToBlock array currently accepts cities and states to block, but allows users to override blocks. Users can be added when you want to block a state, but want to allow a certain user in that state to be allowed to watch (may add more specific locations later)
locationsToBlock
```python
locationsToBlock = ["Florida", "Pennsylvania", "Los Angeles", "Houston"]
```
locationsToAllow
```python
locationsToAllow = ["New York"]
```
usersToAllow
```python
usersToAllow = ['test1', 'userNameEx']  # used to override locations
```
![image](https://user-images.githubusercontent.com/12754111/174920583-4ff3bb22-89b1-4b58-8173-defbabf4b6fd.png)
