import numpy as np
import genesis as gs

# Initialize Genesis with GPU backend
gs.init(backend=gs.gpu)

# Create the simulation scene
scene = gs.Scene(
    viewer_options=gs.options.ViewerOptions(
        camera_pos=(10, 5, 2),
        camera_lookat=(0.0, 0.0, 0.5),
        camera_fov=60,
        res=(960, 640),
        max_FPS=30,
    ),
    sim_options=gs.options.SimOptions(dt=0.01),
    show_viewer=True,
)

# Add a ground plane and the Prius URDF model
scene.add_entity(gs.morphs.Plane())
prius = scene.add_entity(
    morph=gs.morphs.URDF(
        file="urdf/prius_description/urdf/prius.urdf",
        pos=(0.0, 0.0, 0.0),
        euler=(0.0, 0.0, 0.0),
        scale=1.0,
        fixed=False,
    ),
    # material=gs.materials.Hybrid(
    #     mat_rigid=gs.materials.Rigid(
    #         gravity_compensation=1.,
    #     ),
    #     mat_soft=gs.materials.MPM.Muscle( # to allow setting group
    #         E=1e4,
    #         nu=0.45,
    #         rho=1000.,
    #         model='neohooken',
    #     ),
    #     thickness=0.05,
    #     damping=1000.,
    #     func_instantiate_rigid_from_soft=None,
    #     func_instantiate_soft_from_rigid=None,
    #     func_instantiate_rigid_soft_association=None,
    # ),
)

# Build the scene
scene.build()

# Define joint names for steering
steering_joints = [
    'steering_joint',
    'front_left_steer_joint',
    'front_right_steer_joint',
]

# Define wheel joint names
wheels_joints = [
    'front_left_wheel_joint',
    'front_right_wheel_joint'
]

# Get DOF indices
steering_dofs_idx = [prius.get_joint(name).dof_idx_local for name in steering_joints]
wheel_dofs_idx = [prius.get_joint(name).dof_idx_local for name in wheels_joints]

# Set steering joints to 0.5 radians
prius.set_dofs_position(np.array([0.5, 0.5, 0.5]), steering_dofs_idx)

# Set control gains for velocity control (tune as needed)
prius.set_dofs_kp(kp=np.array([0, 0]), dofs_idx_local=wheel_dofs_idx)  # Zero positional gains for pure velocity control
prius.set_dofs_kv(kv=np.array([50, 50]), dofs_idx_local=wheel_dofs_idx)  # Damping for smooth velocity control

# Apply constant velocity to front wheels (positive values move forward)
velocity_command = np.array([30.0, 30.0])  # Adjust speed (rad/s)

# Simulation loop
for _ in range(1500):
    # Apply velocity to the front wheels continuously
    prius.control_dofs_velocity(velocity_command, wheel_dofs_idx)

    # Optional: Debugging forces and velocities
    current_velocity = prius.get_dofs_velocity(wheel_dofs_idx)
    print(f"Wheel Velocities: {current_velocity}")

    # Step the simulation
    scene.step()
