
import os
import subprocess

colmap_path = "colmap"
images_folder = "/home/zahid/Downloads/images-fleet-20250204T153120Z-001/images-fleet"
workspace_folder = "/home/zahid/dense/colmap/build"
database_path = os.path.join(workspace_folder, "database.db")
sparse_folder = os.path.join(workspace_folder, "sparse")
dense_folder = os.path.join(workspace_folder, "dense")

#HEADS UP: THIS CODE IS NOT THE CODE I USED FOR THE DENSE RECONSTRUCTION - I USED THE GUI. I WILL UPDATE THIS ON TUESDAY. 

os.makedirs(sparse_folder, exist_ok=True)
os.makedirs(dense_folder, exist_ok=True)


subprocess.run([
    colmap_path, "feature_extractor",
    "--database_path", database_path,
    "--image_path", images_folder,
    "--SiftExtraction.use_gpu", "1"  # Enable GPU for SIFT feature extraction
])


subprocess.run([
    colmap_path, "exhaustive_matcher",
    "--database_path", database_path,
    "--SiftMatching.use_gpu", "1"  # Enable GPU for feature matching
])


subprocess.run([
    colmap_path, "mapper",
    "--database_path", database_path,
    "--image_path", images_folder,
    "--output_path", os.path.join(sparse_folder, "0")  # Ensure correct directory
])



subprocess.run([
    colmap_path, "image_undistorter",
    "--image_path", images_folder,
    "--input_path", os.path.join(sparse_folder, "0"),
    "--output_path", dense_folder
])


subprocess.run([
    colmap_path, "patch_match_stereo",
    "--workspace_path", dense_folder,
    "--workspace_format", "COLMAP",
    "--PatchMatchStereo.geom_consistency", "true",
    "--PatchMatchStereo.gpu_index", "0"  # Use GPU index 0
])


dense_ply_path = os.path.join(dense_folder, "fused.ply")
subprocess.run([
    colmap_path, "stereo_fusion",
    "--workspace_path", dense_folder,
    "--output_path", dense_ply_path
])


print("Sparse and Dense reconstruction complete")

