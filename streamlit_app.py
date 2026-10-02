import streamlit as st
import trimesh
import os

st.title("3D STL Hollow Tool")
st.write("Apni STL file upload karke hollow karein.")

uploaded_file = st.file_uploader("STL File Upload Karein", type=["stl"])
thickness = st.slider("Metal Thickness (mm)", min_value=0.3, max_value=2.0, value=0.6, step=0.1)

if uploaded_file is not None:
    if st.button("Hollow STL Banayein"):
        st.info("File process ho rahi hai...")
        with open("input.stl", "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        try:
            mesh = trimesh.load("input.stl", file_type='stl')
            if not mesh.is_watertight:
                mesh.fill_holes()
                
            inner_mesh = mesh.copy()
            inner_mesh.vertices -= inner_mesh.vertex_normals * thickness
            inner_mesh.invert()
            
            hollow_mesh = trimesh.util.concatenate([mesh, inner_mesh])
            output_path = "hollow_output.stl"
            hollow_mesh.export(output_path)
            
            st.success("Aapki Hollow STL File Ready Hai!")
            with open(output_path, "rb") as file:
                st.download_button("Download Hollow STL", data=file, file_name="Hollow_Model.stl", mime="model/stl")
        except Exception as e:
            st.error(f"Error: {str(e)}")
