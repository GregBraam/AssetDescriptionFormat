import bpy # type: ignore[import-untyped]
import json

def serialize_all_material_nodes(materials: list[bpy.types.Material]) -> str:
    """Serializes the nodes of a collection of materials."""
    all_mat_nodes_serialized = []
    for mat in materials:
        all_mat_nodes_serialized.append({mat.name: __serialize_material_nodes(mat)})

    return json.dumps(all_mat_nodes_serialized,indent=4)

def __serialize_material_nodes(material: bpy.types.Material) -> list[dict[str,str]]:
    """Serializes every node of a material."""
    nodes: list[bpy.types.Node] = material.node_tree.nodes
    serialized_nodes: list[dict[str,str]] = []

    for node in nodes:
        serialized_nodes.append(__serialize_node(node))
    return serialized_nodes

def __serialize_node(node: bpy.types.Node) -> dict[str,str]:
    """Serializes a single material node."""
    serialized_node: dict[str,str] = {
        "name": node.name,
        "type": node.type,
    }
    return serialized_node

def serialize_all_material_links(materials: list[bpy.types.Material]) -> str:
    """Serializes the links of a collection of materials."""
    all_mat_links_serialized = []
    for mat in materials:
        all_mat_links_serialized.append({mat.name: __serialize_material_links(mat)})

    return json.dumps(all_mat_links_serialized,indent=4)

def __serialize_material_links(material: bpy.types.Material) -> list[dict[str,str]]:
    """Serializes every link of a material."""
    links: list[bpy.types.NodeLink] = material.node_tree.links
    serialized_links: list[dict[str,str]] = []

    for link in links:
        serialized_links.append(__serialize_link(link))
    return serialized_links

def __serialize_link(link: bpy.types.NodeLink) -> dict[str,str]:
    """Serializes one material link."""
    serialized_link: dict[str,str] = {
        "from_node": link.from_node.name,
        "from_socket": link.from_socket.name,
        "to_node": link.to_node.name,
        "to_socket": link.to_socket.name
    }
    return serialized_link
