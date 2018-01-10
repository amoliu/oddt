"""Common utilities for ODDT"""
import numpy as np
import oddt


def is_molecule(obj):
    """Check whether an object is an `oddt.toolkits.{rdk,ob}.Molecule` instance.
    """
    return is_openbabel_molecule(obj) or is_rdkit_molecule(obj)


def is_openbabel_molecule(obj):
    """Check whether an object is an `oddt.toolkits.ob.Molecule` instance."""
    return (hasattr(oddt.toolkits, 'ob') and
            isinstance(obj, oddt.toolkits.ob.Molecule))


def is_rdkit_molecule(obj):
    """Check whether an object is an `oddt.toolkits.rdk.Molecule` instance."""
    return (hasattr(oddt.toolkits, 'rdk') and
            isinstance(obj, oddt.toolkits.rdk.Molecule))


def check_molecule(mol,
                   force_protein=False,
                   force_coords=False,
                   non_zero_atoms=False):
    """Universal validator of molecule objects. Usage of positional arguments is
    allowed only for molecule object, otherwise it is prohibitted (i.e. the
    order of arguments **will** change). Desired properties of molecule are
    validated based on specified arguments. By default only the object type is
    checked. In case of discrepancy to the specification a `ValueError` is
    raised with appropriate message.

    Parameters
    ----------
        mol: oddt.toolkit.Molecule object
            Object to verify

        force_protein: bool (default=False)
            Force the molecule to be marked as protein (mol.protein).

        force_coords: bool (default=False)
            Force the molecule to have non-zero coordinates.

        non_zero_atoms: bool (default=False)
            Check if molecule has at least one atom.

    """
    # TODO 2to3 force only one positional argument by adding * to args
    if not is_molecule(mol):
        raise ValueError('Molecule object was expected, insted got: %s'
                         % str(mol))

    if force_protein and not mol.protein:
        raise ValueError('Molecule "%s" is not marked as a protein. Mark it by '
                         'setting the protein property to `True` (`mol.protein '
                         '= True)' % mol.title)

    if force_coords and (not mol.coords.any() or
                         np.isnan(mol.coords).any()):
        raise ValueError('Molecule "%s" has no 3D coordinates. All atoms are '
                         'located at (0, 0, 0).' % mol.title)

    if non_zero_atoms and len(mol.atoms) == 0:
        raise ValueError('Molecule "%s" has zero atoms.' % mol.title)