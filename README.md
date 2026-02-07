# TimberFrameDesigner
Python application that designs timber frame structures based on user-specified dimensions and snow load requirements. Automatically calculates appropriate member sizes (posts, beams, rafters) using engineering standards and generates interactive 3D visualizations of the structure.


## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the program
python timber_frame_designer.py
```

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
