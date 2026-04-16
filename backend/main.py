import cv2
import processing

filename = '/Users/patriciomartinez/Desktop/Image2Surface/backend/tree_test_img.jpg'
raw_img = cv2.imread(filename)

if raw_img is None:
    raise ValueError("Image not found. Check file path.")

vertices, faces, normals = processing.run_pipeline(raw_img)

processing.save_obj("mesh.obj", vertices, faces)