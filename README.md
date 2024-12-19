# Iris Project

## Overview
The Iris Project is a graphical Python application designed to calculate the distance and velocity of a planet in relation to Earth based on user-specified time intervals. The project leverages Python libraries for astronomical calculations, graphical interface creation, and multimedia playback to provide an engaging user experience.

## Features
- Select planets in the solar system from a graphical interface.
- Input time intervals to calculate:
  - The distance between Earth and the selected planet.
  - The velocity of the planet relative to Earth.
- Display results dynamically on the interface.
- Play background music during the application's runtime.
- Graphical elements include:
  - Background image.
  - Planet icons and names.
  - Styled input and output sections.

## Requirements
### Python Dependencies
Install the required Python libraries using pip:

```bash
pip install pygame tk pillow astropy
```

### Files and Resources
Ensure the following file structure:

```
project_directory/
|-- iris.py
|-- images/
|   |-- background.png
|   |-- mercury.png
|   |-- venus.png
|   |-- earth.png
|   |-- mars.png
|   |-- jupiter.png
|   |-- saturn.png
|   |-- uranus.png
|   |-- neptune.png
|-- background_music/
    |-- your_music_file.mp3
```

## Running the Project

### In Development Environment
Run the application using:

```bash
python iris.py
```

### Creating an Executable
To distribute the project as a standalone executable, use PyInstaller:

```bash
pyinstaller --onefile --windowed \
  --add-data "images/*;images/" \
  --add-data "background_music/*;background_music/" \
  iris.py
```

The resulting executable will be located in the `dist` folder.

### Note
When distributing the executable, ensure all required resources (`images` and `background_music`) are correctly bundled by PyInstaller.

## Usage
1. Launch the application.
2. Select a planet from the graphical interface.
3. Input the initial and final times in the format `YYYY-MM-DD HH:MM:SS`.
4. View the calculated distance and velocity.
5. Enjoy the background music!

## Customization
### Changing Background Music
Replace the file in `background_music/your_music_file.mp3` with your desired MP3 file, ensuring the file path is updated in `iris.py`:

```python
pygame.mixer.music.load(resource_path('background_music/your_music_file.mp3'))
```

### Updating Images
Replace the images in the `images/` folder with your own, maintaining the same naming convention.

## License
This project is open-source and free to use for educational and personal purposes.

## Author
**Arthur Clemente Machado**  
Version: 0.1  
Date: 19/12/2024
