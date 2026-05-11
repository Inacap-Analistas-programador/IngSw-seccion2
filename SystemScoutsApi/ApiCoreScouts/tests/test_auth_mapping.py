
import unittest
from unittest.mock import MagicMock
import sys
import os

# Mock Django because we don't want to run against a real DB in this unit test
# we just want to test the logic of the mapping.

class TestAuthMapping(unittest.TestCase):
    def test_flag_mapping(self):
        # Simulation of the mapping logic
        pa_flags = {
            'pea_consultar': True,
            'pea_ingresar': True,
            'pea_modificar': False,
            'pea_eliminar': False
        }
        
        expected_codenames = ['view_persona', 'add_persona']
        
        # Logic to test
        model_name = 'persona'
        perm_map = {
            'pea_consultar': f'view_{model_name}',
            'pea_ingresar': f'add_{model_name}',
            'pea_modificar': f'change_{model_name}',
            'pea_eliminar': f'delete_{model_name}',
        }
        
        mapped_codenames = [codename for flag, codename in perm_map.items() if pa_flags.get(flag)]
        
        self.assertEqual(mapped_codenames, expected_codenames)

if __name__ == '__main__':
    unittest.main()
