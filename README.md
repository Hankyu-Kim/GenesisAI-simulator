# Robotics Projects Collection

This repository contains three robotics-related projects implemented simulation tools, and custom components. Each project is organized into its own directory.

## Prerequisites

Follow the command below to install python packages needed in this project.

```bash
conda env create -f genesis_conda.yaml
conda activate genesis_conda
```

## Projects

### 1. Autonomous Driving (Prius URDF)

**Description**:  
A simple autonomous driving setup using a Prius URDF model. The project includes vehicle dynamics, basic control logic, and sensor simulation.

**Features**:
- Prius URDF model
- Basic path following or lane keeping(TO-BE)
- LIDAR and camera simulation (TO-BE)

**Usage**:
```bash
cd workspace
python autonomous_driving.py
```

### 2. Soft Robots (Material research)

**Description**:  
A simple material test given by genesis engine.

**Features**:
- Material 1 : gs.materials.MPM.Muscle
- Material 2 : gs.materials.FEM.Muscle
- Place the above on the height and see the impact and deformation when they hit the ground

**Usage**:
```bash
cd workspace
python soft_robots.py
```

### 3. Robot Arm (Pick & place)

**Description**:  
A simple robot manipulator project that perform 'pick & place'.

**Features**:
- Franka panda model
- PD control
- adjusting parameters(tuning)

**Usage**:
```bash
cd workspace
python robot_arm.py

```

https://github.com/user-attachments/assets/86a97fae-6eda-48d6-84a3-65b13f2fa098
