import pyrealsense2 as rs
import numpy as np
import cv2


# ストリーム(IR/Color/Depth)の設定
config = rs.config()

config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
#config.enable_stream(rs.stream.infrared, 2, 640, 480, rs.format.y8, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
#config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 15)

# ストリーミング開始
pipeline = rs.pipeline()
profile = pipeline.start(config)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,480))

try:
    i = 0
    while True:
        # フレーム待ち
        frames = pipeline.wait_for_frames()

        #IR1
        ir_frame1 = frames.get_infrared_frame(1)
        ir_image1 = np.asanyarray(ir_frame1.get_data())
        #ir_color_image = np.zeros((480, 640, 3))

        # RGB
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())

        # IR -> RGB
        #for h in range(0, 640):
        #    for v in range(0, 480):
        #        color_image[v, h, 0] = ir_image1[v, h]
        #        color_image[v, h, 1] = ir_image1[v, h]
        #        color_image[v, h, 2] = ir_image1[v, h]



        # write the flipped frame
        #out.write(ir_image1)
        #out.write(ir_color_image)
        out.write(color_image)
        
        # 表示
        cv2.namedWindow('RealSense-Color', cv2.WINDOW_AUTOSIZE)
        #cv2.namedWindow('RealSense-IR', cv2.WINDOW_AUTOSIZE)

        cv2.imshow('RealSense-Color', color_image)
        #cv2.imshow('RealSense-IR', ir_image1)

        if cv2.waitKey(1) & 0xff == 27:
            out.release()
            cv2.destroyAllWindows()
            break

finally:
    # ストリーミング停止
    pipeline.stop()