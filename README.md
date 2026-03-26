
# 🌌 Solar System Simulator (CW2)

An interactive **3D Solar System Simulator** built using **Python, Pygame, and OpenGL**.
This project visualizes planetary motion, textures, and basic astronomical data with an interactive UI.

---

## 🚀 Features

* 🌍 Real-time simulation of the Solar System
* 🪐 Textured planets with orbital motion
* 🌙 Moon orbiting Earth
* 🎥 Camera movement and zoom controls
* 📊 Interactive UI panel displaying planet information
* 🖱️ Clickable sidebar buttons to focus on planets
* ⏸️ Pause/Resume simulation

---

## 🎮 Controls

| Action         | Control                      |
| -------------- | ---------------------------- |
| Move Camera    | Arrow Keys                   |
| Rotate View    | `W` key                      |
| Zoom In/Out    | Mouse Wheel                  |
| Pause / Resume | Spacebar                     |
| Select Planet  | Click buttons on right panel |
| Quit           | Click "Quit" button          |

---

## 🛠️ Technologies Used

* **Python**
* **Pygame**
* **PyOpenGL**
* **Math (for orbital calculations)**

---

## 📂 Project Structure

```
📁 Solar-System-Simulator
│── main.py
│── README.md
│
├── textures/
│   ├── 2k_sun.jpg
│   ├── 2k_mercury.jpg
│   ├── 2k_venus.jpg
│   ├── 2k_earth.jpg
│   ├── 2k_moon.jpg
│   ├── 2k_mars.jpg
│   ├── 2k_jupiter.jpg
│   ├── 2k_saturn.jpg
│   ├── 2k_uranus.jpg
│   └── 2k_neptune.jpg
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/solar-system-simulator.git
cd solar-system-simulator
```

### 2. Install dependencies

```bash
pip install pygame PyOpenGL PyOpenGL_accelerate
```

### 3. Run the project

```bash
python main.py
```

---

## 🌠 How It Works

* Each planet is represented as a **textured sphere**
* Orbital motion is calculated using **trigonometric rotation formulas**
* OpenGL handles:

  * Rendering
  * Lighting
  * Texture mapping
* UI elements are rendered as **2D textures in 3D space**
* Info panel dynamically updates based on selected planet

---

## 📊 Planet Information Panel

* Displays:

  * Name
  * Type
  * Diameter
  * Distance from Sun
  * Orbital period
  * Additional facts
* Automatically updates when a planet is selected

---

## 🔧 Future Improvements

* 🌌 Add asteroid belts and comets
* 🛰️ Add more moons for other planets
* 🎨 Improve lighting and shaders (Vulkan/OpenGL modern pipeline 👀)
* 🧠 Add AI-based educational assistant
* 🎮 Add free camera mode

---

## 🐞 Known Issues

* Performance may vary on low-end GPUs
* Texture loading may fail if file paths are incorrect
* UI scaling may not adapt to all screen sizes

---
s (since you're doing graphics/VR internship 👀)**
