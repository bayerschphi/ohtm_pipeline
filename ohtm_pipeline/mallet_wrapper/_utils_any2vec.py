## encoding: utf-8
# module gensim.models._utils_any2vec
# from C:\Users\phili\anaconda3\envs\OHD_Migration_und_Heimat\lib\site-packages\gensim\models\_utils_any2vec.cp37-win_amd64.pyd
# by generator 1.147
""" General functions used for any2vec models. """

# imports
import builtins as __builtins__ # <module 'builtins' (built-in)>
import numpy as np # C:\Users\phili\anaconda3\envs\OHD_Migration_und_Heimat\lib\site-packages\numpy\__init__.py

# Variables with simple values

PY2 = False

# functions

def compute_ngrams(word, unsigned_int_min_n, unsigned_int_max_n): # real signature unknown; restored from __doc__
    """
    compute_ngrams(word, unsigned int min_n, unsigned int max_n)
    Get the list of all possible ngrams for a given word.

        Parameters
        ----------
        word : str
            The word whose ngrams need to be computed.
        min_n : unsigned int
            Minimum character length of the ngrams.
        max_n : unsigned int
            Maximum character length of the ngrams.

        Returns
        -------
        list of str
            Sequence of character ngrams.
    """
    pass

def compute_ngrams_bytes(word, unsigned_int_min_n, unsigned_int_max_n): # real signature unknown; restored from __doc__
    """
    compute_ngrams_bytes(word, unsigned int min_n, unsigned int max_n)
    Computes ngrams for a word.

        Ported from the original FB implementation.

        Parameters
        ----------
        word : str
            A unicode string.
        min_n : unsigned int
            The minimum ngram length.
        max_n : unsigned int
            The maximum ngram length.

        Returns:
        --------
        list of str
            A list of ngrams, where each ngram is a list of **bytes**.

        See Also
        --------
        `Original implementation <https://github.com/facebookresearch/fastText/blob/7842495a4d64c7a3bb4339d45d6e64321d002ed8/src/dictionary.cc#L172>`__
    """
    pass

def ft_hash_broken(unicode_string): # real signature unknown; restored from __doc__
    """
    ft_hash_broken(unicode string)
    Calculate hash based on `string`.

        This implementation is broken, see https://github.com/RaRe-Technologies/gensim/issues/2059.
        It is here only for maintaining backwards compatibility with older models.

        Parameters
        ----------
        string : unicode
            The string whose hash needs to be calculated.

        Returns
        -------
        unsigned int
            The hash of the string.
    """
    pass

def ft_hash_bytes(bytes_bytez): # real signature unknown; restored from __doc__
    """
    ft_hash_bytes(bytes bytez)
    Calculate hash based on `bytez`.
        Reproduce `hash method from Facebook fastText implementation
        <https://github.com/facebookresearch/fastText/blob/master/src/dictionary.cc>`_.

        Parameters
        ----------
        bytez : bytes
            The string whose hash needs to be calculated, encoded as UTF-8.

        Returns
        -------
        unsigned int
            The hash of the string.
    """
    pass

# no classes
# variables with complex values

__loader__ = None # (!) real value is '<_frozen_importlib_external.ExtensionFileLoader object at 0x000001E641002AC8>'

__spec__ = None # (!) real value is "ModuleSpec(name='gensim.models._utils_any2vec', loader=<_frozen_importlib_external.ExtensionFileLoader object at 0x000001E641002AC8>, origin='C:\\\\Users\\\\phili\\\\anaconda3\\\\envs\\\\OHD_Migration_und_Heimat\\\\lib\\\\site-packages\\\\gensim\\\\models\\\\_utils_any2vec.cp37-win_amd64.pyd')"

__test__ = {}

