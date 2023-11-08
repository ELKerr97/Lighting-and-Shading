""" Modified code from Peter Colling Ridge 
	Original found at http://www.petercollingridge.co.uk/pygame-3d-graphics-tutorial
"""

import pygame, math
import numpy as np
import wireframe as wf
import basicShapes as shape

class WireframeViewer(wf.WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    
    def __init__(self, width, height, name="Wireframe Viewer"):
        self.width = width
        self.height = height
        
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(name)
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True
        
        self.perspective = False
        self.eyeX = self.width/2
        self.eyeY = 100
        self.light_color = np.array([1,1,1])
        self.view_vector = np.array([0, 0, -1])        
        self.light_vector = np.array([0, 0, -1])  

        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
        
        self.control = 0
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)
    
    def display(self):
        self.screen.fill(self.background)

        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes
            
            if self.displayFaces:
                for (face, colour) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]

                    normal = np.cross(v1, v2)
                    normal /= np.linalg.norm(normal)
                    towards_us = np.dot(normal, self.view_vector)

                    # Only draw faces that face us
                    if towards_us > 0:
                        m_ambient = 0.1
                        ambient = self.light_color * (m_ambient * colour)

                        #Your lighting code here
                        #Make note of the self.view_vector and self.light_vector 
                        #Use the Phong model

                        # r = 2(l*n)n-l
                        r = 2*(np.dot(self.light_vector, normal))*normal - self.light_vector

                        # Specular Reflection
                        k_s = 0.5 # Specular coefficient
                        k_gls = 5.0 # Glossiness

                        specular_R = k_s * self.light_color[0] * colour[0] * ((np.dot(self.view_vector, r)) ** k_gls)
                        specular_G = k_s * self.light_color[1] * colour[1] * ((np.dot(self.view_vector, r)) ** k_gls)
                        specular_B = k_s * self.light_color[2] * colour[2] * ((np.dot(self.view_vector, r)) ** k_gls)

                        specular_R = np.clip(specular_R, 0, 255)
                        specular_G = np.clip(specular_G, 0, 255)
                        specular_B = np.clip(specular_B, 0, 255)

                        specular_RGB = [specular_R, specular_G, specular_B]

                        # Diffuse Reflection
                        k_d = 0.5 # Diffuse coefficient

                        diffuse_R = k_d * self.light_color[0] * colour[0] * (np.dot(normal, self.light_vector))
                        diffuse_G = k_d * self.light_color[1] * colour[1] * (np.dot(normal, self.light_vector))
                        diffuse_B = k_d * self.light_color[2] * colour[2] * (np.dot(normal, self.light_vector))

                        diffuse_R = np.clip(diffuse_R, 0, 255)
                        diffuse_G = np.clip(diffuse_G, 0, 255)
                        diffuse_B = np.clip(diffuse_B, 0, 255)

                        diffuse_RGB = [diffuse_R, diffuse_G, diffuse_B]

						#Once you have implemented diffuse and specular lighting, you will want to include them here
                        light_total = ambient + specular_RGB + diffuse_RGB

                        pygame.draw.polygon(self.screen, light_total, [(nodes[node][0], nodes[node][1]) for node in face], 0)

                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective/ (self.perspective + nodes[n1][2])
                                x1 = self.width/2  + z1*(nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1*(nodes[n1][1] - self.height/2)
                    
                                z2 = self.perspective/ (self.perspective + nodes[n2][2])
                                x2 = self.width/2  + z2*(nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2*(nodes[n2][1] - self.height/2)
                                
                                pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(self.screen, colour, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        pygame.display.flip()

    def keyEvent(self, key):
        
        #Your code here
        # Rotate up (around x-axis)
        if key == pygame.K_w:
            print("w is pressed")

        # Rotate down (around x-axis)
        if key == pygame.K_s:
            print("s is pressed")

        # Rotate left (around y-axis)
        if key == pygame.K_a:
            print("a is pressed")

        # Rotate right (around y-asix)
        if key == pygame.K_d:
            print("d is pressed")

        # Rotate ccw (around z-axis)
        if key == pygame.K_q:
            print("q is pressed")

        # Rotate cw (around z-axis)
        if key == pygame.K_e:
            print("e is pressed")







        return

    def run(self):
        """ Display wireframe on screen and respond to keydown events """
        
        running = True
        key_down = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    key_down = event.key
                elif event.type == pygame.KEYUP:
                    key_down = None
            
            if key_down:
                self.keyEvent(key_down)
            
            self.display()
            self.update()
            
        pygame.quit()

		
resolution = 52
viewer = WireframeViewer(600, 400)
viewer.addWireframe('sphere', shape.Spheroid((300,200, 20), (160,160,160), resolution=resolution))

# Colour ball
faces = viewer.wireframes['sphere'].faces
for i in range(int(resolution/4)):
	for j in range(resolution*2-4):
		f = i*(resolution*4-8) +j
		faces[f][1][1] = 0
		faces[f][1][2] = 0
	
viewer.displayEdges = False
viewer.run()