import bpy # type: ignore[import-untyped]
import json

def serialize_all_material_nodes(materials):
    """Serializes the nodes of a collection of materials."""
    all_mat_nodes_serialized = []
    for mat in materials:
        all_mat_nodes_serialized.append({mat.name: __serialize_material_nodes(mat)})

    return json.dumps(all_mat_nodes_serialized,indent=4)

def __serialize_material_nodes(material):
    """Serializes every node of a material."""
    nodes = material.node_tree.nodes
    serialized_nodes = []

    for node in nodes:
        serialized_nodes.append(__serialize_node(node))
    return serialized_nodes

def __serialize_node(node):
    """Serializes a single material node."""
    serialized_node = {
        "name": node.name,
        "type": node.type,
    }
    return serialized_node

def serialize_all_material_links(materials):
    """Serializes the links of a collection of materials."""
    all_mat_links_serialized = []
    for mat in materials:
        all_mat_links_serialized.append({mat.name: __serialize_material_links(mat)})

    return json.dumps(all_mat_links_serialized,indent=4)

def __serialize_material_links(material):
    """Serializes every link of a material."""
    links = material.node_tree.links
    serialized_links = []

    for link in links:
        serialized_links.append(__serialize_link(link))
    return serialized_links

def __serialize_link(link):
    """Serializes one material link."""
    serialized_link = {
        "from_node": link.from_node.name,
        "from_socket": link.from_socket.name,
        "to_node": link.to_node.name,
        "to_socket": link.to_socket.name
    }
    return serialized_link
