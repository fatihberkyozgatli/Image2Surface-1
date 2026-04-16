import cv2
import processing

filename = '../assets/images/tree_test_img.jpg'
output_path = '../outputs/mesh.obj'

raw_img = cv2.imread(filename)

if raw_img is None:
    raise ValueError("Image not found.")

vertices, faces, normals = processing.run_pipeline(raw_img)

processing.save_obj(output_path, vertices, faces)