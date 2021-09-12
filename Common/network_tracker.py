import time
import psutil

# Returning constants from psutil.net_io_counters result
# Index : number of bytes sent
BYTES_SENT = 0
# Index : number of bytes received
BYTES_RECV = 1


class NetworkTracker:
    
    def __init__(self) -> None:
        self.initial_bytes_sent = self.get_total_bytes_sent()
        self.initial_bytes_recv = self.get_total_bytes_recv()

        self.last_bytes_sent = self.get_total_bytes_sent()
        # returns the time as floating point number expressed in seconds since the epoch, in UTC.
        self.last_bytes_sent_time = time.time() 
        
        self.last_bytes_recv = self.get_total_bytes_recv()
        # returns the time as floating point number expressed in seconds since the epoch, in UTC.
        self.last_bytes_sent_recv = time.time()


    def get_total_bytes_sent(self):
        return psutil.net_io_counters(pernic=False)[BYTES_SENT]
    def get_total_byt_recv(self):
        return psutil.net_io_counters(pernic=False)[BYTES_RECV]


    def get_total_data_used(self):
        return ((self.get_total_bytes_sent() - self.initial_bytes_sent) + \
                (self.get_total_bytes_recv() - self.initial_bytes_recv))
    

    def get_current_upload_speed(self):
        current_time_in_sec = time.time() - self.last_bytes_sent_time
        current_nr_of_bytes = self.get_total_bytes_sent() - self.last_bytes_sent

        self.last_bytes_sent = self.get_total_bytes_sent()
        self.last_bytes_sent_time = time.time()

        return (current_nr_of_bytes / current_time_in_sec) if current_time_in_sec != 0 else 0

    
    def get_current_download_speed(self):
        current_time_in_sec = time.time() - self.last_bytes_sent_recv
        current_nr_of_bytes = self.get_total_bytes_recv() - self.last_bytes_recv

        self.last_bytes_recv = self.get_total_bytes_recv()
        self.last_bytes_sent_time = time.time()

        return (current_nr_of_bytes / current_time_in_sec) if current_time_in_sec != 0 else 0
