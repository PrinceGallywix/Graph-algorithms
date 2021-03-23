import networkx as nx


def buildNodesMap(paths):
    _map = {}

    for i in range(0, len(paths)):
        _from = paths[i][0]
        _to = paths[i][1]

        if not _from in _map:
            _map[_from] = [[], []]

        if not _to in _map:
            _map[_to] = [[], []]

        _map[_to][0].append(_from)
        _map[_from][1].append(_to)

    for key in _map:
        _map[key][0].sort()
        _map[key][1].sort()

    return _map


def findWeight(paths, first, second, isOriented):
    _found = None

    for e in paths:
        if isOriented:
            if e[0] == first and e[1] == second:
                _found = e
                break
        else:
            if e[0] == first and e[1] == second or e[0] == second and e[1] == first:
                _found = e
                break

    if _found is not None:
        return _found[2]
    else:
        return False


def getNodesList(paths):
    _list = []

    for i in range(0, len(paths)):
        for j in range(0, 2):
            if not paths[i][j] in _list:
                _list.append(paths[i][j])

    return sorted(_list)


def calculateNodesCount(paths):
    return len(getNodesList(paths))


def generateEdgeList(paths):
    _edgelist = []

    for path in paths:
        _edgelist.append((path[0], path[1]))

    return _edgelist


def generateWeightedEdgeList(paths):
    weighted_edgelist = []

    for path in paths:
        weighted_edgelist.append((path[0], path[1], path[2]))

    return weighted_edgelist


def generateEdgeLabels(paths):
    edge_labels = {}

    for j in range(0, len(paths)):
        if paths[j][2] is not None:
            edge_labels[(paths[j][0], paths[j][1])] = paths[j][2]

    return edge_labels


def parseTableItem(item):
    _value = item.text() if item else None

    if _value == "":
        _value = None

    if _value is not None:
        _value = int(_value)

    return _value


def getAdjencyListString(paths, isOriented):
    _map = buildNodesMap(paths)
    _nodes = calculateNodesCount(paths)

    _string = ""

    for _from in _map:
        _arr = []

        if isOriented:
            _arr = _map[_from][1]
        else:
            _arr = _map[_from][0] + _map[_from][1]

        _arr.sort()

        _string += str(_from)

        for _to in _arr:
            _weight = findWeight(paths, _from, _to, isOriented) or " "
            _string += " -> " + "[" + str(_to) + "]" + "[" + str(_weight) + "]"

        _string += " -> [X]\n"

    return _string
