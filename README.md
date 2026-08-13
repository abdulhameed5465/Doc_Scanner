# Document Scanner (Doc_Scanner)

An interactive, real-time Document Scanner built with Python and OpenCV. This application captures a document image or uses a live video feed, detects the edges of a piece of paper or document, applies a perspective transform to create a top-down bird's-eye view, and applies image processing to make the text clean and readable.

## 🚀 Features
* **Real-time Edge Detection:** Automatic detection of rectangular document contours.
* **Perspective Wrap:** Straightens warped documents into a crisp, flat view.
* **Image Optimization:** Enhances contrast and thresholds the image to mimic a physical hardware scanner output.
* **Live Feed & File Support:** Scalable for static images or live camera processing loops.

## 📂 Repository Structure
* `main.py` - The core application script holding the image processing pipeline, edge detection threshold steps, and perspective warping logic.
* `LICENSE` - Distributed under the open-source MIT License.

## 🛠️ Installation & Setup

Follow these clean configuration steps to set up your local environment and clear potential virtual environment executable errors:

### 1. Clone the Repository
```bash
git clone https://github.com/abdulhameed5465/Doc_Scanner.git
cd Doc_Scanner
```

### 2. Configure a Working Python Virtual Environment
Initialize your local virtual environment using an active, verified base interpreter:
```bash
python -m venv .venv
```

### 3. Activate the Environment
* **On Windows (Command Prompt):**
  ```cmd
  .venv\Scripts\activate.bat
  ```
* **On Windows (PowerShell):**
  ```powershell
  .venv\Scripts\activate.ps1
  ```

### 4. Install Dependencies
Install the standard core computer vision dependencies into your environment to avoid `ModuleNotFoundError` issues:
```bash
pip install opencv-python numpy
```

## 💻 How To Run
Execute the application wrapper from your project directory root:
```bash
python main.py
```

### Key Bindings (Standard OpenCV Controls)
* Press **`q`** or **`Esc`** while focused on the active video stream windows to gracefully shut down the camera stream and close all windows.

## 📝 License
This project is licensed under the terms of the MIT License. See the `LICENSE` file for full details.
