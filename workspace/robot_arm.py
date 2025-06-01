import numpy as np
import genesis as gs

########################## init ##########################
gs.init(backend=gs.gpu)

########################## create a scene ##########################
scene = gs.Scene(
    show_viewer = True,
    viewer_options = gs.options.ViewerOptions(
        camera_pos    = (2.5, 1.5, 2.5),
        camera_lookat = (0.0, 0.0, 0.5),
        camera_fov    = 30,
        res           = (960, 640),
        max_FPS       = 60,
    ),
    sim_options = gs.options.SimOptions(
        dt = 0.01,
        gravity=(0, 0, -9.8),
    ),
)

########################## entities ##########################
plane = scene.add_entity(
    gs.morphs.Plane(),
)
franka = scene.add_entity(
    gs.morphs.MJCF(
        file  = 'xml/franka_emika_panda/panda.xml',
    ),
)
object = scene.add_entity(
    morph=gs.morphs.Box(
        pos    = (0.5, 0.5, 0.0),
        size   = (0.1, 0.1, 0.1),
        euler  = (0.0, 0.0, 0.0), 
    ),
    # material=gs.materials.Rigid(
    #     gravity_compensation=1.0,
    # ),
)

cam = scene.add_camera(
    res    = (640, 480),
    pos    = (2.5, 1.5, 2.5),
    lookat = (0, 0, 0.5),
    fov    = 30,
    GUI    = False,
)
########################## build ##########################
scene.build()

jnt_names = [
    'joint1',
    'joint2',
    'joint3',
    'joint4',
    'joint5',
    'joint6',
    'joint7',
    'finger_joint1',
    'finger_joint2',
]
dofs_idx = [franka.get_joint(name).dof_idx_local for name in jnt_names]

############ Optional: set control gains ############
# set positional gains
franka.set_dofs_kp(
    kp             = np.array([4500, 2250, 3500, 3500, 2000, 1000, 1000, 1, 1]),
    dofs_idx_local = dofs_idx,
)
# set velocity gains
franka.set_dofs_kv(
    kv             = np.array([450, 450, 350, 350, 200, 200, 200, 10, 10]),
    dofs_idx_local = dofs_idx,
)
# set force range for safety
franka.set_dofs_force_range(
    lower          = np.array([-87, -87, -87, -87, -12, -12, -12, -100, -100]),
    upper          = np.array([ 87,  87,  87,  87,  12,  12,  12,  100,  100]),
    dofs_idx_local = dofs_idx,
)

# [yaw, 1, 2, 3, 4, 5, 6, finger1, finger2] finger with negative value = pick, finger with positive value = release

# franka.set_dofs_position(
#     np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]),
#     dofs_idx,
# )
# scene.step()

# cam.start_recording()

for i in range(2250):
    if i == 0:
        franka.control_dofs_position(
            np.array([0, 0, 0, 0, 0, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 250:
        franka.control_dofs_position(
            np.array([1, 0, 0, 0, 0, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 500:
        franka.control_dofs_position(
            np.array([1, 1, 0, 0, 0, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 750:
        franka.control_dofs_position(
            np.array([1, 1, 1, 0, 0, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 1000:
        franka.control_dofs_position(
            np.array([1, 1, 1, -1, 0, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 1250:
        franka.control_dofs_position(
            np.array([1, 1, 1, -1, 1, 0, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 1500:
        franka.control_dofs_position(
            np.array([1, 1, 1, -1, 1, 1, 0, 1, 1]),
            dofs_idx,
        )
    elif i == 1750:
        franka.control_dofs_position(
            np.array([1, 1, 1, -1, 1, 1, 1, 1, 1]),
            dofs_idx,
        )
    elif i == 2000:
        franka.control_dofs_position(
            np.array([1, 1, 1, -1, 1, 1, 1, -1, -1]),
            dofs_idx,
        )

    # print('control force:', franka.get_dofs_control_force(dofs_idx))
    # print('internal force:', franka.get_dofs_force(dofs_idx))
    # print(i // 250, 'th axis is moving')    

    scene.step()
#     cam.set_pose(
#         pos = (3.0 * np.sin(i / 250), 3.0 * np.cos(i / 250), 2.5),
#         lookat   = (0.0, 0.0, 0.5),
#     )
#     cam.render()
# cam.stop_recording(save_to_filename='video.mp4', fps=60)