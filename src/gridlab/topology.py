"""Topology diagnostics independent of numerical matrix conditioning."""
def islands(nbus, lines):
    neighbors = [set() for _ in range(nbus)]
    for line in lines:
        if line.enabled:
            neighbors[line.start].add(line.end)
            neighbors[line.end].add(line.start)
    unseen, result = set(range(nbus)), []
    while unseen:
        stack, component = [min(unseen)], set()
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(neighbors[node]-component)
        unseen -= component
        result.append(tuple(sorted(component)))
    return result

def unpowered_islands(nbus, lines, source_buses):
    sources = set(source_buses)
    return [group for group in islands(nbus, lines) if not sources.intersection(group)]
