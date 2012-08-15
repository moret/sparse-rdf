from tests.assets.paper import paper_nodes
from tests.assets.paper import paper_paths
from tests.assets.paper import paper_templates

from app.index_parser import index_parser
from app.persistance import db


def set_default_paper_matrix():
    db.replace_all_nodes(paper_nodes)
    db.replace_all_paths(paper_paths)
    db.replace_all_templates(paper_templates)

    index_parser.generate_sparse_matrix()
