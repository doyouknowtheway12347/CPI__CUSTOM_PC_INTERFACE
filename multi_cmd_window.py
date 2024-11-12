class Output:
    def __init__(self, no_channels, channel_data=None, total_width=80, 
                 partition_char="|", border=False, headers=None, channel_widths=None, 
                 horizontal_line_char="-", verbose=False):
        # Initialize basic parameters
        self.no_channels = no_channels  # Number of channels
        self.total_width = total_width  # Total width for the entire output
        self.partition_char = partition_char  # Character used for partitioning columns
        self.horizontal_line_char = horizontal_line_char  # Character for horizontal lines
        self.border = border  # Boolean to determine if borders should be printed
        self.verbose = verbose  # Flag to control if additional messages should be printed

        # Set headers if provided, else None
        self.headers = headers if headers and len(headers) == no_channels else None
        
        # Initialize channel_data as empty lists for each channel
        self.channel_data = [list() for _ in range(no_channels)]
        
        # Handle channel widths if provided, otherwise set them to None
        self.channel_widths = channel_widths if channel_widths else [None] * no_channels
        
        # Calculate the remaining width after considering specified channel widths
        total_specified_width = sum(w for w in self.channel_widths if w is not None)
        remaining_width = total_width - total_specified_width - (self.no_channels - 1)  # Subtract space for partition characters
        
        # Check if total specified width exceeds total width
        if remaining_width < 0:
            if self.verbose:
                print(f"Error: The specified widths exceed the total width of {total_width}.")
        elif remaining_width > 0:
            # Distribute remaining width among channels with None width
            num_none = self.channel_widths.count(None)
            if num_none > 0:
                remaining_width_per_channel = remaining_width // num_none
                for i in range(self.no_channels):
                    if self.channel_widths[i] is None:
                        self.channel_widths[i] = remaining_width_per_channel
                if self.verbose:
                    print(f"Warning: The remaining width of {remaining_width} has been distributed evenly.")
        
        # Add provided data to the channels
        if channel_data is not None:
            for i, data in enumerate(channel_data):
                if i < no_channels:
                    self.add_data(i, data)
                else:
                    if self.verbose:
                        print(f"Warning: Ignoring excess data for channel {i}.")

    def add_data(self, channel_index, data):
        """Adds data to a specific channel."""
        if 0 <= channel_index < self.no_channels:
            self.channel_data[channel_index].append(str(data))
        else:
            raise ValueError(f"Invalid channel index. Must be between 0 and {self.no_channels - 1}")

    def print_all_data(self, smart_wrap=False):
        """Prints all channel data with proper formatting."""
        
        # List to hold wrapped data for each channel
        wrapped_data = []
        
        # Process each channel's data
        for i, channel in enumerate(self.channel_data):
            column_width = self.channel_widths[i]  # Width for the current channel
            channel_rows = []
            
            # Split each line of data into multiple parts to fit within the column width
            for data in channel:
                for part in data.split("\n"):
                    while len(part) > column_width:
                        if smart_wrap:
                            # Try to split at the last space within the column width
                            split_index = part.rfind(" ", 0, column_width)
                            if split_index == -1:  # If no space, split at the limit
                                split_index = column_width
                        else:
                            split_index = column_width
                        channel_rows.append(part[:split_index].strip())  # Add the split part
                        part = part[split_index:].strip()  # Remainder for next split
                    channel_rows.append(part)  # Add the last part
            wrapped_data.append(channel_rows)

        # Determine the maximum number of rows to print across all channels
        max_rows = max(len(rows) for rows in wrapped_data)

        # Print border if enabled
        if self.border:
            print("+" + (self.horizontal_line_char * (self.total_width - 2)) + "+")

        # Print headers if provided
        if self.headers:
            header_row = [header.center(self.channel_widths[i]) for i, header in enumerate(self.headers)]
            print(f" {self.partition_char} ".join(header_row).center(self.total_width))
            if self.border:
                print("+" + (self.horizontal_line_char * (self.total_width - 2)) + "+")

        # Print the data rows for each channel
        for i in range(max_rows):
            row = []
            for channel_rows, column_width in zip(wrapped_data, self.channel_widths):
                if i < len(channel_rows):
                    row.append(channel_rows[i].ljust(column_width))  # Add data for the row
                else:
                    row.append(" " * column_width)  # Padding for empty rows

            # Check if any data exceeds the column width and truncate if necessary
            for j, channel in enumerate(row):
                if len(channel) > self.channel_widths[j]:
                    if self.verbose:
                        print(f"Warning: Data in Channel {j + 1} exceeds width and may be truncated.")
                    row[j] = channel[:self.channel_widths[j]]  # Truncate the data if it exceeds the width

            print(f" {self.partition_char} ".join(row).center(self.total_width))  # Print the row

        # Print border if enabled
        if self.border:
            print("+" + (self.horizontal_line_char * (self.total_width - 2)) + "+")

# Usage example
# output = Output(3, total_width=130, partition_char="|", border=True, 
#                 headers=["Channel 1", "Channel 2", "Channel 3"],
#                 channel_widths=[30, 60, None], horizontal_line_char="+",
#                 verbose=True)  # Custom channel widths and verbose flag enabled
# output.add_data(0, "This is some text that will be broken into multiple lines if too long.")
# output.add_data(1, "This is channel 1's data. Another line here.\nAnd a new line.")
# output.add_data(2, "Just a simple line.")

# print("\nPrinting all data:")
# output.print_all_data(smart_wrap=True)

"""
The Output class is designed to manage and display multi-channel data in a formatted table.

It allows for customization of the output table's appearance, including:
- The number of channels
- The total width of the table
- The partition character used between columns
- Horizontal line characters for table borders
- Whether or not to print borders around the table
- The width of each channel
- The ability to wrap and format long data entries to fit within column widths
- Verbosity for warning messages during formatting

Attributes:
    no_channels (int): Number of channels in the table.
    total_width (int): Total width of the table (including partitions).
    partition_char (str): Character used to separate columns.
    horizontal_line_char (str): Character used to draw horizontal lines in the table.
    border (bool): Whether to print borders around the table.
    verbose (bool): If True, prints additional messages for warnings and errors.
    headers (list or None): Optional list of headers for the channels.
    channel_widths (list): A list of widths for each channel, or None for automatic adjustment.
    channel_data (list): A list of data for each channel.

Methods:
    __init__(no_channels, channel_data=None, total_width=80, partition_char="|", 
             border=False, headers=None, channel_widths=None, horizontal_line_char="-", verbose=False):
        Initializes the Output object with the specified settings.
    
    add_data(channel_index, data):
        Adds data to the specified channel.
    
    print_all_data(smart_wrap=False):
        Prints all data from all channels in a formatted table, with optional word wrapping.
    
Usage Example:
    output = Output(3, total_width=130, partition_char="|", border=True, 
                    headers=["Channel 1", "Channel 2", "Channel 3"],
                    channel_widths=[30, 60, None], horizontal_line_char="+",
                    verbose=True)
    output.add_data(0, "This is some text that will be broken into multiple lines if too long.")
    output.add_data(1, "This is channel 1's data. Another line here.\nAnd a new line.")
    output.add_data(2, "Just a simple line.")
    output.print_all_data(smart_wrap=True)
"""