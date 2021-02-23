import socket
import struct
import numpy as np
import threading


class UDP_Receiver(threading.Thread):
    def __init__(self,is_running_event, output_pipe, static_ip='192.168.33.30', adc_ip='192.168.33.180',
                 data_port=4098,n_chirps=255,n_rx=4,n_tx=1,n_samples=256):
        threading.Thread.__init__ (self)
        # Create configuration and data destinations
        self.is_running_event = is_running_event
        self.output_pipe = output_pipe
        self.data_recv = (static_ip, data_port)
        # Create sockets)
        self.data_socket = socket.socket(socket.AF_INET,
                                         socket.SOCK_DGRAM,
                                         socket.IPPROTO_UDP)
        # Bind data socket to fpga
        self.data_socket.bind(self.data_recv)

        self.last_bytes = 0
        self.data = []
        self.packet_count = []
        self.byte_count = []
        self.frame_buff = []
        self.curr_buff = None
        self.last_frame = None
        self.lost_packets = None
        self.BYTES_IN_PACKET = 1456

        self.adc_parameters = {'chirps': n_chirps,  # 32
                          'rx': n_rx,
                          'tx': n_tx,
                          'samples': n_samples,
                          'bytes': 2}

        # DYNAMIC
        self.bytes_per_frame = (self.adc_parameters['chirps'] * self.adc_parameters['rx'] * self.adc_parameters['tx'] * self.adc_parameters['samples'] * self.adc_parameters['bytes'])
        self.bytes_in_frame = (self.bytes_per_frame // self.BYTES_IN_PACKET) * self.BYTES_IN_PACKET
        self.packets_in_frame = self.bytes_per_frame / self.BYTES_IN_PACKET
        self.PACKETS_IN_FRAME_CLIPPED = self.bytes_per_frame // self.BYTES_IN_PACKET
        self.uint16_in_packet = self.BYTES_IN_PACKET // 2
        self.uint16_in_frame = self.bytes_per_frame // 2
        self.ret_frame = np.zeros(self.uint16_in_frame, dtype=np.int16)


    def close(self):
        self.data_socket.close()

    def run(self):
        self.read()
        print("UDP receiver quit!")

    def read(self, timeout=1):
        # Wait for start of next frame
        while (self.is_running_event.is_set()):

            data, addr = self.data_socket.recvfrom(4096)
            byte_count = struct.unpack('>Q', b'\x00\x00' + data[4:10][::-1])[0]
            packet_data = np.frombuffer(data[10:], dtype=np.uint16)

            # print(byte_count - last_byte_count)
            if byte_count % self.bytes_in_frame == 0:
                packets_read = 1
                self.ret_frame[0:self.uint16_in_packet] = packet_data
                break

        # Read in the rest of the frame
        while (self.is_running_event.is_set()):
            #Read the packet
            data, addr = self.data_socket.recvfrom(4096)
            sequence_number = struct.unpack('<1l', data[:4])[0]
            curr_idx = ((sequence_number - 1) % self.PACKETS_IN_FRAME_CLIPPED)

            if sequence_number % self.PACKETS_IN_FRAME_CLIPPED == 0 :
            # if  curr_idx==0:
                self.output_pipe.send(self.ret_frame)

            self.ret_frame[curr_idx * self.uint16_in_packet:(curr_idx + 1) * self.uint16_in_packet] = np.frombuffer(data[10:], dtype=np.uint16)




