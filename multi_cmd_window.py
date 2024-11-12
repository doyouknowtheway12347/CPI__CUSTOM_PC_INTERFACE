class Output:
    def __init__(self, no_channels, channel_data=None, total_width=80, 
                 partition_char="|", border=False, headers=None):
        self.no_channels = no_channels
        self.total_width = total_width
        self.partition_char = partition_char
        self.border = border
        self.headers = headers if headers and len(headers) == no_channels else None
        self.channel_data = [list() for _ in range(no_channels)]
        
        if channel_data is not None:
            for i, data in enumerate(channel_data):
                if i < no_channels:
                    self.add_data(i, data)
                else:
                    print(f"Warning: Ignoring excess data for channel {i}.")

    def add_data(self, channel_index, data):
        if 0 <= channel_index < self.no_channels:
            self.channel_data[channel_index].append(str(data))
        else:
            raise ValueError(f"Invalid channel index. Must be between 0 and {self.no_channels - 1}")

    def print_all_data(self, smart_wrap=False):
        column_width = (self.total_width // self.no_channels) - 3
        wrapped_data = []
        
        for channel in self.channel_data:
            channel_rows = []
            for data in channel:
                for part in data.split("\n"):
                    while len(part) > column_width:
                        if smart_wrap:
                            split_index = part.rfind(" ", 0, column_width)
                            split_index = split_index if split_index != -1 else column_width
                        else:
                            split_index = column_width
                        channel_rows.append(part[:split_index].strip())
                        part = part[split_index:].strip()
                    channel_rows.append(part)
            wrapped_data.append(channel_rows)

        max_rows = max(len(rows) for rows in wrapped_data)

        # Print border, headers, and rows
        if self.border:
            print("+" + ("-" * (self.total_width - 2)) + "+")

        if self.headers:
            header_row = [header.center(column_width) for header in self.headers]
            print((self.partition_char + " ").join(header_row).center(self.total_width))
            if self.border:
                print("+" + ("-" * (self.total_width - 2)) + "+")

        for i in range(max_rows):
            row = [
                channel_rows[i].ljust(column_width) if i < len(channel_rows) else " " * column_width 
                for channel_rows in wrapped_data
            ]
            print((f" {self.partition_char} ").join(row).center(self.total_width))

        if self.border:
            print("+" + ("-" * (self.total_width - 2)) + "+")

# Usage example
output = Output(6, total_width=130, partition_char="|", border=True, 
                headers=["Channel 1", "Channel 2", "Channel 3", "Channel 4", "Channel 5", "Channel 6"])
output.add_data(0, "This is some text that will be broken into multiple lines if too long.")
output.add_data(1, "This is channel 1's data. Another line here.\nAnd a new line.")
output.add_data(2, "Just a simple line.")
output.add_data(3, "Here's data that\nspans multiple lines.")
output.add_data(4, "Data for channel 4")
output.add_data(5, "More data for channel 5")

print("\nPrinting all data:")
output.print_all_data(smart_wrap=True)
