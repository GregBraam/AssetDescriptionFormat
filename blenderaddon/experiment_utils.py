import bpy

def serialize_material(material):
    nodes = material.node_tree.nodes
    links = material.node_tree.links
    return

def serialize_node(node):
    serialized_node = {
        "name": node.name,
        "type": node.type,
    }
    return serialized_node

def serialize_link(link):
    serialized_link = {
        "from_node": link.from_node.name,
        "from_socket": link.from_socket.name,
        "to_node": link.to_node.name,
        "to_socket": link.to_socket.name
    }
    return serialized_link
