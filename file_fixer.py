
from enum import Enum
import re

FILE_LOCATIONS = "/Users/aspanu/Downloads/"
MOVIE_FILE = FILE_LOCATIONS + "movie_metadata1.sql"
OUTPUT_FILE = FILE_LOCATIONS + "movie_metadata_fixed.sql"

class sqlite_file_cleaner:
    
    def get_state(self, line):
        if 'CREATE TABLE' in line:
            return State.CREATE
        if 'INSERT INTO' in line:
            return State.INSERT
        return State.STATUS_QUO

    def get_values_to_replace(self, line, state):
        if state != State.INSERT:
            return ""
        match = re.search("`\w+`", line)
        return "INSERT INTO " + match.group() + " VALUES "

    def process_line(self, line, section_state, prefix):
        if section_state != State.INSERT:
            return line

        line = line.replace("),", ");")
        return prefix + line

    def process_file(self, input_file, output_file):
        out = open(output_file, 'w')

        with open(input_file, 'r') as sql_file:
            region_state = State.STATUS_QUO
            prefix_value = ""
            for line in sql_file:
                state = self.get_state(line)
                if state == State.INSERT:
                    region_state = state
                    prefix_value = self.get_values_to_replace(line, state)
                    line = line.replace("),", ");")
                    out.write(line)
                    continue
                elif state == State.CREATE:
                    region_state = state
                    out.write(line)
                    continue

                # This is the status quo, if we are in the 'create' region, just write to file, otherwise, prefix and then write to file
                if region_state == State.CREATE:
                    out.write(line)
                elif region_state == State.INSERT:
                    line = self.process_line(line, region_state, prefix_value)
                    out.write(line)

        out.close()

class State(Enum):

    CREATE = 0
    INSERT = 1
    STATUS_QUO = 2




def main():
    file_fixer = sqlite_file_cleaner()

    file_fixer.process_file(MOVIE_FILE, OUTPUT_FILE)


if __name__ == "__main__":
    main()