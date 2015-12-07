# -*- coding: utf-8 -*-
import ctypes  
# import logging
import os
import string
import random
from threading import Thread

from defines import *
# log = logging.getLogger()


BUFSIZE = 512

def _rand_string(a, b):
    return "".join(random.choice(string.ascii_lowercase)
                   for x in xrange(random.randint(a, b)))

PIPE = "\\\\.\\PIPE\\" + _rand_string(6, 10)

class PipeServer(Thread):
    """Cuckoo PIPE server.

    This Pipe Server receives notifications from the injected processes for
    new processes being spawned and for files being created or deleted.
    """

    def __init__(self, pipe_name=PIPE):
        """@param pipe_name: Cuckoo PIPE server name."""
        Thread.__init__(self)
        self.pipe_name = pipe_name
        self.do_run = True

    def stop(self):
        """Stop PIPE server."""
        self.do_run = False

    def run(self):
        """Create and run PIPE server.
        @return: operation status.
        """
        while self.do_run:
            # Create the Named Pipe.
            h_pipe = KERNEL32.CreateNamedPipeA(self.pipe_name,
                                               PIPE_ACCESS_DUPLEX,
                                               PIPE_TYPE_MESSAGE | \
                                               PIPE_READMODE_MESSAGE | \
                                               PIPE_WAIT,
                                               PIPE_UNLIMITED_INSTANCES,
                                               BUFSIZE,
                                               BUFSIZE,
                                               0,
                                               None)

            if h_pipe == INVALID_HANDLE_VALUE:
                return False

            # If we receive a connection to the pipe, we invoke the handler.
            if KERNEL32.ConnectNamedPipe(h_pipe, None) or \
                            KERNEL32.GetLastError() == ERROR_PIPE_CONNECTED:
                threed_id = PipeHandler(h_pipe)
                p = Pp(h_process=threed_id, threed_id= threed_id)
                dll = os.path.join("dll", "cuckoomon.dll")
                p.inject(dll)
            else:
                KERNEL32.CloseHandle(h_pipe)

        return True



class PipeHandler(Thread):
    """Pipe Handler.

    This class handles the notifications received through the Pipe Server and
    decides what to do with them.
    """

    def __init__(self, h_pipe):
        """@param h_pipe: PIPE to read."""
        Thread.__init__(self)
        self.h_pipe = h_pipe

    def run(self):
        """Run handler.
        @return: operation status.
        """
        data = ""
        response = "OK"
        wait = False
        proc = None

        # Read the data submitted to the Pipe Server.
        while True:
            bytes_read = c_int(0)

            buf = create_string_buffer(BUFSIZE)
            success = KERNEL32.ReadFile(self.h_pipe,
                                        buf,
                                        sizeof(buf),
                                        byref(bytes_read),
                                        None)

            data += buf.value

            if not success and KERNEL32.GetLastError() == ERROR_MORE_DATA:
                continue
            # elif not success or bytes_read.value == 0:
            #    if KERNEL32.GetLastError() == ERROR_BROKEN_PIPE:
            #        pass

            break

        if data:
            command = data.strip()


            data = command[8:]

            process_id = thread_id = None
            if not "," in data:
                if data.isdigit():
                    process_id = int(data)
            elif len(data.split(",")) == 2:
                process_id, thread_id = data.split(",")
                if process_id.isdigit():
                    process_id = int(process_id)
                else:
                    process_id = None

                if thread_id.isdigit():
                    thread_id = int(thread_id)
                else:
                    thread_id = None
        return thread_id











class Pp:
    def __init__(self, h_process=0, thread_id=0, h_thread=0):
        self.pid = process_id
        self.h_process = h_process
        self.h_thread = h_thread
        self.thread_id = thread_id

    def inject(self, dll=os.path.join("dll", "cuckoomon.dll"), apc=True):
        """Cuckoo DLL injection.
        @param dll: Cuckoo DLL path.
        @param apc: APC use.
        """
        if self.pid == 0:
            # log.warning("No valid pid specified, injection aborted")
            return False

        self.h_process = KERNEL32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        self.h_thread = KERNEL32.OpenThread(THREAD_ALL_ACCESS, False, self.thread_id)

        # if not self.is_alive():
        #     log.warning("The process with pid %d is not alive, injection "
        #                 "aborted" % self.pid)
        #     return False

        # dll = randomize_dll(dll)

        if not dll or not os.path.exists(dll):
            # log.warning("No valid DLL specified to be injected in process "
            #             "with pid %d, injection aborted" % self.pid)
            return False

        arg = KERNEL32.VirtualAllocEx(self.h_process,
                                      None,
                                      len(dll) + 1,
                                      MEM_RESERVE | MEM_COMMIT,
                                      PAGE_READWRITE)

        if not arg:
            # log.error("VirtualAllocEx failed when injecting process with "
            #           "pid %d, injection aborted (Error: %s)"
            #           % (self.pid, get_error_string(KERNEL32.GetLastError())))
            return False

        bytes_written = c_int(0)
        if not KERNEL32.WriteProcessMemory(self.h_process,
                                           arg,
                                           dll + "\x00",
                                           len(dll) + 1,
                                           byref(bytes_written)):
            # log.error("WriteProcessMemory failed when injecting process "
            #           "with pid %d, injection aborted (Error: %s)"
            #           % (self.pid, get_error_string(KERNEL32.GetLastError())))
            return False

        kernel32_handle = KERNEL32.GetModuleHandleA("kernel32.dll")
        load_library = KERNEL32.GetProcAddress(kernel32_handle,
                                               "LoadLibraryA")

        # config_path = os.path.join(os.getenv("TEMP"), "%s.ini" % self.pid)
        # with open(config_path, "w") as config:
        #     cfg = Config("analysis.conf")
        #
        #     config.write("host-ip={0}\n".format(cfg.ip))
        #     config.write("host-port={0}\n".format(cfg.port))
        #     config.write("pipe={0}\n".format(PIPE))
        #     config.write("results={0}\n".format(PATHS["root"]))
        #     config.write("analyzer={0}\n".format(os.getcwd()))
        #     config.write("first-process={0}\n".format(Process.first_process))
        #
        #     Process.first_process = False

        if apc or self.suspended:
            # log.info("Using QueueUserAPC injection")
            if not self.h_thread:
                # log.info("No valid thread handle specified for injecting "
                #          "process with pid %d, injection aborted" % self.pid)
                return False

            if not KERNEL32.QueueUserAPC(load_library, self.h_thread, arg):
                # log.error("QueueUserAPC failed when injecting process "
                #           "with pid %d (Error: %s)"
                #           % (self.pid,
                #              get_error_string(KERNEL32.GetLastError())))
                return False
            # log.info("Successfully injected process with pid %d" % self.pid)

        return True


if __name__ =='__main__':  
    if 0:
        print 'x'
    elif 1:
        print 'z'
    # procupdll = ctypes.cdll.LoadLibrary("InjectAssist.dll")
    # process_id = procupdll.GetPIDbyName('services.exe')
    # print process_id
    # if procupdll.EnableOpenprocPriv() == 0:
    #     print "提权失败"

    # pip = PipeServer()
    # pip.run()
    # h_process = KERNEL32.OpenProcess(PROCESS_ALL_ACCESS, False, int(process_id))
    # p = Pp(process_id, h_process)
    # dll = os.path.join("dll", "cuckoomon.dll")
    # p.inject(dll)
