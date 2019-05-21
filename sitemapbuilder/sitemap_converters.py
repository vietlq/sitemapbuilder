"""Converters to transform sitemap to various formats"""

DOT_TMPL = """digraph G {
ratio="compress"
rankdir=LR
%s
}
"""


def convert_to_dot(sitemap):
    """Convert sitemap to Graphviz .dot format"""
    edges = []
    for caller, callees in sitemap.items():
        for callee in callees:
            edges.append('"%s" -> "%s"' % (caller, callee))
    return DOT_TMPL % '\n'.join(edges)
