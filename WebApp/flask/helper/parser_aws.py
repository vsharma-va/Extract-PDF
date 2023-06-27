import json
import csv


class ParserAws:
    def __init__(self, file_info: dict) -> None:
        self.file_name = file_info["file_name"]
        self.file_path = file_info["file_path"]
        self.file_extension = file_info["file_extension"]

    def parse_response_for_key_value_pair(self, json_file_info: dict):
        data = None
        with open(self.file_path, "r") as file:
            data = json.load(file)
        word_map = self._map_all_words_to_ids(data)
        key_map = self._map_all_keys_to_values_id(data, word_map)
        value_map = self._map_all_values_to_keys_id(data, word_map)
        final_map = self._get_final_key_value_map(key_map, value_map)
        self._write_dict_to_csv(final_map, json_file_info)
        print("written key value successfully")
    
    def parse_response_for_tables(self):
        data = None
        with open(self.file_path, "r") as file:
            data = json.load(file)
        table_map = self._get_all_tables(data)
        if isinstance(table_map, str):
            print(table_map)
            return
        else: 
            elements = self._map_all_elements_to_ids(data)
            table = self._get_rows_and_columns(table_map, elements)
            self._write_table_dict_to_csv(table_map, elements, table, self.file_name)
            print("present in the output directory")

    def _map_all_words_to_ids(self, response: dict) -> dict:
        word_map = {}
        for element in response["Blocks"]:
            # the result is divided into LINE, WORD, PAGE
            # with their types given in BlockType =
            # each block has an id associated with it. Id is how aws refers to all words in relationships
            # that is why we are mapping all words to their respective id

            if element["BlockType"] == "WORD":
                # element["Text"] contains the actual text value
                word_map[element["Id"]] = element["Text"]
        return word_map

    def _map_all_keys_to_values_id(self, response: dict, word_map: dict) -> dict:
        key_map = {}
        # aws defines key value relationships under BlockType = KEY_VALUE_SET
        # furthermore if the BlockType is KEY or VALUE is defined under EntityType
        # it also defines the KEYs VALUE under Type = VALUE
        # Now to find out the actual text of the KEY, aws adds all the words that are part of that particular key under relation["Type"] = "CHILD"
        # Therefore we can use the earlier function which returned a word dict with all the keys mapped to find out the actual text of the ids is,
        for element in response["Blocks"]:
            if (
                element["BlockType"] == "KEY_VALUE_SET"
                and "KEY" in element["EntityTypes"]
            ):
                for relations in element["Relationships"]:
                    if relations["Type"] == "VALUE":
                        id_value = relations["Ids"]
                    if relations["Type"] == "CHILD":
                        text_value_key = " ".join(
                            [word_map[i] for i in relations["Ids"]]
                        )
                        key_map[text_value_key] = id_value

        return key_map

    def _map_all_values_to_keys_id(self, response: dict, word_map: dict) -> dict:
        # simillar to EntityTypes = KEY but this doesn't have Type = VALUE, but contains an Id = some value which specifies the id of
        # the key
        # it contains a CHILD block which has id of all the words that the VALUE is made up of.
        value_map = {}
        for element in response["Blocks"]:
            if (
                element["BlockType"] == "KEY_VALUE_SET"
                and "VALUE" in element["EntityTypes"]
            ):
                # some elements don't have relationships don't know why 
                # therefore to prevent an error no value found is added
                if 'Relationships' in element:
                    for relations in element["Relationships"]:
                        if relations["Type"] == "CHILD":
                            text_value_value = " ".join(
                                [word_map[i] for i in relations["Ids"]]
                            )
                            value_map[element["Id"]] = text_value_value
                else:
                    value_map[element['Id']] = "No value found"
        return value_map

    def _get_final_key_value_map(self, key_map: dict, value_map: dict):
        final_map = {}
        # all that is remaining is to compare both key map and value map and to substitute the text values
        for i, j in key_map.items():
            final_map[i] = "".join(["".join(value_map[k]) for k in j])
        return final_map
    
    '''
        basic hierarchy ->
        TABLE (under relationships) -> CHILD (can be title, cell etc) (for eg take cell) 
        -> CHILD (inside relationship contains more child ids for whatever is present in the cells, can be words, selection text etc)  
        -> now those ids can be used to find the actual text in the cell
    '''
    
    def _get_all_tables(self, response: dict) -> dict:
        # all tables have the BlockType == TABLE
        # they contain ids to title, footer, cell, merged cell etc.
        # and cells contain ids to words that they contain
        table_elements = []
        for element in response['Blocks']:
            if element['BlockType'] == 'TABLE':
                table_elements.append(element)
        
        if len(table_elements) <= 0:
            return "No tables found"
        else:
            return table_elements
        
    def _map_all_elements_to_ids(self, response: dict) -> dict:
        elements = {}
        for element in response['Blocks']:
            elements[element['Id']] = element
            
        return elements
    
    '''
    TABLE 
    ->(look into CHILD) Ids 
    ->(feed ids to elements) get the whole child element 
    -> check child elements type
    '''
    def _get_rows_and_columns(self, table_elements: list, elements: dict) -> dict:
        table = {}
        # looking into the childs of table
        # and specifically finding CELL
        for single_table_element in table_elements:
            for relationship in single_table_element['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        # cell = blocks_map[child_id] returns the whole block with the matching child_id
                        # so that we can check if that block is a cell or not
                        cell = elements[child_id]
                        if cell['BlockType'] == 'CELL':
                            row_index = cell['RowIndex']
                            col_index = cell['ColumnIndex']
                            # if the row is not present in the table a new one is created
                            if row_index not in table:
                                table[row_index] = {}
                            table[row_index][col_index] = self._get_text(cell, elements)
        return table
    
    '''
    Cell
    ->(look into child ids) Ids
    ->(feed ids to elements) get the whole child element
    ->(check if BlockType = WORD) WORD
    ->(get text)
    '''
    def _get_text(self, cell, elements):
        text = ''
        # all elements don't have Relationships don't know why
        if 'Relationships' in cell:
            for relationship in cell['Relationships']:
                if relationship['Type'] == 'CHILD':
                    for child_id in relationship['Ids']:
                        # get the whole word block
                        word = elements[child_id]
                        if word['BlockType'] == 'WORD':
                            text += word['Text'] + ' '
                            
        return text
    
    def _write_dict_to_csv(self, final_map: dict, json_file_info: dict):
        with open(f'./helper/output/csv/{json_file_info["file_name"]}.csv', "a") as csv_file:
            writer = csv.writer(csv_file)
            for key, value in final_map.items():
                writer.writerow([key, value])
    
    def _write_table_dict_to_csv(self, table_elements: dict, elements: dict, table: dict, file_name: str):
        string = ''
        for index, single_table in enumerate(table_elements):
            temp_string = f'Table: {index}\n\n'
            for i, cell in table.items():
                for j, text in cell.items():
                    # same row elements are seperated by ,
                    temp_string += f'{text},'
                # end of row therefore switch to new line
                temp_string += '\n'
            # end of table. if there are multiple they will be seperated by 5 newlines
            temp_string += '\n\n\n\n\n'
            string += temp_string
            temp_string = ''
        
        with open(f"./helper/output/csv/{file_name}.csv", "wt") as file:
            file.write(string)
        print("table written to csv successfully")