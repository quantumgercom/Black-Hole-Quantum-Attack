import pandas as pd

class DataCollector:
    """
    Data collector to calculate simulations results

    Args:
        dataFrame (optional): DataFrame with all simulation data
    """
    def __init__(self, dataFrame: pd.DataFrame | None = None) -> None:
        self.df: pd.DataFrame | None = dataFrame
        self.standard_deviations: dict[str, float] = {}

    def is_DataFrame(
            self, 
            dataFrame: pd.DataFrame
            ) -> None:
        """
        Find out if it is a DataFrame

        Args:
            dataFrame (required): DataFrame to be analyzed

        Returns:
            Exception: If isn't DataFrame return a Exception, else, return None
        """
        if type(dataFrame) != pd.DataFrame:
            raise Exception("O valor dado não é um DataFrame")

    def get_DataFrame(
            self, 
            dataFrame: pd.DataFrame | None = None, 
            convert: bool | None = None
            ) -> None:
        """
        Get a DataFrame to DataCollector

        Args:
            dataFrame (required): DataFrame or Dict to add on DataCollector
            convert (optional): If is True convert dict to DataFrame
        """
        if convert:
            dataFrame = pd.DataFrame(dataFrame)
        
        # Checks for a DataFrame
        self.is_DataFrame(dataFrame)
        # Save DataFrame
        self.df = dataFrame

    def get_DataFrame_csv(self, path: str) -> None:
        """
        Get a DataFrame from a csv file

        Args:
            path (required): Path to csv file
        """
        # Checks if is a valid path
        if type(path) == str:
            self.df = pd.read_csv(path, encoding='utf-8')
            return
        raise Exception("Não é um caminho válido")
    
    def arithmetic_Mean(self, *columns) -> dict:
        """
        Will calculate the arithmetic mean from columns of DataFrame

        Args:
            *columns (required): Columns of DataFrame

        Returns:
            dict: Dict with all arithmetic means
        """
        # Checks for a DataFrame
        self.is_DataFrame(self.df)

        averages = {}
        for column in columns:
            averages[column] = self.df[column].sum() / len(self.df[column])
        return averages
    
    def standard_Deviation(self, *columns) -> dict:
        """
        Will calculate standard deviations from columns of DataFrame

        Args:
            *columns (required): Columns of DataFrame

        Returns:
            dict: Dict with all standard deviatons
        """
        # Checks for a DataFrame
        self.is_DataFrame(self.df)

        avareges = self.arithmetic_Mean(*columns)
        standard_deviations = {}
        for column in columns:
            variance = 0
            # Used to divide
            number_items = len(self.df[column])

            # Sum all (Xi - u)^2
            for item in self.df[column]:
                variance += (item - avareges[column]) ** 2
            
            variance /= number_items
            # Square root of variance
            standard_deviations[column] = variance ** 0.5

        self.standard_deviations = standard_deviations

        return self.standard_deviations

    def save(
            self, 
            file_name: str, 
            save_standard_deviation: bool | None = None, 
            standard_columns: tuple | None = None
            ) -> None:
        """
        Will save all data from DataCollector on files

        Args:
            file_name (required): Name of the file to be saved (without .extension)
            save_standard_deviation (optional): If True, save the standard deviations
            standard_columns (optional): Columns of DataFrame to be save
        """
        # Checks for a DataFrame
        self.is_DataFrame(self.df)

        # Save DataFrame on csv file
        self.df.to_csv(f'{file_name}.csv', encoding='utf-8', header=True, index=True)

        if save_standard_deviation:
            standard_deviations = pd.DataFrame(self.standard_Deviation(*standard_columns))
            standard_deviations.to_csv(f'{file_name}_standard_deviations.csv', encoding='utf-8', header=True, index=False)
            
if __name__ == "__main__":
    a: dict[int, list] = {
        1:[1, 1],
        2:[2, 1]
    }

    dataCollector: DataCollector = DataCollector()
    dataCollector.get_DataFrame(a, convert=True)
    dataCollector.save('test', save_standard_deviation=True, standard_columns=(1, 2))


class DataGroup:
    """
    Data class with all DataCollectors to use more efficiently
    """
    def __init__(self) -> None:
        self._group: list = list()
        self._iterator: int = 0

    def __getitem__(self, index: int) -> tuple:
        return self._group[index]
    
    def __setitem__(self, index: int, value: tuple[DataCollector]) -> None:
        self._isTuple(value)

        self._group[index] = value
    
    def __len__(self) -> int:
        return len(self._group)

    def __add__(self, value: 'DataGroup') -> 'DataGroup':
        if type(value) == type(self):
            temp_dataGroup: DataGroup = DataGroup()
            temp_dataGroup._group = self._group + value._group
            return temp_dataGroup
        
        raise TypeError(f"{value} is not type DataGroup")
    
    def __iter__(self):
        return self
    
    def __next__(self) -> int:
        if self._iterator >= len(self._group):
            self._iterator = 0
            raise StopIteration
        
        value = self._group[self._iterator]
        self._iterator += 1

        return value

    def __str__(self) -> str:
        return f'{self._group}'
    
    def _isTuple(self, value) -> None:
        """
        Just verify if the value is a tuple

        Args:
            value (required): Value to be analyzed
        """
        if type(value) != tuple:
            raise TypeError("The given value is not a Tuple")
        
    def _isDataCollector(self, value) -> None:
        """
        Just verify if the value is a DataCollector

        Args:
            value (required): Value to be analyzed
        """
        if type(value) != DataCollector:
            raise TypeError("The given value is not a DataCollector")

    def add_Group(self, value: tuple[DataCollector], indexgroup: int | None = None) -> list:
        """
        The safest way to add a Tuple of DataCollectors

        Args:
            value (required): Tuple with DataCollectors
            idexgroup (optional): Index to insert group on especific location

        Returns:
            list: List with all data
        """
        self._isTuple(value)
        
        if indexgroup == None or indexgroup >= len(self._group):
            self._group.append(value)
            return self._group

        self._group.insert(indexgroup, value)

        return self._group

    def add_Data(self, value: DataCollector, indexgroup: int) -> list:
        """
        The safest way to add a DataCollector

        Args:
            value (required): DataCollector to add to group
            indexgroup (required): Index of the group to which the DataCollector will be added

        Returns:
            list: List with all data
        """
        self._isDataCollector(value)

        if indexgroup >= len(self._group):
            self._group.append((value,))
            return self._group
        
        self._group[indexgroup] += (value,)

        return self._group

    def pop(self, indexgroup: int = -1) -> tuple:
        """
        Remove group corresponding to index

        Args:
            indexgroup (required): Index of the group to which will be removed

        Returns:
            tuple: Return removed tuple
        """
        return self._group.pop(indexgroup)

if __name__ == '__main__':
    a: DataGroup = DataGroup()

    a.add_Group((1, 2, 3))
    print(a, a[0])

    a[0] = (1, 2, 4)
    print(a[0])

    dc: DataCollector = DataCollector(pd.DataFrame({1:[1, 2], 2:['a', 'b']}))
    a.add_Data(dc, 1)
    print(a)

    a.add_Group((3, 4, 5))
    print(a)

    a.pop()
    print(a)

    b: DataGroup = DataGroup()
    b.add_Group((5, 6, 7))
    print(b)

    print(a + b)

    for value in a:
        print(value)