import trimesh
import cv2
import numpy as np
import json


class InpaintingTexture:
    def __init__(self, H, W):
        self.texture = np.zeros(shape=(H, W, 3), dtype=np.uint8)
        self.metadata = []
        self.n_images = 0
        self._start_pos_x = 0
        self._start_pos_y = 0
        self._row = 0
        self._col = 0
        self._right = 0
        self._bottom = 0

    def add(self, image):
        h, w, c = self.texture.shape
        in_h, in_w, in_c = image.shape
        # check if image can be added next to prev
        if self._start_pos_x + in_w > w:
            self._start_pos_x = 0
            self._start_pos_y = self._bottom
            self._col = 0
            self._row += 1
        if self._start_pos_y + in_h > h:
            # self.texture = np.zeros(shape=(2 * h, 2 * w, c), dtype=np.uint8)
            KeyError(f"self.texture has no buffer.")
        self.texture[self._start_pos_y: self._start_pos_y + in_h, self._start_pos_x: self._start_pos_x + in_w] = image
        self.metadata.append({'texture_id': self.n_images,
                              'start_y': self._start_pos_y,
                              'start_x': self._start_pos_x,
                              'y_offset': in_h,
                              'x_offset': in_w})
        self.n_images += 1
        self._col += 1
        self._right = max(self._right, self._start_pos_x + in_w)
        self._bottom = max(self._bottom, self._start_pos_y + in_h)
        self._start_pos_x += in_w

    def write(self, filename):
        cv2.imwrite(filename, self.texture)
        return


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
    # inpaint = InpaintingTexture(2048, 2048)
    # img = cv2.imread('image/0aad054556200b9afaf8a7f5edb03d4e.jpg')
    # np.random.seed(819)
    # for i in range(40):
    #     size_x, size_y = np.random.randint(200, 300, 2)
    #     test = cv2.resize(img, (size_x, size_y))
    #     inpaint.add(test)
    # inpaint.write("test.png")
