import pybullet as p
import time
import pybullet_data
from pyPS4Controller.controller import Controller
import threading

physicsClient = p.connect(p.GUI)#or p.DIRECT for non-graphical version
p.setAdditionalSearchPath(pybullet_data.getDataPath()) #optionally

p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")
startPos = [0,0,1]

startOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("r2d2.urdf",startPos, startOrientation)
#set the center of mass frame (loadURDF sets base link frame)

# startPos/Ornp.resetBasePositionAndOrientation(boxId, startPos, startOrientation)
p.resetBasePositionAndOrientation(boxId, startPos, startOrientation)

jumlah_joint = p.getNumJoints(boxId)
print("jumlah joint: ")
for i in range(jumlah_joint):
    info = p.getJointInfo(boxId,i)

    indeks = info[0]
    nama = info[1]

    print(f"Indeks: {indeks}, Nama: {nama}")


class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    # def on_triangle_press(self):
    #     p.setJointMotorControl2(
    #         bodyUniqueId=boxId,
    #         jointIndex=13,
    #         controlMode=p.POSITION_CONTROL,
    #         targetPosition = 1.57,
    #         force = 100,
    #         maxVelocity = 5
    #     )
    
    # def on_triangle_release(self):
    #     p.setJointMotorControl2(
    #         bodyUniqueId=boxId,
    #         jointIndex=13,
    #         controlMode=p.POSITION_CONTROL,
    #         targetPosition = 0,
    #         force = 100,
    #         maxVelocity = 5
    #     )

    def on_up_arrow_press(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[-20, -20, -20, -20],
            forces=[10, 10, 10, 10]
        )

    def on_down_arrow_press(self):
            p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[20, 20, 20, 20],
            forces=[100, 100, 100, 100]
        )
       
    def on_left_arrow_press(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[-20, -20, 20, 20],
            forces=[100, 100, 100, 100]
        )

    def on_right_arrow_press(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[20, 20, -20, -20],
            forces=[100, 100, 100, 100]
        )

    def on_left_right_arrow_release(self):
       p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[0, 0, 0, 0],
            forces=[100, 100, 100, 100]
        )    

    def on_up_down_arrow_release(self):
       p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 3, 6, 7],
            controlMode=p.VELOCITY_CONTROL,
            targetVelocities=[0, 0, 0, 0],
            forces=[100, 100, 100, 100]
        )       
       
def PS4Controller():
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

thread_controller = threading.Thread(target = PS4Controller)
thread_controller.daemon = True
thread_controller.start()

# p.resetJointState(
#     bodyUniqueId= boxId,
#     jointIndex = 13,
#     targetValue = 0
# )

# Mengintip batas maksimal dan minimal sendi kepala (Indeks 13)
info_kepala = p.getJointInfo(boxId, 13)
batas_bawah = info_kepala[8]
batas_atas = info_kepala[9]

p.setJointMotorControl2(
    bodyUniqueId=boxId,
    jointIndex=13,
    controlMode=p.POSITION_CONTROL,
    targetPosition = -0.38,
    force = 500,
    maxVelocity = 5
)

for i in range (480):
    p.stepSimulation()
    time.sleep(1/240.)

p.setJointMotorControl2(
    bodyUniqueId=boxId,
    jointIndex=13,
    controlMode=p.POSITION_CONTROL,
    targetPosition = 0,
    force = 500,
    maxVelocity = 5
)

for i in range (240):
    p.stepSimulation()
    time.sleep(1/240.)


print("Intro selesai, masuk ke kendali PS4!")

while True:
    p.stepSimulation()
    time.sleep(1./240.)