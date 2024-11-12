class Output:
    def __init__(self, no_channels, channel_data=None, total_width=80):
        self.no_channels = no_channels
        self.total_width = total_width
        self.channel_data = [list() for _ in range(no_channels)]
        
        # Initialize channel data if provided
        if channel_data is not None:
            for i, data in enumerate(channel_data):
                if i < no_channels:
                    self.add_data(i, data)
                else:
                    print(f"Warning: Ignoring excess data for channel {i}.")

    def add_data(self, channel_index, data):
        """
        Add data as a single string to the specified channel.
        """
        if 0 <= channel_index < self.no_channels:
            # Ensure data is treated as a string and add it to the channel's data list
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

        for i in range(max_rows):
            row = [channel_rows[i].ljust(column_width) if i < len(channel_rows) else " " * column_width for channel_rows in wrapped_data]
            print(" | ".join(row))








# Usage example
output = Output(2, total_width=80)
output.add_data(0, "This is some text that will be broken into multiple lines if too long.")
output.add_data(1, "This is channel 1's data. Another line here.\nAnd a new line.")
# output.add_data(2, "Just a simple line.")
# output.add_data(3, "Here's data that\nspans multiple lines.")
# output.add_data(4, "Data for channel 4")
# output.add_data(5, "More data for channel 5")

print("\nPrinting all data:")
output.print_all_data(smart_wrap=True)
