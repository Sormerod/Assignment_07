#------------------------------------------#
# Title: Assignment07.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# SOrmerod, 2020-Aug-17, Moved the write to File Processing
# SOrmerod, 2020-Aug-18, Moved Delete to Data Processing
# SOrmerod, 2020-Aug-18, Moved CD info inputs to IO
# SOrmerod, 2020-Aug-18, Moved the convertion of CD info inputs to a dictionary to Data Processing
# SOrmerod, 2020-Aug-19, Updated the Doc Strings for the functions that were moved
# SOrmerod, 2020-Aug-25, Updated Title
# SOrmerod, 2020-Aug-25, Updated local variables
# SOrmerod, 2020-Aug-25, Updated permanent data store to use binary data
# SOrmerod, 2020-Aug-25, Updated read_file
# SOrmerod, 2020-Aug-25, Updated write_file
# SOrmerod, 2020-Aug-26, Updated the global variable lstTbl
# SOrmerod, 2020-Aug-26, Added Error handling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
objFile = None  # file object

# -- PROCESSING -- #
class DataProcessor:

    @staticmethod
    def new_Dict(cd_ID, cd_Title, cd_Artist, table):
        """Convert user inputs to Dictionary and adding it to the table

        Args:
            strID: User input ID
            strTitle: User input Title
            strArtist: User input Artist

        Returns:
            None
        """

        dicRow = {'ID': int(cd_ID), 'Title': cd_Title, 'Artist': cd_Artist}
        table.append(dicRow)

    @staticmethod
    def del_CD(ID_to_delete, table):
        """Delete CD based on the ID

        Args:
            ID_to_delete: User input ID to delete

        Returns:
            None
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in table:
            intRowNr += 1
            if row['ID'] == ID_to_delete:
                del table[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        lstTbl.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as fileObj:
            data = pickle.load(fileObj) #load one line of data
        return data

    @staticmethod
    def write_file(file_name, table):
        """Function to save list of dictionaries to text file

        Writes the data from a 2D table (list of dicts) to a file identified by file_name
        one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to write the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None
        """
        with open(file_name, 'wb') as fileObj:
            pickle.dump(table,fileObj)


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table

        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def new_CD():
        """Gets users input for CD info

        Args:
            None

        Returns:
            strID: CD ID number
            strTitle: CD Title
            strArtist: CD Artist

        """
        strID = int(input('Enter an ID: ').strip())
        strTitle = input('Enter the CD\'s Title: ').strip()
        strArtist = input('Enter the Artist\'s Name: ').strip()
        return strID, strTitle, strArtist


# 1. When program starts, read in the currently saved Inventory
try:
    lstTbl = FileProcessor.read_file(strFileName, lstTbl)
except:
    pass

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break

    # 3.2 process load inventory
    if strChoice == 'l':
        strYesNo = input('Would you like to load from file? [y/n] ')
        if strYesNo.lower() == 'y':
            print('loading')
            try:
                lstTbl = FileProcessor.read_file(strFileName, lstTbl)
            except EOFError:
                pass
            except FileNotFoundError:
                with open(strFileName, 'w'):
                    pass
                IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        try:
            strID, strTitle, strArtist = IO.new_CD()
        # 3.3.2 Add item to the table
            DataProcessor.new_Dict(strID, strTitle, strArtist, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError:
            print('That is not an integer!')

    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.

    # 3.5 process delete a CD
    elif strChoice == 'd':
        try:
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
            IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
            IDRow = int(input('Which ID would you like to delete? ').strip())
        # 3.5.2 search thru table and delete CD
            DataProcessor.del_CD(IDRow, lstTbl)
            IO.show_inventory(lstTbl)
            continue  # start loop back at top.
        except ValueError:
            print('That is not an integer!')

    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.

    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




