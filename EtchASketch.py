import cv2
import numpy as np
import matplotlib.pyplot as plt
import PIL.ImageOps
import networkx as nx
import pickle
import PIL
from PIL import Image, ImageFilter
import PIL.ImageOps

def auto_canny(image, sigma=0.33):
    '''
    https://www.pyimagesearch.com/2015/04/06/zero-parameter-automatic-canny-edge-detection-with-python-and-opencv/
    '''
    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)

    # return the edged image
    return edged

def draw(file='tree',size=(0,0),sigma=.33):
    image = cv2.imread('Inputs\\'+file+'.jpg')
    image = cv2.resize(image, size, fx=0.5, fy=0.5)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 0)

    # apply Canny edge detection using a wide threshold, tight
    # threshold, and automatically determined threshold
    wide = cv2.Canny(blurred, 10, 200)
    tight = cv2.Canny(blurred, 225, 250)
    auto = auto_canny(blurred,sigma)

    return auto

def generate_path(file='elephant',sigma=.33):
    edges = 255-draw(file,(256,144),sigma)
    image = PIL.Image.open('Inputs\\' + file + '.jpg')
    image.thumbnail((256, 144), Image.NEAREST)
    simplified = single_line_image(edges)
    img = PIL.Image.fromarray(edges)
    plt.subplot(131)
    plt.imshow(image)
    plt.subplot(132)
    plt.imshow(img, cmap='gray')
    plt.subplot(133)
    plt.imshow(simplified, cmap='gray')
    plt.show()
    PIL.Image.fromarray(simplified).convert('RGBA').save('Previews\\' + file + '.png')
    pp,nn = pa_to_path(file)
    with open('Paths\\' +file+'.p', 'wb') as fp:
        pickle.dump(pp, fp)

def single_line_image(arr):
    x,y = arr.shape
    arr[:,0] = 255
    arr[:,y-2:] = 255
    arr[0,:] = 255
    arr[x-2:,:] = 255
    new_img = np.ones((x, y))*255
    # plt.subplot(121)
    # plt.imshow(arr,cmap='gray')#,cmap='gray')
    imgSimple = arr
    tolerance = 2
    G = nx.Graph()
    for ix in range(x):
        for iy in range(y):
            if imgSimple[ix, iy] == 0:  # then it's black
                # check for other black pixels nearby
                neighbors = []
                for subx in [-2,-1, 0, 1,2]:
                    for suby in [-2,-1, 0, 1, 2]:
                        # below should be fine if we don't draw too close to screen / pad
                        iix = ix + subx
                        iiy = iy + suby

                        if imgSimple[iix, iiy] == 0:
                            #new_img[ix,iy] = arr[ix,iy]
                            G.add_edge((ix, iy), (iix, iiy))
    G = max(nx.connected_component_subgraphs(G), key=len)
    for node in G.nodes:
        new_img[node[0], node[1]] = 0
    return new_img

def load_path(file):
    with open('Paths\\' + file + '.p', 'rb') as myfile:
        data = pickle.load(myfile)
    return data

def pa_to_path(file):
    image = PIL.Image.open('Previews\\' + file + '.png')
    #image = image.rotate(90)
    image_array = np.array(image)
    y,x,z = image_array.shape
    #print(image_array.shape)
    startx,starty = None, None

    # from left, look for first black pixel
    G = nx.Graph()

    imgSimple = image_array.sum(2)
    for ix in range(x):
        for iy in range(y):
            if imgSimple[iy,ix] == 255: # then it's black
                # check for other black pixels nearby
                neighbors = []
                for subx in [-2,-1,0,1,-2]:
                    for suby in [-2,-1,0,1,2]:
                        # below should be fine if we don't draw too close to screen / pad
                        iix = ix + subx
                        iiy = iy + suby

                        if imgSimple[iiy,iix] == 255:
                            G.add_edge((ix, iy), (iix, iiy), weight=((ix - iix) ** 2 + (iy - iiy) ** 2) ** 0.5)

                if startx is None:
                    startx,starty = ix,iy


    print('Starting Location Found: ',startx,starty)
    plt.imshow(image_array)
    plt.plot([startx], [starty], marker='o', markersize=3, color="red")

    path, nodes = dfs_tree_to_etch_path(G,startx,starty)

    x_nodes = [z[0] for z in nodes]
    y_nodes = [z[1] for z in nodes]
    plt.scatter(x=x_nodes,y=y_nodes,s=1.)
    plt.show()
    return path, nodes


def dfs_tree_to_etch_path(G,startx,starty):
    T = nx.dfs_tree(G, (startx, starty))
    #print(T.edges())
    mvmts = []
    nodes = []
    Tedges = T.edges()
    prevte = [None,[z for z in Tedges][0][0]]
    for te in Tedges:
        if te[0] == prevte[1]:
            # the node smoothly connects to the next node
            pass
        else:
            # we need to backtrack first before we can add the movement
            backtrack_start = prevte[1]
            backtrack_end = te[0]
            path_back = nx.shortest_path(G,backtrack_start,backtrack_end)

            for bb in range(len(path_back)-1):
                start_b = path_back[bb]
                dest_b  = path_back[bb+1]
                xdiff_b = dest_b[0] - start_b[0]
                ydiff_b = dest_b[1] - start_b[1]
                mvmts.append((xdiff_b, ydiff_b))
                nodes.append(dest_b)

        start = te[0]
        dest = te[1]
        xdiff = dest[0] - start[0]
        ydiff = dest[1] - start[1]
        mvmts.append((xdiff, ydiff))
        nodes.append(dest)
        prevte = te

    return mvmts, nodes


