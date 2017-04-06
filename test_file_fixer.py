import unittest
from file_fixer import sqlite_file_cleaner
from file_fixer import State

class file_fixer_test(unittest.TestCase):
    
    def test_compiles(self):
        file_fixer = sqlite_file_cleaner()
        self.assertTrue(True)

    def test_get_state(self):
        file_fixer = sqlite_file_cleaner()
        state = file_fixer.get_state("INSERT INTO `table`")
        self.assertEquals(state, State.INSERT)

        state = file_fixer.get_state("CREATE TABLE \"tarantino\"")
        self.assertEquals(state, State.CREATE)

        state = file_fixer.get_state(");")
        self.assertEquals(state, State.STATUS_QUO)

    def test_get_values_to_replace(self):
        file_fixer = sqlite_file_cleaner()
        state = file_fixer.get_state("CREATE TABLE")
        value_to_replace = file_fixer.get_values_to_replace("INSERT INTO `tarantino` VALUES (1,'0.40','word','dick',4497),", state)
        self.assertEquals(value_to_replace, "")

        state = file_fixer.get_state("INSERT INTO")
        self.assertEquals(state, State.INSERT)
        value_to_replace = file_fixer.get_values_to_replace("INSERT INTO `tarantino` VALUES (1,'0.40','word','dick',4497),", state)
        self.assertEquals(value_to_replace, "INSERT INTO `tarantino` VALUES ")

    def test_process_line(self):
        file_fixer = sqlite_file_cleaner()
        file_fixer.process_line("INSERT INTO `tarantino` VALUES (1,'0.40','word','dick',4497),")