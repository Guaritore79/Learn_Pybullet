import pybullet as p
import time 
import pybullet_data
from pyPS4Controller.controller import Controller
import threading

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-10)
planeId = p.loadURDF("plane.urdf")

startPos = [0,0,1]
startOrientation = p.getQuaternionFromEuler([0,0,0])
boxId = p.loadURDF("Hexapod.urdf",startPos, startOrientation)

joint = p.getNumJoints(boxId)
print("Jumlah joint: ")
for i in range (joint):
    info = p.getJointInfo(boxId, i)
    indeks = info[0]
    nama = info[1].decode("utf-8")
    tipe_joint = info[2]
    

    print(f"Indeks: {indeks}, nama: {nama}")

# p.resetJointState(
#     bodyUniqueId= boxId,
#     jointIndex = 2,
#     targetValue = 1.5
# )

p.changeVisualShape(
    objectUniqueId=boxId,
    linkIndex= 3,
    rgbaColor=[1, 0, 0, 1] 
)

p.changeVisualShape(
    objectUniqueId=boxId,
    linkIndex= 6,
    rgbaColor=[1, 0, 0, 1] 
)

print("Berhasil memuat robot!")

class MyController(Controller):
    def __init__ (self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_triangle_press(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 5, 8, 11, 14, 17],
            controlMode=p.POSITION_CONTROL,
            targetPositions=[1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
            forces=[500, 500, 500, 500, 500, 500],
            # maxVelocities=[5, 5, 5, 5, 5, 5]
        )
    
    def on_triangle_release(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[2, 5, 8, 11, 14, 17],
            controlMode=p.POSITION_CONTROL,
            targetPositions=[0, 0, 0, 0, 0, 0],
            forces=[500, 500, 500, 500, 500, 500],
            # maxVelocities=[5, 5, 5, 5, 5, 5]
        )

    def on_circle_press(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[0, 3, 6, 9, 12, 15],
            controlMode=p.POSITION_CONTROL,
            targetPositions=[1.5, 1.5, 1.5, 1.5, 1.5, 1.5],
            forces=[500, 500, 500, 500, 500, 500],
            # maxVelocities=[5, 5, 5, 5, 5, 5]
        )

    def on_circle_release(self):
        p.setJointMotorControlArray(
            bodyUniqueId=boxId,
            jointIndices=[0, 3, 6, 9, 12, 15],
            controlMode=p.POSITION_CONTROL,
            targetPositions=[0, 0, 0, 0, 0, 0],
            forces=[500, 500, 500, 500, 500, 500],
            # maxVelocities=[5, 5, 5, 5, 5, 5]
        )
    


def PS4Controller():
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)

thread_controller = threading.Thread(target = PS4Controller)
thread_controller.daemon = True
thread_controller.start()

for i in range(joint):
    limit = p.getJointInfo(boxId, i)
    batas_bawah = limit[8]
    batas_atas = limit[9]
    indeks = limit[0]
    jenis = limit[1].decode("utf-8")

    print(f"indeks : {indeks}, Batas atas : {batas_atas}, Batas bawah : {batas_bawah}, Jenis : {jenis}")

while True:
    p.stepSimulation()
    time.sleep(1./240.)