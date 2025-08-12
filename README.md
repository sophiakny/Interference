# Interference Analysis Python Project

This project processes experimental interference data using Fourier transform techniques.  
It includes modules for data analysis, visualization, and hardware control (camera and step motor).

## Project Structure

- `interference.py`

  Main script to run full analysis
- `Fourier_transformer.py`

  Functions for Fourier transform and plotting

- `camera.py`
  
  camera functions
- `Thorlabsmotor.py`

  Controls motor movements
- intencity.txt

  intencity_0808.txt
  
  positions.txt
  
  positions_0808.txt
  
  Experimental datasets

## Installation 
pip install -r requirements.txt

dlls for Thorlab camera and Thorlab step motor 

## Usage 
1. python interference.py
  
   running measurements and creating graphs with results 

2. python Fourier_transformer.py 

   creating graphs using ready data
