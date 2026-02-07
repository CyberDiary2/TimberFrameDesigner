# TimberFrameDesigner
Python application that designs timber frame structures based on user-specified dimensions and snow load requirements. Automatically calculates appropriate member sizes (posts, beams, rafters) using engineering standards and generates interactive 3D visualizations of the structure.


## Quick Start

### 1. Install system dependencies
sudo apt update && sudo apt install python3 python3-venv python3-pip python3-tk -y

### 2. Go to your project directory
cd ~/your/git/directory  

git clone https://github.com/CyberDiary2/TimberFrameDesigner.git  

cd TimberFrameDesigner

### 3. Create virtual environment
python3 -m venv venv

### 4. Activate it  
source venv/bin/activate

### 5. Install packages  
pip install -r requirements.txt


### 6. Run the program  
python timber_frame_designer.py

## Requirements

- Python 3.7+
- NumPy
- Matplotlib
- Tkinter (for GUI display)

## Input Parameters

- Building length and width (10-100 ft)
- Wall height (6-20 ft)
- Roof pitch (2/12 to 16/12)
- Design snow load (5-200 psf)

## Output

- Structural member dimensions
- Number and spacing of timber frame bents
- Material requirements estimate
- Interactive 3D visualization
- Saved PNG image of design

## Disclaimer

This is a preliminary design tool for educational purposes. Always consult a licensed structural engineer and comply with local building codes before construction.

## License

MIT License
