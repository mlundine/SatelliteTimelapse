# tensorflow_app

**Satellite Timelapse GUI**

**By: Mark Lundine**

**1: Setting Up with Anaconda**

Download this repository.

Open up terminal (mac) or Anaconda prompt (windows).

Run these commands:

cd where_you_placed_it/satellitetimelapse

conda env create --file environment.yml

This will download all the required packages.

Then run:

conda activate satvid

earthengine authenticate

This will pull up a browser and ask you to log in to your google account and authenticate Google Earth Engine.

Once your earth engine account is authenticated, this gui can be used.

To run the gui, type in the command prompt:

python satgui.py



