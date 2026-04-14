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
boxId = p.loadURDF("Hexapodv2.urdf",startPos, startOrientation)


joint = p.getNumJoints(boxId)
# print("Jumlah joint: ")
# for i in range (joint):
#     info = p.getJointInfo(boxId, i)
#     indeks = info[0]
#     nama = info[1].decode("utf-8")
#     tipe_joint = info[2]

    

#     print(f"Indeks: {indeks}, nama: {nama}")



# p.resetJointState(
#     bodyUniqueId= boxId,
#     jointIndex = 2,
#     targetValue = 1.5
# )
triangle_press = False
circle_press = False
p.changeVisualShape(
    objectUniqueId=boxId,
    linkIndex= 0,
    rgbaColor=[1, 0, 0, 1] 
)

p.changeVisualShape(
    objectUniqueId=boxId,
    linkIndex= 1,
    rgbaColor=[88/255, 120/255, 198/255, 1] 
)

p.changeVisualShape(
    objectUniqueId=boxId,
    linkIndex= 2,
    rgbaColor=[100/255, 198/255, 88/255, 0.8] 
)

print("Berhasil memuat robot!")

class MyController(Controller):
    def __init__ (self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_triangle_press(self):
        global triangle_press
        triangle_press = True


    
    def on_triangle_release(self):
        global triangle_press
        triangle_press = False



    def on_circle_press(self):
        global circle_press
        circle_press = True

    def on_circle_release(self):
        global circle_press
        circle_press = False
    


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
sudut_sekarang = 0

while True:
    if triangle_press:
        target_sudut = -1.5
    elif circle_press:
        target_sudut = 1.5
    else:
        target_sudut = 0
    
    if sudut_sekarang > target_sudut:
        sudut_sekarang -= 0.01
        sudut_sekarang = max(sudut_sekarang, target_sudut)

    elif sudut_sekarang < target_sudut:
        sudut_sekarang += 0.01
        sudut_sekarang = min(sudut_sekarang, target_sudut)

            
        # Tembakkan ke motor (Indeks 0)
    p.setJointMotorControl2(
        bodyUniqueId=boxId,
        jointIndex=0,
        controlMode=p.POSITION_CONTROL,
        targetPosition=sudut_sekarang,
        force=500
    )

    p.setJointMotorControl2(
        bodyUniqueId=boxId,
        jointIndex=1,
        controlMode=p.POSITION_CONTROL,
        targetPosition=sudut_sekarang,
        force=500
    )

    p.setJointMotorControl2(
        bodyUniqueId=boxId,
        jointIndex=2,
        controlMode=p.POSITION_CONTROL,
        targetPosition=sudut_sekarang,
        force=500
    )

    p.stepSimulation()
    time.sleep(1./240.)