"""
A :class:`~allennlp.modules.text_field_embedders.text_field_embedder.TextFieldEmbedder`
is a ``Module`` that takes as input the ``dict`` of NumPy arrays
produced by a :class:`~allennlp.data.fields.text_field.TextField` and
returns as output an embedded representation of the tokens in that field.
"""

from allennlp.modules.text_field_embedders.text_field_embedder import TextFieldEmbedder
from allennlp.modules.text_field_embedders.basic_text_field_embedder import BasicTextFieldEmbedder
