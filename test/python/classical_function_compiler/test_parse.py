# This code is part of Qiskit.
#
# (C) Copyright IBM 2020.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Tests the classicalfunction parser."""
import unittest

from qiskit.circuit.classicalfunction import ClassicalFunctionParseError
from qiskit.circuit.classicalfunction import classical_function as compile_classical_function
from qiskit.circuit.classicalfunction.classicalfunction import HAS_TWEEDLEDUM

from qiskit.test import QiskitTestCase
from . import bad_examples as examples


class TestParseFail(QiskitTestCase):
    """Tests bad_examples with the classicalfunction parser."""

    def assertExceptionMessage(self, context, message):
        """Asserts the message of an exception context"""
        self.assertTrue(message in context.exception.args[0])

    @unittest.skipUnless(HAS_TWEEDLEDUM, 'tweedledum not available')
    def test_id_bad_return(self):
        """Trying to parse examples.id_bad_return raises ClassicalFunctionParseError"""
        with self.assertRaises(ClassicalFunctionParseError) as context:
            compile_classical_function(examples.id_bad_return)
        self.assertExceptionMessage(context, 'return type error')

    @unittest.skipUnless(HAS_TWEEDLEDUM, 'tweedledum not available')
    def test_id_no_type_arg(self):
        """Trying to parse examples.id_no_type_arg raises ClassicalFunctionParseError"""
        with self.assertRaises(ClassicalFunctionParseError) as context:
            compile_classical_function(examples.id_no_type_arg)
        self.assertExceptionMessage(context, 'argument type is needed')

    @unittest.skipUnless(HAS_TWEEDLEDUM, 'tweedledum not available')
    def test_id_no_type_return(self):
        """Trying to parse examples.id_no_type_return raises ClassicalFunctionParseError"""
        with self.assertRaises(ClassicalFunctionParseError) as context:
            compile_classical_function(examples.id_no_type_return)
        self.assertExceptionMessage(context, 'return type is needed')

    @unittest.skipUnless(HAS_TWEEDLEDUM, 'tweedledum not available')
    def test_out_of_scope(self):
        """Trying to parse examples.out_of_scope raises ClassicalFunctionParseError"""
        with self.assertRaises(ClassicalFunctionParseError) as context:
            compile_classical_function(examples.out_of_scope)
        self.assertExceptionMessage(context, 'out of scope: c')
