

def get_neighbours(i, w, h):
    """
    Get the list of indexes for neighbours of i,j
    in a w x h lattice (toroidal boundaries) but where
    each is given a single index in a list i.e.

    9 elts:

    0 1 2
    3 4 5
    6 7 8

    neighbours of i=4 (i.e. 5th el.) are:
    [0,1,2,3,5,6,7,8]
    """

    def xy_to_i(coords):
        return w * coords[1] + coords[0]

    def i_to_xy(i):
        return i % w, i / w

    # up    = j > 0 ? j - 1 : @height - 1
    #     down  = j < @height - 1 ? j + 1 : 0
    #     right = i < @width -1 ? i + 1 : 0
    #     left  = i > 0 ? i -1 : @width -1
    #
    #     [@array[right][up],
    #      @array[right][j],
    #      @array[right][down],
    #      @array[i][down], @array[left][down], @array[left][j],
    #      @array[left][up],
    #      @array[i][up]]

    x,y = i_to_xy(i)

    #print "x: %d, y: %d" % (x,y)

    if y > 0:
        up = y - 1
    else:
        up = h - 1

    if y < h - 1:
        down = y + 1
    else:
        down = 0

    if x > 0:
        left = x - 1
    else:
        left = w - 1

    if x < w - 1:
        right = x + 1
    else:
        right = 0

    #print "up: %d, down: %d, left: %d, right: %d" % (up, down, left, right)

    return(map(xy_to_i, [(left, up), (x, up), (right, up), (left, y), (right, y),
                         (left, down), (x, down), (right, down)]
    ))