import mdl
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [0,
              255,
              255]]
    areflect = [0.1,
                0.1,
                0.1]
    dreflect = [0.5,
                0.5,
                0.5]
    sreflect = [0.5,
                0.5,
                0.5]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 20

    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
        for q in commands:
            if q[0] == 'push':
                stack.append( [x[:] for x in stack[-1]] )
            elif q[0] == 'pop':
		stack.pop()
            elif q[0] == 'display' or q[0] == 'save':
                if q[0] == 'display':
                    display(screen)
                else:
                    save_extension(screen, q[1])
            elif q[0] == 'move':
                t = make_translate(float(q[1]), float(q[2]), float(q[3]))
                w = stack.pop()
                matrix_mult(w, t)
                stack.append(t)
            elif q[0] == 'rotate':
                theta = float(q[2]) * (math.pi / 180)
                if q[1] == 'x':
                    t = make_rotX(theta)
                elif q[1] == 'y':
                    t = make_rotY(theta)
                else:
                    t = make_rotZ(theta)
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]
            elif q[0] == 'scale':
                t = make_scale(float(q[1]), float(q[2]), float(q[3]))
                matrix_mult( stack[-1], t )
                stack[-1] = [ x[:] for x in t]
            elif q[0] == 'box':
                add_box(tmp,
                    float(q[1]), float(q[2]), float(q[3]),
                    float(q[4]), float(q[5]), float(q[6]))
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif q[0] == 'sphere':
                add_sphere(tmp,
                       float(q[1]), float(q[2]), float(q[3]),
                       float(q[4]), step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif q[0] == 'torus':
                add_torus(tmp,
                      float(q[1]), float(q[2]), float(q[3]),
                      float(q[4]), float(q[5]), step_3d)
                matrix_mult( stack[-1], tmp )
                draw_polygons(tmp, screen, zbuffer, view, ambient, light, areflect, dreflect, sreflect)
                tmp = []
            elif q[0] == 'line':
                add_edge( tmp,
                      float(q[1]), float(q[2]), float(q[3]),
                      float(q[4]), float(q[5]), float(q[6]) )
                matrix_mult( stack[-1], tmp )
                draw_lines(tmp, screen, zbuffer, color)
                tmp = []
    else:
        print "Parsing failed."
        return
