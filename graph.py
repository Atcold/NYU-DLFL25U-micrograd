from graphviz import Digraph

__all__ = [
    'draw_dot'
]


def trace(root):
    nodes, edges = set(), set()
    def build(v):
        if v not in nodes:
            nodes.add(v)
            for child in v._prev:
                edges.add((child, v))
                build(child)
    build(root)
    return nodes, edges

def draw_dot(root, format='svg', rankdir='LR'):
    """
    format: png | svg | ...
    rankdir: TB (top to bottom graph) | LR (left to right)
    """
    assert rankdir in ['LR', 'TB']
    nodes, edges = trace(root)
    dot = Digraph(format=format, graph_attr={'rankdir': rankdir}) #, node_attr={'rankdir': 'TB'})

    # Set background color for the entire graph
    dot.graph_attr['bgcolor'] = '#282C35'  # Dark background

    # Set default attributes for nodes
    dot.node_attr['fontcolor'] = '#e6e6e6'  # Light font color
    dot.node_attr['style'] = 'filled'
    dot.node_attr['color'] = '#e6e6e6'  # Light border color
    dot.node_attr['fillcolor'] = '#333333' # Dark fill color for nodes

    # Set default attributes for edges
    dot.edge_attr['color'] = '#e6e6e6'  # Light edge color
    dot.edge_attr['fontcolor'] = '#e6e6e6' # Light font color for edge labels
    
    for n in nodes:
        # dot.node(name=str(id(n)), label = "{ %s | %.2f | ∇ %.3f }" % (n.label, n.data, n.grad), shape='record')
        minus = '−'  # Unicode U+2212
        dot.node(name=str(id(n)), label="{ %s | %s | ∇: %s }" % (
            n.label,
            f"{n.data:.2f}".replace('-', minus),
            f"{n.grad:.3f}".replace('-', minus)
        ), shape='record', color=n.color)
        if n._op:
            dot.node(name=str(id(n)) + n._op, label=n._op, shape='cds', color='aqua')
            dot.edge(str(id(n)) + n._op, str(id(n)))
    
    for n1, n2 in edges:
        dot.edge(str(id(n1)), str(id(n2)) + n2._op)
    
    return dot