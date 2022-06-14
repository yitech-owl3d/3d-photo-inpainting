import trimesh
import json


def convert_to_trimesh(vertices, faces, vertex_colors=None):
    mesh = trimesh.Trimesh(vertices=vertices,
                           faces=faces,
                           vertex_colors=vertex_colors)
    return mesh


def convert_to_texture_trimesh(vertices, faces, uvs, image):
    texture = trimesh.visual.texture.TextureVisuals(uv=uvs, image=image)
    mesh = trimesh.Trimesh(vertices=vertices,
                           faces=faces,
                           visual=texture)
    return mesh


def write_glb(file_dst, geometry):
    with open(file_dst, 'wb') as glb:
        glb.write(trimesh.exchange.export.export_glb(geometry))


if __name__ == '__main__':
    # mesh objects can be created from existing faces and vertex data
    mesh = trimesh.Trimesh(vertices=[[0, 0, 0], [0, 0, 1], [0, 1, 0]],
                           faces=[[0, 1, 2]])


    write_glb('tri.glb', mesh)